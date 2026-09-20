
#> mgs:v5.1.0/zombies/dog_max_ammo_at_self
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/dog_death
#

scoreboard players set #zb_dog_ammo_done mgs.data 1
scoreboard players add #pu_uid mgs.data 1
data modify storage mgs:temp _pu_spawn set value {x:0,y:0,z:0,uid:0,type:"max_ammo"}
execute at @s summon minecraft:marker run function mgs:v5.1.0/shared/probe_pos
data modify storage mgs:temp _pu_spawn.x set from storage mgs:temp _probe_pos[0]
data modify storage mgs:temp _pu_spawn.y set from storage mgs:temp _probe_pos[1]
data modify storage mgs:temp _pu_spawn.z set from storage mgs:temp _probe_pos[2]
execute store result storage mgs:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid mgs.data
function mgs:v5.1.0/zombies/powerups/spawn_display with storage mgs:temp _pu_spawn

