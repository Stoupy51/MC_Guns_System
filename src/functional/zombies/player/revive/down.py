""" Going down: spawning the mannequin, its name HUD and the teleport macros. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from ....helpers.titles import TitleTimes
from .shared import BLEED_OUT_TICKS, HUD_OFFSET_Y_THOUSANDTHS


# Functions
def write_going_down() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Run from on_respawn when a player dies in zombies.
	write_versioned_function("zombies/revive/on_down", f"""
# Dying Wish first: off cooldown, it replaces going down with a berserk. Must stay above Who's Who.
execute if score @s {ns}.zb.perk.dying_wish matches 1 if score @s {ns}.zb.dw_cd matches ..0 run return run function {ns}:v{version}/zombies/perks/dying_wish_trigger

# A doppelganger going down again forfeits their unrevived body first (BO2 rule), then goes down normally
# (or as a fresh Who's Who if they rebought it).
execute if entity @s[tag={ns}.ww_active] run function {ns}:v{version}/zombies/whos_who/forfeit

# Who's Who: play on as a doppelganger with a pistol while the body waits for a revive, solo or co-op.
# It sits above the solo Quick Revive and Tombstone paths, so it wins over both.
execute if score @s {ns}.zb.perk.whos_who matches 1 run return run function {ns}:v{version}/zombies/whos_who/on_down

scoreboard players set @s {ns}.zb.downed 1
scoreboard players set @s {ns}.zb.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.revive_p 0
tag @s add {ns}.downed_spectator

# on_respawn already set it to 0.
scoreboard players set @s {ns}.mp.death_count 0

# Unique downed id, then the revivable body (mannequin and name HUD) at the death spot.
scoreboard players add #downed_id_next {ns}.data 1
scoreboard players operation @s {ns}.zb.downed_id = #downed_id_next {ns}.data
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/revive/spawn_downed_body

# Electric Cherry: a full-strength discharge (used == cap == 1) before the perk is stripped (BO behaviour).
scoreboard players set #ec_used {ns}.data 1
scoreboard players set #ec_cap {ns}.data 1
execute if score @s {ns}.special.electric_cherry matches 1 at @s run function {ns}:v{version}/zombies/perks/electric_cherry_shock

# Tombstone: snapshot the perks before they are stripped. Never reached by a Who's Who down.
execute if score @s {ns}.zb.perk.tombstone matches 1 run function {ns}:v{version}/zombies/perks/tombstone_on_down

# Solo Quick Revive: snapshot ownership before lose_all strips the perk, since the auto-revive runs a tick later
# from downed_tick. Recomputed on every down.
tag @s remove {ns}.zb_qr_armed
execute if entity @s[tag={ns}.perk.quick_revive] run tag @s add {ns}.zb_qr_armed

function {ns}:v{version}/zombies/perks/lose_all

gamemode spectator @s

# The spectator rides this item_display for a locked third-person view.
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.downed_cam","{ns}.downed_cam_new","{ns}.gm_entity"],teleport_duration:1}}

scoreboard players operation @n[tag={ns}.downed_cam_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

# Id-matched, since with Who's Who bodies around the nearest mannequin can be someone else's.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run tp @n[tag={ns}.downed_cam_new] ^ ^2 ^-3
tag @e[tag={ns}.downed_cam_new] remove {ns}.downed_cam_new

execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tag @s add {ns}.downed_mine_temp
ride @s mount @n[tag={ns}.downed_mine_temp]
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

{TitleTimes.BAD_NEWS.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"You are down! A teammate can revive you.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="red")},{{"text":" is down!","color":"gray"}}]
""")

	## Spawn the revivable body of @s (mannequin with armor and skin, name HUD), for a normal down and Who's Who; needs a fresh downed_id, leaves the position in temp rv_x, rv_y, rv_z.
	## {ns}:temp _body_at ([x, y, z]) overrides LastDeathLocation, for the out-of-bounds revive.
	write_versioned_function("zombies/revive/spawn_downed_body", f"""
execute unless data storage {ns}:temp _body_at run data modify storage {ns}:temp _body_at set from entity @s LastDeathLocation.pos

# Full float precision: x1000, stored back as double 0.001.
execute store result score #rv_y_raw {ns}.data run data get storage {ns}:temp _body_at[1] 1000
scoreboard players add #rv_y_raw {ns}.data {HUD_OFFSET_Y_THOUSANDTHS}
execute store result storage {ns}:temp rv_x double 0.001 run data get storage {ns}:temp _body_at[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get storage {ns}:temp _body_at[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get storage {ns}:temp _body_at[2] 1000
execute store result storage {ns}:temp rv_y_hud double 0.001 run scoreboard players get #rv_y_raw {ns}.data
data remove storage {ns}:temp _body_at

# Glowing, so the squad finds a body on the floor in a horde before it bleeds out.
summon minecraft:mannequin ~ ~1.5 ~ {{Invulnerable:1b,Glowing:1b,pose:"swimming",hide_description:true,Tags:["{ns}.downed_mannequin","{ns}.downed_new","{ns}.gm_entity"]}}

scoreboard players operation @n[tag={ns}.downed_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

data modify entity @n[tag={ns}.downed_new] equipment set from entity @s equipment

# The get_username loot table gives a player_head with the profile, for the skin.
loot replace entity @n[tag={ns}.downed_new] weapon.mainhand loot {ns}:get_username
data modify entity @n[tag={ns}.downed_new] profile set from entity @n[tag={ns}.downed_new] equipment.mainhand.components."minecraft:profile"

# Take the name from the profile: on_down runs at the shared respawn point, so a nearest-spectator
# selector would give the same player to every down of the same tick.
data modify storage {ns}:temp rv_name set from entity @n[tag={ns}.downed_new] equipment.mainhand.components."minecraft:profile".name
execute unless data storage {ns}:temp rv_name run data modify storage {ns}:temp rv_name set value "???"
item replace entity @n[tag={ns}.downed_new] weapon.mainhand with minecraft:air

# see_through, so the name reads through walls and zombies.
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.downed_hud","{ns}.downed_hud_new","{ns}.gm_entity"],billboard:"vertical",shadow:1b,see_through:1b,teleport_duration:1,transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},text:[{{"text":"...","color":"yellow"}},{{"text":" ↓","color":"yellow"}}]}}
function {ns}:v{version}/zombies/revive/set_hud_name with storage {ns}:temp

scoreboard players operation @n[tag={ns}.downed_hud_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

function {ns}:v{version}/zombies/revive/tp_to_death with storage {ns}:temp

tag @e[tag={ns}.downed_new] remove {ns}.downed_new
tag @e[tag={ns}.downed_hud_new] remove {ns}.downed_hud_new
""")

	## Player names only hold [A-Za-z0-9_].
	write_versioned_function("zombies/revive/set_hud_name", f"""
$data modify entity @n[tag={ns}.downed_hud_new] text set value [{{"text":"$(rv_name)","color":"yellow"}},{{"text":" ↓","color":"yellow"}}]
""")

	write_versioned_function("zombies/revive/tp_to_death", f"""
$tp @n[tag={ns}.downed_new] $(rv_x) $(rv_y) $(rv_z)
$tp @n[tag={ns}.downed_hud_new] $(rv_x) $(rv_y_hud) $(rv_z)
""")

	write_versioned_function("zombies/revive/tp_revive_pos", """
$tp @s $(rv_x) $(rv_y) $(rv_z)
""")

