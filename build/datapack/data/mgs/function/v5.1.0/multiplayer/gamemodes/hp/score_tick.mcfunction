
#> mgs:v5.1.0/multiplayer/gamemodes/hp/score_tick
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/hp/tick
#

# Only score if one team exclusively holds the zone (not contested)
# Red alone in zone
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. at @e[tag=mgs.hp_marker] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. run scoreboard players add #red mgs.mp.team 1

# Blue alone in zone
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. at @e[tag=mgs.hp_marker] run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. run scoreboard players add #blue mgs.mp.team 1

# First side to hold this hill after it rotated
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. if score #hp_xp_captured mgs.data matches 0 run tellraw @a[tag=!mgs.in_hp_zone] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🎯 ",{"translate":"mgs.hardpoint_captured","color":"gold"}]
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. if score #hp_xp_captured mgs.data matches 0 run tellraw @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🎯 ",{"translate":"mgs.hardpoint_captured","color":"gold"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. if score #hp_xp_captured mgs.data matches 0 run tellraw @a[tag=!mgs.in_hp_zone] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🎯 ",{"translate":"mgs.hardpoint_captured","color":"gold"}]
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. if score #hp_xp_captured mgs.data matches 0 run tellraw @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🎯 ",{"translate":"mgs.hardpoint_captured","color":"gold"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. if score #hp_xp_captured mgs.data matches 0 as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_hp_capture
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. if score #hp_xp_captured mgs.data matches 0 as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_hp_capture
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. run scoreboard players set #hp_xp_captured mgs.data 1
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. run scoreboard players set #hp_xp_captured mgs.data 1

# Holding it, once every 5s. No message: the bar moving is the feedback.
scoreboard players remove #hp_xp_hold mgs.data 1
execute if score #hp_red mgs.data matches 1.. unless score #hp_blue mgs.data matches 1.. if score #hp_xp_hold mgs.data matches ..0 as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_hp_hold
execute if score #hp_blue mgs.data matches 1.. unless score #hp_red mgs.data matches 1.. if score #hp_xp_hold mgs.data matches ..0 as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_hp_hold
execute if score #hp_xp_hold mgs.data matches ..0 run scoreboard players set #hp_xp_hold mgs.data 5

# Check win
function mgs:v5.1.0/multiplayer/check_team_win

