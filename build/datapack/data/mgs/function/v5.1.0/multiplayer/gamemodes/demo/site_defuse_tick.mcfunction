
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_defuse_tick
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/tick [ as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s ]
#

scoreboard players set #demo_ch mgs.data 0
execute if score @s mgs.demo_owner matches 1 store result score #demo_ch mgs.data if entity @a[scores={mgs.mp.team=2},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0]
execute if score @s mgs.demo_owner matches 2 store result score #demo_ch mgs.data if entity @a[scores={mgs.mp.team=1},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0]

# #demo_ch counts defusers and is only tested against zero.
execute if score #demo_ch mgs.data matches 0 run scoreboard players set @s mgs.demo_prog 0
execute if score #demo_ch mgs.data matches 1.. run scoreboard players operation @s mgs.demo_prog += #tick_delta mgs.data

# Only the defending side sees it, or an attacker crouched by their own bomb would read that they are defusing.
scoreboard players operation #demo_prog_shown mgs.data = @s mgs.demo_prog
execute if score #demo_ch mgs.data matches 1.. if score @s mgs.demo_owner matches 1 run title @a[scores={mgs.mp.team=2},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0] actionbar [{"translate":"mgs.defusing","color":"aqua"},{"score":{"name":"#demo_prog_shown","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.100"}]
execute if score #demo_ch mgs.data matches 1.. if score @s mgs.demo_owner matches 2 run title @a[scores={mgs.mp.team=1},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0] actionbar [{"translate":"mgs.defusing","color":"aqua"},{"score":{"name":"#demo_prog_shown","objective":"mgs.data"},"color":"yellow"},{"translate":"mgs.100"}]

execute if score @s mgs.demo_prog matches 100.. run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_defused

