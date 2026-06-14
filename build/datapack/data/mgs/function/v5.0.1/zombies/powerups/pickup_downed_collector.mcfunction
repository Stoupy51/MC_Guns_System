
#> mgs:v5.0.1/zombies/powerups/pickup_downed_collector
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/do_pickup
#

scoreboard players set #pu_downed_id mgs.data -1
execute as @e[tag=mgs.downed_mannequin,sort=nearest,limit=1,distance=..1.5] run scoreboard players operation #pu_downed_id mgs.data = @s mgs.zb.downed_id
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] if score @s mgs.zb.downed_id = #pu_downed_id mgs.data run tag @s add mgs.pu_collecting

