
#> mgs:v5.0.0/multiplayer/gamemodes/dom/capture_blue
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/dom/point_tick
#

execute store result score #dom_prog mgs.data run scoreboard players get @s mgs.mp.dom_progress
scoreboard players remove @s mgs.mp.dom_progress 2

# Cap at -100
execute if score @s mgs.mp.dom_progress matches ..-101 run scoreboard players set @s mgs.mp.dom_progress -100

# If crossed 0, point neutralized
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_A] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_a_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_B] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_b_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_C] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_c_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_d_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_E] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_e_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run scoreboard players set @s mgs.mp.dom_owner 0
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "yellow"

# If reached -100, captured by blue
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_A] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_a","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_B] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_b","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_C] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_c","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_d","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_E] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_e","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 0.8
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "blue"
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run scoreboard players set @s mgs.mp.dom_owner 2

