
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_plant_tick
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/tick [ as @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] & at @s ]
#

execute store result score #demo_ch_red mgs.data if entity @a[tag=mgs.demo_atk,scores={mgs.mp.team=1},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0]
execute store result score #demo_ch_blue mgs.data if entity @a[tag=mgs.demo_atk,scores={mgs.mp.team=2},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0]
scoreboard players set #demo_ch mgs.data 0
execute if score #demo_ch_red mgs.data matches 1.. if score #demo_ch_blue mgs.data matches 0 run scoreboard players set #demo_ch mgs.data 1
execute if score #demo_ch_blue mgs.data matches 1.. if score #demo_ch_red mgs.data matches 0 run scoreboard players set #demo_ch mgs.data 2

# A different team taking over restarts the plant from zero
execute unless score #demo_ch mgs.data = @s mgs.demo_owner run scoreboard players set @s mgs.demo_prog 0
scoreboard players operation @s mgs.demo_owner = #demo_ch mgs.data

# The += is here and NOT inside a per-player function, so a crowd plants no faster than one attacker
execute if score #demo_ch mgs.data matches 0 run scoreboard players set @s mgs.demo_prog 0
execute if score #demo_ch mgs.data matches 1.. run scoreboard players operation @s mgs.demo_prog += #tick_delta mgs.data

# Progress readout. Mirrored into a fake player first: a score component naming @s would be resolved in
# the recipient's context, not the site's.
scoreboard players operation #demo_prog_shown mgs.data = @s mgs.demo_prog
execute if score #demo_ch mgs.data matches 1.. run title @a[tag=mgs.demo_atk,predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0] actionbar [{"translate":"mgs.planting","color":"gold"},{"score":{"name":"#demo_prog_shown","objective":"mgs.data"},"color":"yellow"},{"text":"/50"}]

execute if score @s mgs.demo_prog matches 50.. run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_planted

