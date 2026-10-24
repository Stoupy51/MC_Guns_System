
#> mgs:v5.2.0/multiplayer/custom/notify_selected
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/multiplayer/custom/find_and_notify with storage mgs:temp _find_iter[0]
#
# @args		name (unknown)
#

$tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],["",{"translate":"mgs.class_set_to","fallback":"Class set to"}," "],{"text":"$(name)","color":"green","bold":true},[{"text":"","color":"aqua"}," (",{"translate":"mgs.custom","fallback":"custom"},")"],[{"text":" - ","color":"yellow"}, {"translate":"mgs.will_apply_on_respawn","fallback":"will apply on respawn"}],{"text":" [✔]","color":"gold","hover_event":{"action":"show_text","value":{"translate":"mgs.click_here_to_apply_immediately_op_only","fallback":"Click here to apply immediately (OP only)","color":"yellow"}},"click_event":{"action":"suggest_command","command":"/function mgs:v5.2.0/multiplayer/apply_class"}}]

