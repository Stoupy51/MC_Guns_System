
#> mgs:v5.0.0/player/config/process
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# 1 = Show config menu
# 2 = Toggle hitmarker sound
# 3 = Toggle damage debug in chat
# 4 = Open multiplayer class selection menu
# 11-20 = Select class 1-10 (via trigger from class menu)
execute if score @s mgs.player.config matches 1 run function mgs:v5.0.0/player/config/menu
execute if score @s mgs.player.config matches 2 run function mgs:v5.0.0/player/config/toggle_hitmarker
execute if score @s mgs.player.config matches 3 run function mgs:v5.0.0/player/config/toggle_damage_debug
execute if score @s mgs.player.config matches 4 run function mgs:v5.0.0/multiplayer/select_class
execute if score @s mgs.player.config matches 11 run function mgs:v5.0.0/multiplayer/set_class {class_num:1,class_name:"Assault"}
execute if score @s mgs.player.config matches 12 run function mgs:v5.0.0/multiplayer/set_class {class_num:2,class_name:"Rifleman"}
execute if score @s mgs.player.config matches 13 run function mgs:v5.0.0/multiplayer/set_class {class_num:3,class_name:"Support"}
execute if score @s mgs.player.config matches 14 run function mgs:v5.0.0/multiplayer/set_class {class_num:4,class_name:"Sniper"}
execute if score @s mgs.player.config matches 15 run function mgs:v5.0.0/multiplayer/set_class {class_num:5,class_name:"SMG"}
execute if score @s mgs.player.config matches 16 run function mgs:v5.0.0/multiplayer/set_class {class_num:6,class_name:"Shotgunner"}
execute if score @s mgs.player.config matches 17 run function mgs:v5.0.0/multiplayer/set_class {class_num:7,class_name:"Engineer"}
execute if score @s mgs.player.config matches 18 run function mgs:v5.0.0/multiplayer/set_class {class_num:8,class_name:"Medic"}
execute if score @s mgs.player.config matches 19 run function mgs:v5.0.0/multiplayer/set_class {class_num:9,class_name:"Marksman"}
execute if score @s mgs.player.config matches 20 run function mgs:v5.0.0/multiplayer/set_class {class_num:10,class_name:"Heavy"}

# Reset score
scoreboard players set @s mgs.player.config 0

