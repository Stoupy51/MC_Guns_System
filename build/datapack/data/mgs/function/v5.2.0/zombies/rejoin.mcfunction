
#> mgs:v5.2.0/zombies/rejoin
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/zombies/on_rejoin
#

execute if score #zb_freeze mgs.data matches 1.. run function mgs:v5.2.0/zombies/freeze_player
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s"},[{"text":" ","color":"green"}, {"translate":"mgs.is_back_in_the_game"}]]

