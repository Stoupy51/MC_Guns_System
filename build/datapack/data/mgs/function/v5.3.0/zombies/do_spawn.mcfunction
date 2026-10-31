
#> mgs:v5.3.0/zombies/do_spawn
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/spawn_from/zombies [ at @s ]
#			mgs:v5.3.0/zombies/spawn_from/special [ at @s ]
#

scoreboard players set #zb_spawned mgs.data 1
data modify storage mgs:temp _mob set from entity @s data.mob
scoreboard players operation #zb_spawn_sid mgs.data = @s mgs.zb.spawn.sid
execute store result score #zb_spawn_x mgs.data run data get entity @s Pos[0]
execute store result score #zb_spawn_z mgs.data run data get entity @s Pos[2]

execute if entity @s[tag=mgs.arrive_portal] run return run function mgs:v5.3.0/zombies/arrival/portal
execute if entity @s[tag=mgs.arrive_instant] run return run function mgs:v5.3.0/zombies/arrival/instant
execute if entity @s[tag=mgs.arrive_ceiling] run return run function mgs:v5.3.0/zombies/arrival/ceiling
function mgs:v5.3.0/zombies/arrival/floor

