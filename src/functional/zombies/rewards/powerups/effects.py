""" Each power-up's effect: timed buffs, Nuke, Carpenter, Random Perk and the sales. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from .types import BONFIRE_SALE_DURATION, FIRE_SALE_DURATION, TIMED_POWERUPS, pu_activate_sound, pu_snd


# Functions
def write_powerup_effects() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Timed power-ups: Insta Kill, Double Points, Unlimited Ammo All share the same bossbar+scoreboard activation pattern, driven by TIMED_POWERUPS.
	for pu_id, v in TIMED_POWERUPS.items():
		duration: int     = v.duration
		scoreboard: str   = v.scoreboard
		bossbar_id: str   = v.bossbar_id
		display_name: str = v.display
		bb_color: str     = v.bb_color
		write_versioned_function(f"zombies/powerups/activate/{pu_id}", f"""
scoreboard players set @a[scores={{{ns}.zb.in_game=1}}] {ns}.special.{scoreboard} {duration}
bossbar remove {ns}:{bossbar_id}
bossbar add {ns}:{bossbar_id} {{"text":"{display_name}","bold":true,"color":"{bb_color}"}}
bossbar set {ns}:{bossbar_id} max {duration}
bossbar set {ns}:{bossbar_id} value {duration}
bossbar set {ns}:{bossbar_id} color {bb_color}
bossbar set {ns}:{bossbar_id} style progress
bossbar set {ns}:{bossbar_id} players @a[scores={{{ns}.zb.in_game=1}}]
{pu_activate_sound(ns, v)}
""")

	## 5. Carpenter (instant barricade repair) — no chat message; +200 points, doubled with Double Points
	write_versioned_function("zombies/powerups/activate/carpenter", f"""
function {ns}:v{version}/zombies/barricades/repair_all
{pu_snd(ns, "carpenter")}
scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points 200
scoreboard players add @a[scores={{{ns}.zb.in_game=1,{ns}.special.double_points=1..}}] {ns}.zb.points 200
""")

	## 6.
	## Nuke — kaboom + soul layer, white screen flash, zombies catch fire (no chat message).
	## +400 points to everyone, doubled to +800 for players with Double Points.
	write_versioned_function("zombies/powerups/activate/nuke", f"""
execute as @a[tag={ns}.pu_collecting,scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/nuke
scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points 400
scoreboard players add @a[scores={{{ns}.zb.in_game=1,{ns}.special.double_points=1..}}] {ns}.zb.points 400

# Kaboom + additional layer + soul whoosh (played together)
{pu_snd(ns, "nuke")}
{pu_snd(ns, "nuke_additional")}
{pu_snd(ns, "nuke_soul", 0.8)}

# White screen flash for ~1s (blindness fades to white), and set every zombie on fire
execute as @a[scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/powerups/nuke_flash
execute as @e[tag={ns}.nukable] at @s run function {ns}:v{version}/zombies/powerups/nuke_fire_one
""")

	## Nuke white-flash for a player: the firework 'flash' particle renders a brief white fullscreen flash when emitted at the camera (Black Ops nuke screen flash).
	write_versioned_function("zombies/powerups/nuke_flash", """
execute at @s anchored eyes run particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ^ ^ ^0.4 0 0 0 0 1 force @s
""")

	## Set one zombie on fire + emit fire particles (called as @s = nukable entity)
	write_versioned_function("zombies/powerups/nuke_fire_one", f"""
data merge entity @s {{Fire:1200s}}
effect give @s minecraft:fire_resistance infinite 0 true
particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 12 force @a[scores={{{ns}.zb.in_game=1}},distance=..48]
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 6 force @a[scores={{{ns}.zb.in_game=1}},distance=..48]
""")

	## 7.
	## Random Perk — draws from the shared available-perk pool (perks placed on THIS map, unowned by the collector).
	## See zombies/perks.py `pool/*` (README task 4).
	write_versioned_function("zombies/powerups/activate/random_perk", f"""
# Pick a random unowned perk from the map's placed perks for the collecting player
tag @p[tag={ns}.pu_collecting] add {ns}.pool_target
scoreboard players set #pool_all_perks {ns}.data 0
function {ns}:v{version}/zombies/perks/pool/choose
tag @a[tag={ns}.pool_target] remove {ns}.pool_target

# Nothing available: the collector already owns every perk placed on this map
execute if score #pool_chosen {ns}.data matches ..-1 run return run tellraw @p[tag={ns}.pu_collecting] [{MGS_TAG},{{"text":"You already own every perk on the map!","color":"yellow"}}]

# Grant the chosen perk to the collector
execute as @p[tag={ns}.pu_collecting] run function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pool

# Announce + sound
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Random Perk dropped for ","color":"light_purple"}},{{"selector":"@p[tag={ns}.pu_collecting]","color":"light_purple","bold":true}},{{"text":"!","color":"light_purple"}}]
{pu_snd(ns, "random_perk")}
""")

	## 8. Free PAP
	write_versioned_function("zombies/powerups/activate/free_pap", f"""
execute as @p[tag={ns}.pu_collecting] run function {ns}:v{version}/zombies/pap/on_free_pap
""")

	## 9. Cash Drop: 400-1600 random points to all players; doubled if double_points active
	write_versioned_function("zombies/powerups/activate/cash_drop", f"""
# Roll 4..16 * 100 = 400..1600 points
execute store result score #pu_cash {ns}.data run random value 4..16
scoreboard players operation #pu_cash {ns}.data *= #100 {ns}.data

# Double the reward if double_points is active for the collecting player
execute if score @p[tag={ns}.pu_collecting] {ns}.special.double_points matches 1.. run scoreboard players operation #pu_cash {ns}.data *= #2 {ns}.data

# Award to all in-game players
execute as @a[scores={{{ns}.zb.in_game=1}}] run scoreboard players operation @s {ns}.zb.points += #pu_cash {ns}.data

# Announce with amount
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Cash Drop! ","color":"green","bold":true}},{{"text":"+","color":"gold"}},{{"score":{{"name":"#pu_cash","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" points each!","color":"gold"}}]
{pu_snd(ns, "bonus_points")}
""")

	## 10. Fire Sale: Mystery Box costs 10 points for {FIRE_SALE_DURATION // 20}s (global timer + bossbar)
	write_versioned_function("zombies/powerups/activate/fire_sale", f"""
# Remember whether a Fire Sale was already running (so we don't re-trigger song/temp boxes)
scoreboard players set #fs_was_active {ns}.data 0
execute if score #zb_fire_sale_timer {ns}.data matches 1.. run scoreboard players set #fs_was_active {ns}.data 1

# Save the normal price only when no Fire Sale is already running (so we don't snapshot the discount)
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run scoreboard players operation #zb_fire_sale_saved {ns}.data = #zb_mystery_box_price {ns}.config

# Apply the discount and (re)start the timer
scoreboard players set #zb_mystery_box_price {ns}.config 10
scoreboard players set #zb_fire_sale_timer {ns}.data {FIRE_SALE_DURATION}

# Bossbar
bossbar remove {ns}:pu_fire_sale
bossbar add {ns}:pu_fire_sale {{"text":"Fire Sale","bold":true,"color":"light_purple"}}
bossbar set {ns}:pu_fire_sale max {FIRE_SALE_DURATION}
bossbar set {ns}:pu_fire_sale value {FIRE_SALE_DURATION}
bossbar set {ns}:pu_fire_sale color pink
bossbar set {ns}:pu_fire_sale style progress
bossbar set {ns}:pu_fire_sale players @a[scores={{{ns}.zb.in_game=1}}]

# Only on a NEW Fire Sale: jingle + song (don't restack the song) + temp boxes everywhere
execute if score #fs_was_active {ns}.data matches 0 run {pu_snd(ns, "fire_sale")}
execute if score #fs_was_active {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}}] run playsound {ns}:zombies/powerups/fire_sale_song ambient @s ~ ~ ~ 0.3 1.0
execute if score #fs_was_active {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/fire_sale_start
""")

	## Fire Sale global tick: countdown, bossbar update, restore price on expiry
	write_versioned_function("zombies/powerups/fire_sale_tick", f"""
# Decrement the shared timer
scoreboard players operation #zb_fire_sale_timer {ns}.data -= #tick_delta {ns}.data

# Expired: restore the saved price, remove the bossbar, stop the song, remove temp boxes
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run scoreboard players operation #zb_mystery_box_price {ns}.config = #zb_fire_sale_saved {ns}.data
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run bossbar remove {ns}:pu_fire_sale
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run stopsound @a[scores={{{ns}.zb.in_game=1}}] ambient {ns}:zombies/powerups/fire_sale_song
execute if score #zb_fire_sale_timer {ns}.data matches ..0 run function {ns}:v{version}/zombies/mystery_box/fire_sale_end

# Still active: update bossbar value
execute if score #zb_fire_sale_timer {ns}.data matches 1.. store result bossbar {ns}:pu_fire_sale value run scoreboard players get #zb_fire_sale_timer {ns}.data
""")

	## 11. Bonfire Sale: Pack-a-Punch costs 200 (1000/5) for {BONFIRE_SALE_DURATION // 20}s
	write_versioned_function("zombies/powerups/activate/bonfire_sale", f"""
scoreboard players set #zb_bonfire_sale_timer {ns}.data {BONFIRE_SALE_DURATION}

# Bossbar
bossbar remove {ns}:pu_bonfire_sale
bossbar add {ns}:pu_bonfire_sale {{"text":"Bonfire Sale","bold":true,"color":"gold"}}
bossbar set {ns}:pu_bonfire_sale max {BONFIRE_SALE_DURATION}
bossbar set {ns}:pu_bonfire_sale value {BONFIRE_SALE_DURATION}
bossbar set {ns}:pu_bonfire_sale color yellow
bossbar set {ns}:pu_bonfire_sale style progress
bossbar set {ns}:pu_bonfire_sale players @a[scores={{{ns}.zb.in_game=1}}]
{pu_snd(ns, "bonfire_sale")}
""")

	## Bonfire Sale global tick: countdown + bossbar, clears itself on expiry
	write_versioned_function("zombies/powerups/bonfire_sale_tick", f"""
scoreboard players operation #zb_bonfire_sale_timer {ns}.data -= #tick_delta {ns}.data
execute if score #zb_bonfire_sale_timer {ns}.data matches ..0 run bossbar remove {ns}:pu_bonfire_sale
execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. store result bossbar {ns}:pu_bonfire_sale value run scoreboard players get #zb_bonfire_sale_timer {ns}.data
""")

