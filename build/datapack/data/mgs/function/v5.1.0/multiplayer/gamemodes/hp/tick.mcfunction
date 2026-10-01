
#> mgs:v5.1.0/multiplayer/gamemodes/hp/tick
#
# @within	mgs:v5.1.0/multiplayer/game_tick
#

scoreboard players operation #hp_rotate_timer mgs.data -= #tick_delta mgs.data
execute if score #hp_rotate_timer mgs.data matches ..0 run function mgs:v5.1.0/multiplayer/gamemodes/hp/rotate

scoreboard players operation #hp_rotate_sec mgs.data = #hp_rotate_timer mgs.data
scoreboard players operation #hp_rotate_sec mgs.data /= #20 mgs.data

# Every second.
execute if score #hp_score_timer mgs.data matches ..1 run function #bs.sidebar:refresh {objective:"mgs.sidebar"}

execute at @e[tag=mgs.hp_marker] run particle dust{color:[0.5,0.0,0.5],scale:1.5} ~ ~ ~ 4 0.5 4 0 10

# 5x5 horizontally, 4 vertically, centred on the marker.
tag @a remove mgs.in_hp_zone
execute at @e[tag=mgs.hp_marker] positioned ~-2.5 ~-1 ~-2.5 run tag @a[dx=4,dy=3,dz=4,gamemode=!spectator,scores={mgs.mp.in_game=1}] add mgs.in_hp_zone

execute store result score #hp_red mgs.data if entity @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1}]
execute store result score #hp_blue mgs.data if entity @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2}]

scoreboard players remove #hp_score_timer mgs.data 1
execute if score #hp_score_timer mgs.data matches ..0 run function mgs:v5.1.0/multiplayer/gamemodes/hp/score_tick
execute if score #hp_score_timer mgs.data matches ..0 run scoreboard players set #hp_score_timer mgs.data 20

