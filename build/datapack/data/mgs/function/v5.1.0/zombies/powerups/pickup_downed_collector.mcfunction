
#> mgs:v5.1.0/zombies/powerups/pickup_downed_collector
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/do_pickup
#

scoreboard players set #pu_downed_id mgs.data -1
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,distance=..1.5,sort=nearest,limit=1] run scoreboard players operation #pu_downed_id mgs.data = @s mgs.zb.downed_id
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] if score @s mgs.zb.downed_id = #pu_downed_id mgs.data run tag @s add mgs.pu_collecting

