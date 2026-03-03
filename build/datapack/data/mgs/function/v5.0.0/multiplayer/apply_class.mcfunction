
#> mgs:v5.0.0/multiplayer/apply_class
#
# @executed	as @a & at @s
#
# @within	mgs:v5.0.0/multiplayer/start [ as @a & at @s ]
#			mgs:v5.0.0/multiplayer/on_respawn
#

execute if score @s mgs.mp.class matches 1 run function mgs:v5.0.0/multiplayer/class/assault
execute if score @s mgs.mp.class matches 2 run function mgs:v5.0.0/multiplayer/class/rifleman
execute if score @s mgs.mp.class matches 3 run function mgs:v5.0.0/multiplayer/class/support
execute if score @s mgs.mp.class matches 4 run function mgs:v5.0.0/multiplayer/class/sniper
execute if score @s mgs.mp.class matches 5 run function mgs:v5.0.0/multiplayer/class/smg
execute if score @s mgs.mp.class matches 6 run function mgs:v5.0.0/multiplayer/class/shotgunner
execute if score @s mgs.mp.class matches 7 run function mgs:v5.0.0/multiplayer/class/engineer
execute if score @s mgs.mp.class matches 8 run function mgs:v5.0.0/multiplayer/class/medic
execute if score @s mgs.mp.class matches 9 run function mgs:v5.0.0/multiplayer/class/marksman
execute if score @s mgs.mp.class matches 10 run function mgs:v5.0.0/multiplayer/class/heavy

# Give class selectors in bottom inventory row for future changes
function mgs:v5.0.0/multiplayer/give_class_selectors_gameplay

