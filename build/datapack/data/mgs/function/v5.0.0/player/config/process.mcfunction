
#> mgs:v5.0.0/player/config/process
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# 1 = Show config menu
# 2 = Toggle hitmarker Sound
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

# === Custom Loadout Editor ===
# 100 = Open loadout editor (create new)
execute if score @s mgs.player.config matches 100 run function mgs:v5.0.0/multiplayer/editor/start
# 101 = Open marketplace browser
execute if score @s mgs.player.config matches 101 run function mgs:v5.0.0/multiplayer/marketplace/browse
# 102 = Open my loadouts manager
execute if score @s mgs.player.config matches 102 run function mgs:v5.0.0/multiplayer/my_loadouts/browse
# 200-222 = Editor: pick primary weapon
execute if score @s mgs.player.config matches 200..222 run function mgs:v5.0.0/multiplayer/editor/pick_primary
# 230-234 = Editor: pick primary scope
execute if score @s mgs.player.config matches 230..234 run function mgs:v5.0.0/multiplayer/editor/pick_primary_scope
# 250-258 = Editor: pick secondary weapon (258 = none)
execute if score @s mgs.player.config matches 250..258 run function mgs:v5.0.0/multiplayer/editor/pick_secondary
# 260-264 = Editor: pick secondary scope
execute if score @s mgs.player.config matches 260..264 run function mgs:v5.0.0/multiplayer/editor/pick_secondary_scope
# 300-309 = Editor: pick equipment preset
execute if score @s mgs.player.config matches 300..309 run function mgs:v5.0.0/multiplayer/editor/pick_equipment
# 350-351 = Editor: save loadout (350=public, 351=private)
execute if score @s mgs.player.config matches 350..351 run function mgs:v5.0.0/multiplayer/editor/save
# === Custom Loadout Actions ===
# 1000-1099 = Select/use a custom loadout
execute if score @s mgs.player.config matches 1000..1099 run function mgs:v5.0.0/multiplayer/custom/select
# 1100-1199 = Toggle favorite on a loadout
execute if score @s mgs.player.config matches 1100..1199 run function mgs:v5.0.0/multiplayer/custom/toggle_favorite
# 1200-1299 = Like a loadout
execute if score @s mgs.player.config matches 1200..1299 run function mgs:v5.0.0/multiplayer/custom/like
# 1300-1399 = Delete own loadout
execute if score @s mgs.player.config matches 1300..1399 run function mgs:v5.0.0/multiplayer/custom/delete
# 1400-1499 = Toggle public/private on own loadout
execute if score @s mgs.player.config matches 1400..1499 run function mgs:v5.0.0/multiplayer/custom/toggle_visibility
# 1500-1598 = Set default custom loadout
execute if score @s mgs.player.config matches 1500..1599 run function mgs:v5.0.0/multiplayer/custom/set_default
# 1599 = Unset default loadout
execute if score @s mgs.player.config matches 1599 run function mgs:v5.0.0/multiplayer/custom/unset_default

# Reset score
scoreboard players set @s mgs.player.config 0

