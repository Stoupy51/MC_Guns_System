""" The machine animation: the weapon goes in, is processed, comes out and retreats. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG


# Functions
def write_pap_animation() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# BO1-style animation on a 300-tick countdown: slide in from 298 (2 ticks after summon, for client sync) to 281, inside 279-225 (cosmetics at 252),
	# slide out 219-206, collectible and glowing from 205, retreat 205-1, weapon lost at 0.

	write_versioned_function("zombies/pap/anim/start", f"""
# Run as the machine, at it; $(slot) is the player's weapon slot (hotbar.1 to hotbar.3).

execute positioned ~ ~-2 ~ positioned ~ ~0.8 ~ run summon minecraft:item_display ^ ^ ^0.6 {{Tags:["{ns}.pap_weapon_display","{ns}.gm_entity"],billboard:"fixed",item_display:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}}}}

data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] Rotation set from entity @s Rotation
$item replace entity @n[tag={ns}.pap_weapon_display,distance=..2] contents from entity @p[tag={ns}.pap_owner] $(slot)
$item replace entity @p[tag={ns}.pap_owner] $(slot) with minecraft:air

# Timeslip: this machine runs step 3 times per tick, so the display's slide interpolation is shortened to keep up.
scoreboard players set @s {ns}.zb.pap.timeslip 0
execute if score @p[tag={ns}.pap_owner] {ns}.special.timeslip matches 1 run scoreboard players set @s {ns}.zb.pap.timeslip 1
execute if score @s {ns}.zb.pap.timeslip matches 1 run data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] teleport_duration set value 7
execute unless score @s {ns}.zb.pap.timeslip matches 1 run data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] teleport_duration set value 20

execute store result storage {ns}:temp _pap_anim_slot.id int 1 run scoreboard players get @s {ns}.zb.pap.id
$data modify storage {ns}:temp _pap_anim_slot.slot set value "$(slot)"
function {ns}:v{version}/zombies/pap/anim/store_slot with storage {ns}:temp _pap_anim_slot

scoreboard players set @s {ns}.pap_anim 300

# Timeslip owners hear the 3x-speed jingle.
{ZombiesFeedback.zb_sound('pap_knuckle_crack')}
execute if score @s {ns}.zb.pap.timeslip matches 1 run {ZombiesFeedback.zb_sound('pap_jingle_sting_short')}
execute unless score @s {ns}.zb.pap.timeslip matches 1 run {ZombiesFeedback.zb_sound('pap_jingle_sting')}
""")

	# Weapon slot, keyed by machine id.
	write_versioned_function("zombies/pap/anim/store_slot", f"""
$data modify storage {ns}:zombies pap_anim_slot."$(id)" set value "$(slot)"
""")

	# Scope and camo, keyed by machine id, stored before the animation starts.
	write_versioned_function("zombies/pap/anim/store_cosmetics", f"""
$data modify storage {ns}:zombies pap_pending_cosmetics."$(id)" set from storage {ns}:temp _pap_cosm_store
""")

	write_versioned_function("zombies/pap/anim/fetch_cosmetics", f"""
$data modify storage {ns}:temp _pap_pending_cosmetics set from storage {ns}:zombies pap_pending_cosmetics."$(id)"
""")

	# Run as the machine.
	write_versioned_function("zombies/pap/anim/apply_cosmetics", f"""
execute store result storage {ns}:temp _pap_cosm_fetch.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/anim/fetch_cosmetics with storage {ns}:temp _pap_cosm_fetch
execute as @n[tag={ns}.pap_weapon_display,distance=..2] run function {ns}:v{version}/zombies/pap/anim/apply_cosmetics_to_display
""")

	write_versioned_function("zombies/pap/anim/apply_cosmetics_to_display", f"""
data modify entity @s item.components."minecraft:custom_data".{ns}.stats.models set from storage {ns}:temp _pap_pending_cosmetics.models
data remove entity @s item.components."minecraft:custom_data".{ns}.weapon
execute if data storage {ns}:temp _pap_pending_cosmetics.weapon run data modify entity @s item.components."minecraft:custom_data".{ns}.weapon set from storage {ns}:temp _pap_pending_cosmetics.weapon
data remove entity @s item.components."minecraft:custom_data".{ns}.stats.scope_level
execute if data storage {ns}:temp _pap_pending_cosmetics.scope_level run data modify entity @s item.components."minecraft:custom_data".{ns}.stats.scope_level set from storage {ns}:temp _pap_pending_cosmetics.scope_level
data modify storage {ns}:temp _pap_scope_model.slot set value "contents"
data modify storage {ns}:temp _pap_scope_model.model set from storage {ns}:temp _pap_pending_cosmetics.models.normal
function {ns}:v{version}/zombies/pap/set_item_model_from_scope with storage {ns}:temp _pap_scope_model
""")

	# Run as a machine with pap_anim >= 1.
	write_versioned_function("zombies/pap/anim/step", f"""
scoreboard players remove @s {ns}.pap_anim 1

execute if score @s {ns}.pap_anim matches 298 run function {ns}:v{version}/zombies/pap/anim/trigger_going_in

execute if score @s {ns}.pap_anim matches 281..297 run function {ns}:v{version}/zombies/pap/anim/going_in

execute if score @s {ns}.pap_anim matches 280 run function {ns}:v{version}/zombies/pap/anim/trigger_inside

execute if score @s {ns}.pap_anim matches 225..279 run function {ns}:v{version}/zombies/pap/anim/inside

execute if score @s {ns}.pap_anim matches 252 run function {ns}:v{version}/zombies/pap/anim/apply_cosmetics

execute if score @s {ns}.pap_anim matches 225 run function {ns}:v{version}/zombies/pap/anim/trigger_coming_out

execute if score @s {ns}.pap_anim matches 206..219 run function {ns}:v{version}/zombies/pap/anim/coming_out

execute if score @s {ns}.pap_anim matches 205 run function {ns}:v{version}/zombies/pap/anim/trigger_retreat
execute if score @s {ns}.pap_anim matches 205 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 185 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 165 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 145 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 125 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 105 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 85 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 65 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 45 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 25 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s {ns}.pap_anim matches 5 as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04

# Smoke and a looping sound every 20 ticks while retreating.
execute if score @s {ns}.pap_anim matches 1..205 positioned ~ ~-2 ~ run particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force @a[distance=..48]
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #20 {ns}.data
execute if score @s {ns}.pap_anim matches 1..205 if score #pap_t {ns}.data matches 0 run {ZombiesFeedback.zb_sound('pap_retreat_loop')}

execute if score @s {ns}.pap_anim matches 0 run function {ns}:v{version}/zombies/pap/anim/retreat_finish
""")

	write_versioned_function("zombies/pap/anim/trigger_going_in", f"""
execute as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.6
""")

	write_versioned_function("zombies/pap/anim/going_in", f"""
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #2 {ns}.data
execute if score #pap_t {ns}.data matches 0 positioned ~ ~-2 ~ run particle dust{{color:[0.565,0.0,1.0],scale:1.5}} ~ ~0.8 ~ 0.4 0.2 0.2 0 4 force @a[distance=..48]
""")

	write_versioned_function("zombies/pap/anim/trigger_inside", f"""
{ZombiesFeedback.zb_sound('pap_loop')}
{ZombiesFeedback.zb_sound('pap_upgrade')}
""")

	write_versioned_function("zombies/pap/anim/inside", f"""
execute positioned ~ ~-2 ~ run particle dust{{color:[0.565,0.0,1.0],scale:1.5}} ~ ~0.8 ~ 0.4 0.3 0.4 0 1 force @a[distance=..48]
execute positioned ~ ~-2 ~ run particle end_rod ~ ~0.8 ~ 0.3 0.2 0.3 0.05 1 force @a[distance=..48]

execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #20 {ns}.data
execute if score #pap_t {ns}.data matches 0 run {ZombiesFeedback.zb_sound('pap_loop')}
""")

	write_versioned_function("zombies/pap/anim/trigger_coming_out", f"""
execute as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^0.6
{ZombiesFeedback.zb_sound('pap_dispense')}
""")

	write_versioned_function("zombies/pap/anim/coming_out", """
execute positioned ~ ~-2 ~ run particle end_rod ~ ~0.8 ~ 0.4 0.3 0.3 0.05 3 force @a[distance=..48]
execute positioned ~ ~-2 ~ run particle dust{color:[0.565,0.0,1.0],scale:1.5} ~ ~1.0 ~ 0.4 0.3 0.4 0 2 force @a[distance=..48]
""")

	write_versioned_function("zombies/pap/anim/trigger_retreat", f"""
data merge entity @n[tag={ns}.pap_weapon_display,distance=..2] {{Glowing:true}}

# The retreat runs at 1x even on Timeslip machines and its slides are 20 ticks apart, so the
# 20-tick interpolation that anim/start shortened comes back.
data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] teleport_duration set value 20

execute positioned ~ ~-2 ~ run particle end_rod ~ ~1.0 ~ 0.5 0.3 0.5 0.1 20 force @a[distance=..48]
{ZombiesFeedback.zb_sound('pap_ready')}
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Weapon upgraded! Collect it before it retreats!","color":"aqua"}}]
""")

	# The weapon is lost: remove its display and restore the static one.
	write_versioned_function("zombies/pap/anim/retreat_finish", f"""
kill @e[tag={ns}.pap_weapon_display,distance=..2]

scoreboard players set @s {ns}.pap_anim -1

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The weapon was lost!","color":"red","bold":true}}]
{ZombiesFeedback.zb_sound('pap_deny')}

execute store result score #pap_mid {ns}.data run scoreboard players get @s {ns}.zb.pap.id
execute store result storage {ns}:temp _pap_retreat.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/retreat_cleanup with storage {ns}:temp _pap_retreat
""")

	# Clear the lost weapon's magazine and tracking data.
	write_versioned_function("zombies/pap/retreat_cleanup", f"""
$data modify storage {ns}:temp _pap_retreat.slot set from storage {ns}:zombies pap_anim_slot."$(id)"

execute as @a[scores={{{ns}.zb.pap_s=1..}}] if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run function {ns}:v{version}/zombies/pap/retreat_clear_owner

$data remove storage {ns}:zombies pap_anim_slot."$(id)"
""")

	# Run as the player who lost the weapon.
	write_versioned_function("zombies/pap/retreat_clear_owner", f"""
execute if data storage {ns}:temp _pap_retreat{{slot:"hotbar.1"}} run item replace entity @s inventory.1 with air
execute if data storage {ns}:temp _pap_retreat{{slot:"hotbar.2"}} run item replace entity @s inventory.2 with air
execute if data storage {ns}:temp _pap_retreat{{slot:"hotbar.3"}} run item replace entity @s inventory.3 with air

scoreboard players set @s {ns}.zb.pap_s 0
scoreboard players set @s {ns}.zb.pap_mid 0
""")

