""" The machine animation: the weapon goes in, is processed, comes out and retreats. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG


# Functions
def write_pap_animation() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# --- PAP Animation System (BO1-style, horizontal movement) ---
	# Timeline (240 ticks total, no rotation or size changes):
	# 240→221 (20t): GOING IN   — slide horizontally from ahead to center (2-tick wait after summon)
	# 220→161 (60t): INSIDE     — particles + periodic sound
	# 160→141 (20t): COMING OUT — slide horizontally from center to ahead
	# 140:           TRIGGER RETREAT — glowing weapon, starts retreat timer, allows collection
	# 139→1 (138t):  RETREAT    — weapon retreats back, still collectible
	# 0:             RETREAT FINISH — weapon destroyed (lost) (sound)

	# Spawn weapon item_display, transfer weapon, start animation timer.
	write_versioned_function("zombies/pap/anim/start", f"""
# @s = PAP machine entity, AT machine position
# $(slot) = player weapon slot (hotbar.1 / hotbar.2 / hotbar.3)

# Summon weapon item_display offset ahead of the machine (will slide to center)
execute positioned ~ ~-2 ~ positioned ~ ~0.8 ~ run summon minecraft:item_display ^ ^ ^0.6 {{Tags:["{ns}.pap_weapon_display","{ns}.gm_entity"],billboard:"fixed",item_display:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}}}}

# Transfer weapon into display entity via contents slot, then clear player slot
data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] Rotation set from entity @s Rotation
$item replace entity @n[tag={ns}.pap_weapon_display,distance=..2] contents from entity @p[tag={ns}.pap_owner] $(slot)
$item replace entity @p[tag={ns}.pap_owner] $(slot) with minecraft:air

# Timeslip: this PAP runs 3x faster (anim/step called 3x/tick). Flag the machine off the owner and
# shorten the display's slide interpolation so the going-in/coming-out/retreat slides keep up.
scoreboard players set @s {ns}.zb.pap.timeslip 0
execute if score @p[tag={ns}.pap_owner] {ns}.special.timeslip matches 1 run scoreboard players set @s {ns}.zb.pap.timeslip 1
execute if score @s {ns}.zb.pap.timeslip matches 1 run data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] teleport_duration set value 7
execute unless score @s {ns}.zb.pap.timeslip matches 1 run data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] teleport_duration set value 20

# Store this machine's slot for later retrieval when player collects the weapon
execute store result storage {ns}:temp _pap_anim_slot.id int 1 run scoreboard players get @s {ns}.zb.pap.id
$data modify storage {ns}:temp _pap_anim_slot.slot set value "$(slot)"
function {ns}:v{version}/zombies/pap/anim/store_slot with storage {ns}:temp _pap_anim_slot

# Start animation timer: 300 ticks total
scoreboard players set @s {ns}.pap_anim 300

# Sound: machine accepting weapon (Timeslip owners hear the 3x-speed jingle sting)
{ZombiesFeedback.zb_sound('pap_knuckle_crack')}
execute if score @s {ns}.zb.pap.timeslip matches 1 run {ZombiesFeedback.zb_sound('pap_jingle_sting_short')}
execute unless score @s {ns}.zb.pap.timeslip matches 1 run {ZombiesFeedback.zb_sound('pap_jingle_sting')}
""")

	# Persist weapon slot keyed by machine ID in zombies storage.
	write_versioned_function("zombies/pap/anim/store_slot", f"""
$data modify storage {ns}:zombies pap_anim_slot."$(id)" set value "$(slot)"
""")

	# Persist scope+camo cosmetics keyed by machine ID (called before animation starts).
	write_versioned_function("zombies/pap/anim/store_cosmetics", f"""
$data modify storage {ns}:zombies pap_pending_cosmetics."$(id)" set from storage {ns}:temp _pap_cosm_store
""")

	# Fetch scope+camo cosmetics for this machine into temp storage.
	write_versioned_function("zombies/pap/anim/fetch_cosmetics", f"""
$data modify storage {ns}:temp _pap_pending_cosmetics set from storage {ns}:zombies pap_pending_cosmetics."$(id)"
""")

	# Apply stored scope+camo cosmetics to the weapon display entity (runs as machine).
	write_versioned_function("zombies/pap/anim/apply_cosmetics", f"""
execute store result storage {ns}:temp _pap_cosm_fetch.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/anim/fetch_cosmetics with storage {ns}:temp _pap_cosm_fetch
execute as @n[tag={ns}.pap_weapon_display,distance=..2] run function {ns}:v{version}/zombies/pap/anim/apply_cosmetics_to_display
""")

	# Apply scope+camo data from temp storage to the item in this display entity.
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

	# Main per-machine tick dispatcher (runs as machine when pap_anim >= 1).
	write_versioned_function("zombies/pap/anim/step", f"""
# Decrement timer
scoreboard players remove @s {ns}.pap_anim 1

# Trigger: start going-in interpolation (2 ticks after summon for client sync)
execute if score @s {ns}.pap_anim matches 298 run function {ns}:v{version}/zombies/pap/anim/trigger_going_in

# Phase: GOING IN (timer 281..297)
execute if score @s {ns}.pap_anim matches 281..297 run function {ns}:v{version}/zombies/pap/anim/going_in

# Trigger: weapon fully in at timer=280 — start inside processing
execute if score @s {ns}.pap_anim matches 280 run function {ns}:v{version}/zombies/pap/anim/trigger_inside

# Phase: INSIDE (timer 225..279)
execute if score @s {ns}.pap_anim matches 225..279 run function {ns}:v{version}/zombies/pap/anim/inside

# Trigger: apply scope+camo cosmetics at midpoint of inside phase (timer=252)
execute if score @s {ns}.pap_anim matches 252 run function {ns}:v{version}/zombies/pap/anim/apply_cosmetics

# Trigger: start coming-out interpolation at timer=225
execute if score @s {ns}.pap_anim matches 225 run function {ns}:v{version}/zombies/pap/anim/trigger_coming_out

# Phase: COMING OUT (timer 206..219)
execute if score @s {ns}.pap_anim matches 206..219 run function {ns}:v{version}/zombies/pap/anim/coming_out

# Trigger: weapon fully emerged at timer=205 — start retreat, allow collection
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

# Phase: RETREAT (timer 1..205) — smoke particles + looping sound every 20 ticks
execute if score @s {ns}.pap_anim matches 1..205 positioned ~ ~-2 ~ run particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force @a[distance=..48]
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #20 {ns}.data
execute if score @s {ns}.pap_anim matches 1..205 if score #pap_t {ns}.data matches 0 run {ZombiesFeedback.zb_sound('pap_retreat_loop')}

# Retreat finished at timer=0 — weapon is lost
execute if score @s {ns}.pap_anim matches 0 run function {ns}:v{version}/zombies/pap/anim/retreat_finish
""")

	# New function: start going-in interpolation 2 ticks after summon (client sync).
	write_versioned_function("zombies/pap/anim/trigger_going_in", f"""
# Slide weapon from ahead ^0.5 to center over 30 ticks (no rotation/size changes)
execute as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.6
""")

	# Sparse purple particles during the going-in phase (horizontal slide).
	write_versioned_function("zombies/pap/anim/going_in", f"""
# Sparse purple dust every 2 ticks along the horizontal path
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #2 {ns}.data
execute if score #pap_t {ns}.data matches 0 positioned ~ ~-2 ~ run particle dust{{color:[0.565,0.0,1.0],scale:1.5}} ~ ~0.8 ~ 0.4 0.2 0.2 0 4 force @a[distance=..48]
""")

	# Trigger inside processing (weapon already at center, no transformation change needed).
	write_versioned_function("zombies/pap/anim/trigger_inside", f"""
{ZombiesFeedback.zb_sound('pap_loop')}
{ZombiesFeedback.zb_sound('pap_upgrade')}
""")

	# Dense particles and sounds while the weapon is being processed inside the machine.
	write_versioned_function("zombies/pap/anim/inside", f"""
# Dense purple dust + end_rod particles every tick
execute positioned ~ ~-2 ~ run particle dust{{color:[0.565,0.0,1.0],scale:1.5}} ~ ~0.8 ~ 0.4 0.3 0.4 0 1 force @a[distance=..48]
execute positioned ~ ~-2 ~ run particle end_rod ~ ~0.8 ~ 0.3 0.2 0.3 0.05 1 force @a[distance=..48]

# Periodic processing sound every 20 ticks
execute store result score #pap_t {ns}.data run scoreboard players get @s {ns}.pap_anim
scoreboard players operation #pap_t {ns}.data %= #20 {ns}.data
execute if score #pap_t {ns}.data matches 0 run {ZombiesFeedback.zb_sound('pap_loop')}
""")

	# Trigger coming-out interpolation: slide horizontally out over 30 ticks.
	write_versioned_function("zombies/pap/anim/trigger_coming_out", f"""
# Slide weapon horizontally out to the left over 30 ticks (no rotation/size changes)
execute as @n[tag={ns}.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^0.6
{ZombiesFeedback.zb_sound('pap_dispense')}
""")

	# End_rod and purple particles during the coming-out phase.
	write_versioned_function("zombies/pap/anim/coming_out", """
execute positioned ~ ~-2 ~ run particle end_rod ~ ~0.8 ~ 0.4 0.3 0.3 0.05 3 force @a[distance=..48]
execute positioned ~ ~-2 ~ run particle dust{color:[0.565,0.0,1.0],scale:1.5} ~ ~1.0 ~ 0.4 0.3 0.4 0 2 force @a[distance=..48]
""")

	# Trigger: weapon fully emerged — start slow retreat (BO style).
	# Timer stays positive: 119→1 retreat, 0 = finish.
	write_versioned_function("zombies/pap/anim/trigger_retreat", f"""
# Weapon glows while collectible, start retreat: slide back to center over 119 ticks (no rotation/size changes)
data merge entity @n[tag={ns}.pap_weapon_display,distance=..2] {{Glowing:true}}

# Retreat runs at the normal 1x rate even for Timeslip machines (only the upgrade is sped up), and
# its slides are 20 real ticks apart — restore the full 20-tick interpolation so the retreat glides
# smoothly (anim/start shortens it to 7 for the sped-up upgrade slides on Timeslip machines)
data modify entity @n[tag={ns}.pap_weapon_display,distance=..2] teleport_duration set value 20

# Sound + particle burst
execute positioned ~ ~-2 ~ run particle end_rod ~ ~1.0 ~ 0.5 0.3 0.5 0.1 20 force @a[distance=..48]
{ZombiesFeedback.zb_sound('pap_ready')}
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Weapon upgraded! Collect it before it retreats!","color":"aqua"}}]
""")

	# Retreat finished: weapon is LOST — destroy display, restore static display.
	write_versioned_function("zombies/pap/anim/retreat_finish", f"""
# Weapon is lost — destroy it (not dropped)
kill @e[tag={ns}.pap_weapon_display,distance=..2]

# Reset to idle
scoreboard players set @s {ns}.pap_anim -1

# Notify and sound
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The weapon was lost!","color":"red","bold":true}}]
{ZombiesFeedback.zb_sound('pap_deny')}

# Clean up orphaned magazine and PAP tracking for the owner
execute store result score #pap_mid {ns}.data run scoreboard players get @s {ns}.zb.pap.id
execute store result storage {ns}:temp _pap_retreat.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/retreat_cleanup with storage {ns}:temp _pap_retreat
""")

	# Clean up orphaned magazine and tracking data when weapon is lost.
	write_versioned_function("zombies/pap/retreat_cleanup", f"""
# Get the stored slot for this machine
$data modify storage {ns}:temp _pap_retreat.slot set from storage {ns}:zombies pap_anim_slot."$(id)"

# Find owner by matching PAP machine ID and clear their orphaned magazine
execute as @a[scores={{{ns}.zb.pap_s=1..}}] if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run function {ns}:v{version}/zombies/pap/retreat_clear_owner

# Clean stored slot data
$data remove storage {ns}:zombies pap_anim_slot."$(id)"
""")

	# Clear orphaned magazine from the player who lost their weapon (runs as player).
	write_versioned_function("zombies/pap/retreat_clear_owner", f"""
# Clear the orphaned magazine from the corresponding inventory slot
execute if data storage {ns}:temp _pap_retreat{{slot:"hotbar.1"}} run item replace entity @s inventory.1 with air
execute if data storage {ns}:temp _pap_retreat{{slot:"hotbar.2"}} run item replace entity @s inventory.2 with air
execute if data storage {ns}:temp _pap_retreat{{slot:"hotbar.3"}} run item replace entity @s inventory.3 with air

# Reset PAP tracking scores
scoreboard players set @s {ns}.zb.pap_s 0
scoreboard players set @s {ns}.zb.pap_mid 0
""")

