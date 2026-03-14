
#> mgs:v5.0.0/multiplayer/gamemodes/dom/capture_red
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/point_tick
#

# Get current progress
execute store result score #dom_prog mgs.data run scoreboard players get @s mgs.mp.dom_progress

# Increase progress (2 per tick when capturing)
scoreboard players add @s mgs.mp.dom_progress 2

# Cap at 100
execute if score @s mgs.mp.dom_progress matches 101.. run scoreboard players set @s mgs.mp.dom_progress 100

# If crossed 0 from negative (was blue, now contested), briefly neutral
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.domination_point_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run scoreboard players set @s mgs.mp.dom_owner 0
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "yellow"

# If reached 100, captured by red
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"}," ",{"translate":"mgs.captured_a_point","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 1.2
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "red"
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run scoreboard players set @s mgs.mp.dom_owner 1

