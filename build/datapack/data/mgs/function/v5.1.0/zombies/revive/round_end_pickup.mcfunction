
#> mgs:v5.1.0/zombies/revive/round_end_pickup
#
# @executed	as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/revive/round_respawn [ as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] ]
#

# Is a live (non-downed) teammate standing within 10 blocks of MY body?
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
scoreboard players set #rv_pickup mgs.data 0
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..10] run scoreboard players set #rv_pickup mgs.data 1
execute if score #rv_pickup mgs.data matches 0 run return 0

# Picked up by the end of the round: full revive, inventory untouched
function mgs:v5.1.0/zombies/revive/revive_complete

