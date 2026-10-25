
#> mgs:v5.3.0/multiplayer/gamemodes/dom/capture_red
#
# @executed	at @s
#
# @within	mgs:v5.3.0/multiplayer/gamemodes/dom/point_tick
#

execute store result score #dom_prog mgs.data run scoreboard players get @s mgs.mp.dom_progress
scoreboard players add @s mgs.mp.dom_progress 2

execute if score @s mgs.mp.dom_progress matches 101.. run scoreboard players set @s mgs.mp.dom_progress 100

# Crossing 0 neutralizes the point.
tag @a remove mgs.dom_capturer
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run tag @a[distance=..5,scores={mgs.mp.team=1,mgs.mp.in_game=1}] add mgs.dom_capturer
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_a_neutralized","fallback":"Point A neutralized!","color":"yellow"}]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_a_neutralized","fallback":"Point A neutralized!","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_b_neutralized","fallback":"Point B neutralized!","color":"yellow"}]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_b_neutralized","fallback":"Point B neutralized!","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_c_neutralized","fallback":"Point C neutralized!","color":"yellow"}]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_c_neutralized","fallback":"Point C neutralized!","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_d_neutralized","fallback":"Point D neutralized!","color":"yellow"}]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_d_neutralized","fallback":"Point D neutralized!","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_e_neutralized","fallback":"Point E neutralized!","color":"yellow"}]
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.point_e_neutralized","fallback":"Point E neutralized!","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
execute as @a[tag=mgs.dom_capturer] run function mgs:v5.3.0/progression/mp/award_dom_neutralize
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run playsound minecraft:block.note_block.bass player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 0.5
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run scoreboard players set @s mgs.mp.dom_owner 0
execute if score #dom_prog mgs.data matches ..-1 if score @s mgs.mp.dom_progress matches 0.. run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "yellow"

tag @a remove mgs.dom_capturer
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run tag @a[distance=..5,scores={mgs.mp.team=1,mgs.mp.in_game=1}] add mgs.dom_capturer
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_a","fallback":"captured point A!","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_A] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_a","fallback":"captured point A!","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_b","fallback":"captured point B!","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_B] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_b","fallback":"captured point B!","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_c","fallback":"captured point C!","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_C] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_c","fallback":"captured point C!","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_d","fallback":"captured point D!","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_D] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_d","fallback":"captured point D!","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=!mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_e","fallback":"captured point E!","color":"yellow"}]
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 if entity @s[tag=mgs.dom_label_E] run tellraw @a[tag=mgs.dom_capturer] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"}," ",{"translate":"mgs.captured_point_e","fallback":"captured point E!","color":"yellow"},[" ",{"text":"+20 XP","color":"gold"}]]
execute as @a[tag=mgs.dom_capturer] run function mgs:v5.3.0/progression/mp/award_dom_capture
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run playsound minecraft:block.note_block.bell player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 1.2
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run data modify entity @n[tag=mgs.dom_label,distance=..1] text.color set value "red"
execute if score @s mgs.mp.dom_progress matches 100 unless score @s mgs.mp.dom_owner matches 1 run scoreboard players set @s mgs.mp.dom_owner 1
tag @a remove mgs.dom_capturer

