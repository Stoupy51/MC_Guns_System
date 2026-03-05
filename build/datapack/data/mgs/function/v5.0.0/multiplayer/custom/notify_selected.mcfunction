
#> mgs:v5.0.0/multiplayer/custom/notify_selected
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/find_and_notify with storage mgs:temp _find_iter[0]
#
# @args		name (unknown)
#

$tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],["",{"translate": "mgs.class_set_to"}," "],{"text":"$(name)","color":"green","bold":true},[{"text":"","color":"aqua"}," (",{"translate": "mgs.custom"},")"],{"translate": "mgs.will_apply_on_respawn","color":"yellow"},{"text":" [✔]","color":"gold","hover_event":{"action":"show_text","value":{"translate": "mgs.click_here_to_apply_immediately_op_only","color":"yellow"}},"click_event":{"action":"run_command","command":"/function mgs:v5.0.0/multiplayer/apply_class"}}]

