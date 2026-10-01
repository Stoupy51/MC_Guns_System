""" Bossbar upkeep for the timed power-ups and the game hooks that drive it. """
# Imports
from stewbeet import Mem, write_versioned_function

from .types import TIMED_POWERUPS, pu_snd


# Functions
def write_powerup_bossbars() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# One bossbar update function per TIMED_POWERUPS entry.
	for pu_id, v in TIMED_POWERUPS.items():
		scoreboard: str   = v.scoreboard
		bossbar_id: str   = v.bossbar_id
		# The end sound plays once, when the effect expires.
		end_sound_line: str = ""
		if v.end_sound:
			end_sound: str = pu_snd(ns, v.end_sound, at_s=True)
			end_sound_line = f"execute if score #pu_prev_{pu_id} {ns}.data matches 1.. if score #pu_max_duration {ns}.data matches ..0 {end_sound}\n"
		write_versioned_function(f"zombies/powerups/update_{pu_id}_bb", f"""
# Longest remaining duration across the players who have it.
scoreboard players set #pu_max_duration {ns}.data 0
scoreboard players operation #pu_max_duration {ns}.data > @a[scores={{{ns}.special.{scoreboard}=1..}}] {ns}.special.{scoreboard}

# Inactive now and last tick: nothing to do.
execute if score #pu_max_duration {ns}.data matches ..0 if score #pu_prev_{pu_id} {ns}.data matches ..0 run return 0

execute if score #pu_max_duration {ns}.data matches ..0 run bossbar remove {ns}:{bossbar_id}
execute if score #pu_max_duration {ns}.data matches 1.. store result bossbar {ns}:{bossbar_id} value run scoreboard players get #pu_max_duration {ns}.data
{end_sound_line}scoreboard players operation #pu_prev_{pu_id} {ns}.data = #pu_max_duration {ns}.data
""")

	## Run on state transitions only (tag-gated from game_tick).
	write_versioned_function("zombies/powerups/insta_kill_melee_on", f"""
# Remove then add, so a stale modifier left by a crash cannot stack.
attribute @s minecraft:attack_damage modifier remove {ns}:insta_kill
attribute @s minecraft:attack_damage modifier add {ns}:insta_kill 100000 add_value
tag @s add {ns}.ik_melee
""")
	write_versioned_function("zombies/powerups/insta_kill_melee_off", f"""
attribute @s minecraft:attack_damage modifier remove {ns}:insta_kill
tag @s remove {ns}.ik_melee
""")

	bb_update_calls: str = "\n".join(
		f"function {ns}:v{version}/zombies/powerups/update_{pu_id}_bb"
		for pu_id in TIMED_POWERUPS
	)

	decrement_calls: str = "\n".join(
		f"execute as @a[scores={{{ns}.special.{v.scoreboard}=1..}}] run scoreboard players operation @s {ns}.special.{v.scoreboard} -= #tick_delta {ns}.data"
		for k, v in TIMED_POWERUPS.items()
		if k not in ("insta_kill", "unlimited_ammo") # They are already handled globally (not zombies)
	)

	write_versioned_function("zombies/game_tick", f"""
# #pu_active (kept on spawn, expire and pickup) gates the two scans below. Resynced every 40 ticks as a safety net:
# pu_item is Invulnerable and only dies through tracked paths.
execute store result score #pu_active_phase {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #pu_active_phase {ns}.data %= #40 {ns}.data
execute if score #pu_active_phase {ns}.data matches 0 store result score #pu_active {ns}.data if entity @e[type=minecraft:item,tag={ns}.pu_item]

execute if score #pu_active {ns}.data matches 1.. as @e[type=minecraft:item,tag={ns}.pu_item] at @s run function {ns}:v{version}/zombies/powerups/entity_tick

# A text_display whose item burned or exploded is never removed by expire or pickup.
execute if score #pu_active {ns}.data matches 1.. as @e[type=minecraft:text_display,tag={ns}.pu_text] at @s unless entity @e[type=minecraft:item,tag={ns}.pu_item,distance=..4] run kill @s

# Insta Kill also works with the knife through a huge melee damage modifier (guns insta-kill in the raycast).
# The ik_melee tag marks who carries it, so the attribute commands only run on transitions.
execute as @a[tag=!{ns}.ik_melee,scores={{{ns}.special.instant_kill=1..}}] run function {ns}:v{version}/zombies/powerups/insta_kill_melee_on
execute as @a[tag={ns}.ik_melee,scores={{{ns}.special.instant_kill=..0}}] run function {ns}:v{version}/zombies/powerups/insta_kill_melee_off

# Toggles every 4 ticks, BO2's 0.4 s blink cycle.
scoreboard players add #zb_blink_counter {ns}.data 1
execute if score #zb_blink_counter {ns}.data matches 4.. run scoreboard players set #zb_blink_counter {ns}.data 0
execute if score #zb_blink_counter {ns}.data matches 0 run scoreboard players add #zb_blink_state {ns}.data 1
execute if score #zb_blink_state {ns}.data matches 2.. run scoreboard players set #zb_blink_state {ns}.data 0

{decrement_calls}

{bb_update_calls}

execute if score #zb_fire_sale_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/powerups/fire_sale_tick

execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/powerups/bonfire_sale_tick
""")

	stop_scoreboard_resets: str = "\n".join(
		f"scoreboard players set @a {ns}.special.{v.scoreboard} 0"
		for v in TIMED_POWERUPS.values()
	)
	stop_bossbar_removes: str = "\n".join(
		f"bossbar remove {ns}:{v.bossbar_id}"
		for v in TIMED_POWERUPS.values()
	)

	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:item,tag={ns}.pu_item]
kill @e[type=minecraft:text_display,tag={ns}.pu_text]
scoreboard players set #pu_active {ns}.data 0
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_cycle_done {ns}.data 0
scoreboard players set #zb_cycle_len {ns}.data 0
{stop_scoreboard_resets}
data modify storage {ns}:data _pu_queue set value []

# Also stops the song.
scoreboard players set #zb_fire_sale_timer {ns}.data 0
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0
bossbar remove {ns}:pu_fire_sale
stopsound @a ambient {ns}:zombies/powerups/fire_sale_song
tag @e remove {ns}.mb_fs_active
tag @e remove {ns}.mb_orig_active
kill @e[tag={ns}.mb_temp]

scoreboard players set #zb_bonfire_sale_timer {ns}.data 0
bossbar remove {ns}:pu_bonfire_sale

{stop_bossbar_removes}
""")

	write_versioned_function("zombies/start_round", f"""
scoreboard players set #zb_drops_this_round {ns}.data 0
scoreboard players set #zb_cycle_done {ns}.data 0

# A fresh shuffle bag the size of one full drop cycle.
function {ns}:v{version}/zombies/powerups/queue_refill
execute store result score #zb_cycle_len {ns}.data run data get storage {ns}:data _pu_queue
""")

	write_versioned_function("zombies/check_kill_points", f"""
# Double Points pays the kill points again.
execute if score @s {ns}.special.double_points matches 1.. run scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data
""")

	write_versioned_function("zombies/on_hit_signal", f"""
execute if score @n[tag={ns}.ticking] {ns}.special.double_points matches 1.. run scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""")

