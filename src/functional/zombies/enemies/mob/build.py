""" Building an enemy from a spawn's `mob` compound: summon, the map's nbt, round scaling, gun and riders. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_mob_build() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run where the enemy appears, with its compound in {ns}:temp _mob, its NoAI in _mob.no_ai and #zb_spawn_sid, #zb_spawn_x,
	## #zb_spawn_z naming its spawn. The arrival finds it tagged zb_new_root; riders come along on it.
	write_versioned_function("zombies/mob/spawn", f"""
function {ns}:v{version}/zombies/mob/summon with storage {ns}:temp _mob
tag @n[tag={ns}.zb_new] add {ns}.zb_new_root
scoreboard players set #zb_mob_root {ns}.data 1
execute as @n[tag={ns}.zb_new] run function {ns}:v{version}/zombies/mob/setup
""")

	write_versioned_function("zombies/mob/summon", f"""
# The marker passenger intercepts death before vanilla event 60 (poof particles), 17 ticks after the death with DeathTime -16.
# follow_range also sets the pathfinding region (range + 16) and node budget (range x 16); 40 keeps repaths cheap.
# step_height 1.0 makes 1-block rises walkable nodes instead of jump nodes that stall on stairs and slabs.
$summon $(entity) ~ ~ ~ {{Tags:["{ns}.zb_new"],NoAI:$(no_ai),DeathTime:-16s,PersistenceRequired:true,CanPickUpLoot:false,DeathLootTable:"minecraft:empty",Passengers:[{{id:"minecraft:marker",Tags:["{ns}.death_watch","{ns}.zombies_entity"],CustomName:"Death Watch"}}],attributes:[{{id:"minecraft:follow_range",base:40.0d}},{{id:"minecraft:step_height",base:1.0d}}]}}
""")

	## Run as the new enemy, where it appeared.
	write_versioned_function("zombies/mob/setup", f"""
tag @s remove {ns}.zb_new

# A zombie's or a wolf's own looks first, so the map's nbt can override them.
function {ns}:v{version}/zombies/mob/preset
execute if data storage {ns}:temp _mob.nbt run data modify entity @s {{}} merge from storage {ns}:temp _mob.nbt

# After the merge, which replaces the whole Tags list.
tag @s add {ns}.zombie_round
tag @s add {ns}.zombies_entity
tag @s add {ns}.nukable

# Allied with escort traders, so traders do not flee the horde and enemies do not attack them (see escort).
team join {ns}.horde @s

# Zonweeb types only replace a plain zombie: a spawn's own mob, without nbt, riders or gun, never on a special round.
scoreboard players set #zb_type {ns}.data 0
execute if score #zb_mob_root {ns}.data matches 1 if entity @s[type=minecraft:zombie] unless data storage {ns}:temp _mob.nbt unless data storage {ns}:temp _mob.riders[0] unless data storage {ns}:temp _mob.gun if data storage {ns}:zombies game{{variant:"zonweeb"}} unless score #zb_special_round {ns}.data matches 1 run function {ns}:v{version}/zombies/types/roll

# The round's health and speed, over whatever the nbt set.
function {ns}:v{version}/zombies/calc_zombie_hp
function {ns}:v{version}/zombies/apply_zombie_hp
function {ns}:v{version}/zombies/mob/speed
execute if score #zb_type {ns}.data matches 1.. run function {ns}:v{version}/zombies/types/apply

# Shown on the players' locator bar.
attribute @s minecraft:waypoint_transmit_range base set 256
waypoint modify @s color green

# The stuck rescue counts from here, and never sends it back to this spawn.
scoreboard players operation @s {ns}.zb.spawn.sid = #zb_spawn_sid {ns}.data
scoreboard players operation @s {ns}.zb.stuck_x = #zb_spawn_x {ns}.data
scoreboard players operation @s {ns}.zb.stuck_z = #zb_spawn_z {ns}.data
scoreboard players set @s {ns}.zb.stuck_dist 4
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data

execute if data storage {ns}:temp _mob.gun unless data storage {ns}:temp _mob{{gun:0b}} run function {ns}:v{version}/zombies/mob/arm
execute if data storage {ns}:temp _mob.riders[0] run function {ns}:v{version}/zombies/mob/riders
""")

	## The Missions gun AI with the duty cycle of Zonweeb armed zombies, 60 ticks firing then 40 resting.
	write_versioned_function("zombies/mob/arm", f"""
data modify storage {ns}:temp _arm set value {{active_time:60,sleep_time:40,prefix:""}}
data modify storage {ns}:temp _arm.entity set from storage {ns}:temp _mob.entity
data modify storage {ns}:temp _arm.prefix set string storage {ns}:temp _arm.entity 0 10
execute if data storage {ns}:temp _arm{{prefix:"minecraft:"}} run data modify storage {ns}:temp _arm.entity set string storage {ns}:temp _arm.entity 10

# The gun's level, else 1 for a named gun, else the round's tier.
execute store result storage {ns}:temp _arm.level int 1 run scoreboard players get #zb_level {ns}.data
execute if data storage {ns}:temp _mob.gun.id run data modify storage {ns}:temp _arm.level set value 1
execute if data storage {ns}:temp _mob.gun.level run data modify storage {ns}:temp _arm.level set from storage {ns}:temp _mob.gun.level
function {ns}:v{version}/mob/arm with storage {ns}:temp _arm

execute if data storage {ns}:temp _mob.gun.id run return run function {ns}:v{version}/zombies/mob/give_gun with storage {ns}:temp _mob.gun
function {ns}:v{version}/utils/random_weapon_no_explosive
""")
	write_versioned_function("zombies/mob/give_gun", f"""
$loot replace entity @s weapon.mainhand loot {ns}:i/$(id)
""")

	## Run as the mount, where it appeared: each rider is built like a spawn's own mob, then put on it.
	## Each mount pushes its list, so a rider's riders leave this one where it was.
	write_versioned_function("zombies/mob/riders", f"""
data modify storage {ns}:temp _riders prepend from storage {ns}:temp _mob.riders
function {ns}:v{version}/zombies/mob/rider
data remove storage {ns}:temp _riders[0]
""")
	write_versioned_function("zombies/mob/rider", f"""
data modify storage {ns}:temp _mob set from storage {ns}:temp _riders[0][0]
data remove storage {ns}:temp _riders[0][0]
data modify storage {ns}:temp _mob.no_ai set value 0b
execute unless data storage {ns}:temp _mob.entity run data modify storage {ns}:temp _mob.entity set value "zombie"

function {ns}:v{version}/zombies/mob/summon with storage {ns}:temp _mob
ride @n[tag={ns}.zb_new] mount @s
scoreboard players set #zb_mob_root {ns}.data 0
execute as @n[tag={ns}.zb_new] run function {ns}:v{version}/zombies/mob/setup

execute if data storage {ns}:temp _riders[0][0] run function {ns}:v{version}/zombies/mob/rider
""")

