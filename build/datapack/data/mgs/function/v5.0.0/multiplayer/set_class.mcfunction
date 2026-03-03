
#> mgs:v5.0.0/multiplayer/set_class
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process {class_num:1,class_name:"Assault"}
#			mgs:v5.0.0/player/config/process {class_num:2,class_name:"Rifleman"}
#			mgs:v5.0.0/player/config/process {class_num:3,class_name:"Support"}
#			mgs:v5.0.0/player/config/process {class_num:4,class_name:"Sniper"}
#			mgs:v5.0.0/player/config/process {class_num:5,class_name:"SMG"}
#			mgs:v5.0.0/player/config/process {class_num:6,class_name:"Shotgunner"}
#			mgs:v5.0.0/player/config/process {class_num:7,class_name:"Engineer"}
#			mgs:v5.0.0/player/config/process {class_num:8,class_name:"Medic"}
#			mgs:v5.0.0/player/config/process {class_num:9,class_name:"Marksman"}
#			mgs:v5.0.0/player/config/process {class_num:10,class_name:"Heavy"}
#
# @args		class_num (int)
#			class_name (string)
#

$scoreboard players set @s mgs.mp.class $(class_num)

# If game active: queue for next respawn
$execute if data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"$(class_name)","color":"green","bold":true},{"translate": "mgs.will_apply_on_respawn","color":"yellow"},{"text":" [✔]","color":"gold","hover_event":{"action":"show_text","value":{"translate": "mgs.click_here_to_apply_immediately_op_only","color":"yellow"}},"click_event":{"action":"run_command","command":"/function mgs:v5.0.0/multiplayer/apply_class"}}]

# If game not active: only save choice (no loadout outside multiplayer)
$execute unless data storage mgs:multiplayer game{state:"active"} run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.class_set_to","color":"white"},{"text":"$(class_name)","color":"green","bold":true},{"text":" [✔]","color":"gold","hover_event":{"action":"show_text","value":{"translate": "mgs.click_here_to_apply_immediately_op_only","color":"yellow"}},"click_event":{"action":"run_command","command":"/function mgs:v5.0.0/multiplayer/apply_class"}}]

