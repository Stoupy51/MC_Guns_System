
#> mgs:v5.1.0/multiplayer/gamemodes/dom/capture_blue
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/dom/point_tick
#

execute store result score #dom_prog mgs.data run scoreboard players get @s mgs.mp.dom_progress
scoreboard players remove @s mgs.mp.dom_progress 2

# Cap at -100
execute if score @s mgs.mp.dom_progress matches ..-101 run scoreboard players set @s mgs.mp.dom_progress -100

# If crossed 0, point neutralized
tag @a remove mgs.dom_capturer
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run tag @a[distance=..5,scores={mgs.mp.team=2,mgs.mp.in_game=1}] add mgs.dom_capturer
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_a_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_a_neutralized","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_b_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_b_neutralized","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_c_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_c_neutralized","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_d_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_d_neutralized","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_e_neutralized","color":"yellow"}]
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.point_e_neutralized","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute as @a[tag=mgs.dom_capturer] run function mgs:v5.1.0/progression/mp/award_dom_neutralize
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run playsound minecraft:block.note_block.bass player @a ~ ~ ~ 1 0.5
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run scoreboard players set @s mgs.mp.dom_owner 0
execute if score #dom_prog mgs.data matches 1.. if score @s mgs.mp.dom_progress matches ..0 run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "yellow"

# If reached -100, captured by blue
tag @a remove mgs.dom_capturer
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run tag @a[distance=..5,scores={mgs.mp.team=2,mgs.mp.in_game=1}] add mgs.dom_capturer
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_a","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_a","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_b","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_b","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_c","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_c","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_d","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_d","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_e","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"}," ",{"translate":"mgs.captured_point_e","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute as @a[tag=mgs.dom_capturer] run function mgs:v5.1.0/progression/mp/award_dom_capture
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1 0.8
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "blue"
execute if score @s mgs.mp.dom_progress matches -100 unless score @s mgs.mp.dom_owner matches 2 run scoreboard players set @s mgs.mp.dom_owner 2
tag @a remove mgs.dom_capturer

