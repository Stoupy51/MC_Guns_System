
#> mgs:v5.3.0/zombies/mob/setup
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/spawn [ as @n[tag=mgs.zb_new] ]
#			mgs:v5.3.0/zombies/mob/rider [ as @n[tag=mgs.zb_new] ]
#

tag @s remove mgs.zb_new

# A zombie's or a wolf's own looks first, so the map's nbt can override them.
function mgs:v5.3.0/zombies/mob/preset
execute if data storage mgs:temp _mob.nbt run data modify entity @s {} merge from storage mgs:temp _mob.nbt

# After the merge, which replaces the whole Tags list.
tag @s add mgs.zombie_round
tag @s add mgs.zombies_entity
tag @s add mgs.nukable

# Allied with escort traders, so traders do not flee the horde and enemies do not attack them (see escort).
team join mgs.horde @s

# Zonweeb types only replace a plain zombie: a spawn's own mob, without nbt, riders or gun, never on a special round.
scoreboard players set #zb_type mgs.data 0
execute if score #zb_mob_root mgs.data matches 1 if entity @s[type=minecraft:zombie] unless data storage mgs:temp _mob.nbt unless data storage mgs:temp _mob.riders[0] unless data storage mgs:temp _mob.gun if data storage mgs:zombies game{variant:"zonweeb"} unless score #zb_special_round mgs.data matches 1 run function mgs:v5.3.0/zombies/types/roll

# The round's health and speed, over whatever the nbt set.
function mgs:v5.3.0/zombies/calc_zombie_hp
function mgs:v5.3.0/zombies/apply_zombie_hp
function mgs:v5.3.0/zombies/mob/speed
execute if score #zb_type mgs.data matches 1.. run function mgs:v5.3.0/zombies/types/apply

# Shown on the players' locator bar.
attribute @s minecraft:waypoint_transmit_range base set 256
waypoint modify @s color green

# The stuck rescue counts from here, and never sends it back to this spawn.
scoreboard players operation @s mgs.zb.spawn.sid = #zb_spawn_sid mgs.data
scoreboard players operation @s mgs.zb.stuck_x = #zb_spawn_x mgs.data
scoreboard players operation @s mgs.zb.stuck_z = #zb_spawn_z mgs.data
scoreboard players set @s mgs.zb.stuck_dist 4
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

execute if data storage mgs:temp _mob.gun unless data storage mgs:temp _mob{gun:0b} run function mgs:v5.3.0/zombies/mob/arm
execute if data storage mgs:temp _mob.riders[0] run function mgs:v5.3.0/zombies/mob/riders

