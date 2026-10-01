
#> mgs:v5.1.0/player/config/process
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Isolates simultaneous editors.
execute store result storage mgs:temp _pid int 1 run scoreboard players get @s bs.id
function mgs:v5.1.0/multiplayer/editor/load_state with storage mgs:temp

# 1 config menu, 2 hitmarker sound, 3 damage debug in chat, 4 class menu, 6-9 zombies passive and ability, 11-20 class 1-10.
execute if score @s mgs.player.config matches 1 run function mgs:v5.1.0/player/config/menu
execute if score @s mgs.player.config matches 2 run function mgs:v5.1.0/player/config/toggle_hitmarker
execute if score @s mgs.player.config matches 3 run function mgs:v5.1.0/player/config/toggle_damage_debug
execute if score @s mgs.player.config matches 4 run function mgs:v5.1.0/multiplayer/select_class
execute if score @s mgs.player.config matches 5 run function mgs:v5.1.0/zombies/passive_ability_menu
execute if score @s mgs.player.config matches 6 run function mgs:v5.1.0/zombies/perks/set_passive_1
execute if score @s mgs.player.config matches 7 run function mgs:v5.1.0/zombies/perks/set_passive_2
execute if score @s mgs.player.config matches 8 run function mgs:v5.1.0/zombies/perks/set_ability_1
execute if score @s mgs.player.config matches 9 run function mgs:v5.1.0/zombies/perks/set_ability_2
execute if score @s mgs.player.config matches 11 run function mgs:v5.1.0/multiplayer/set_class {class_num:1,class_name:"Assault"}
execute if score @s mgs.player.config matches 12 run function mgs:v5.1.0/multiplayer/set_class {class_num:2,class_name:"Rifleman"}
execute if score @s mgs.player.config matches 13 run function mgs:v5.1.0/multiplayer/set_class {class_num:3,class_name:"Support"}
execute if score @s mgs.player.config matches 14 run function mgs:v5.1.0/multiplayer/set_class {class_num:4,class_name:"Sniper"}
execute if score @s mgs.player.config matches 15 run function mgs:v5.1.0/multiplayer/set_class {class_num:5,class_name:"SMG"}
execute if score @s mgs.player.config matches 16 run function mgs:v5.1.0/multiplayer/set_class {class_num:6,class_name:"Shotgunner"}
execute if score @s mgs.player.config matches 17 run function mgs:v5.1.0/multiplayer/set_class {class_num:7,class_name:"Engineer"}
execute if score @s mgs.player.config matches 18 run function mgs:v5.1.0/multiplayer/set_class {class_num:8,class_name:"Medic"}
execute if score @s mgs.player.config matches 19 run function mgs:v5.1.0/multiplayer/set_class {class_num:9,class_name:"Marksman"}
execute if score @s mgs.player.config matches 20 run function mgs:v5.1.0/multiplayer/set_class {class_num:10,class_name:"Heavy"}

# Custom loadout editor.
execute if score @s mgs.player.config matches 100 run function mgs:v5.1.0/multiplayer/editor/start
execute if score @s mgs.player.config matches 101 run function mgs:v5.1.0/multiplayer/marketplace/browse
execute if score @s mgs.player.config matches 102 run function mgs:v5.1.0/multiplayer/my_loadouts/browse
# Also the no-op target of grayed-out rows.
execute if score @s mgs.player.config matches 103 run function mgs:v5.1.0/multiplayer/editor/hub
execute if score @s mgs.player.config matches 104 run function mgs:v5.1.0/multiplayer/editor/show_primary_dialog
execute if score @s mgs.player.config matches 105 run function mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog
execute if score @s mgs.player.config matches 106 run function mgs:v5.1.0/multiplayer/editor/show_secondary_dialog
execute if score @s mgs.player.config matches 107 run function mgs:v5.1.0/multiplayer/editor/show_secondary_mags_dialog
execute if score @s mgs.player.config matches 108 run function mgs:v5.1.0/multiplayer/editor/show_equip_slot1_dialog
execute if score @s mgs.player.config matches 109 run function mgs:v5.1.0/multiplayer/editor/show_equip_slot2_dialog
execute if score @s mgs.player.config matches 110 run function mgs:v5.1.0/multiplayer/editor/show_perks_dialog
execute if score @s mgs.player.config matches 113 run function mgs:v5.1.0/multiplayer/editor/show_knife_camo_dialog
execute if score @s mgs.player.config matches 111 run function mgs:v5.1.0/multiplayer/editor/remove_primary
execute if score @s mgs.player.config matches 112 run function mgs:v5.1.0/multiplayer/editor/remove_secondary
execute if score @s mgs.player.config matches 200..222 run function mgs:v5.1.0/multiplayer/editor/pick_primary
execute if score @s mgs.player.config matches 230..234 run function mgs:v5.1.0/multiplayer/editor/pick_primary_scope
execute if score @s mgs.player.config matches 250..256 run function mgs:v5.1.0/multiplayer/editor/pick_secondary
execute if score @s mgs.player.config matches 520..542 run function mgs:v5.1.0/multiplayer/editor/pick_overkill_secondary
execute if score @s mgs.player.config matches 260..264 run function mgs:v5.1.0/multiplayer/editor/pick_secondary_scope
execute if score @s mgs.player.config matches 350..351 run function mgs:v5.1.0/multiplayer/editor/save
execute if score @s mgs.player.config matches 391..395 run function mgs:v5.1.0/multiplayer/editor/pick_primary_mags
execute if score @s mgs.player.config matches 396..401 run function mgs:v5.1.0/multiplayer/editor/pick_secondary_mags
execute if score @s mgs.player.config matches 410..418 run function mgs:v5.1.0/multiplayer/editor/pick_perk
execute if score @s mgs.player.config matches 460..464 run function mgs:v5.1.0/multiplayer/editor/pick_equip_slot1
execute if score @s mgs.player.config matches 470..474 run function mgs:v5.1.0/multiplayer/editor/pick_equip_slot2
execute if score @s mgs.player.config matches 480..484 run function mgs:v5.1.0/multiplayer/editor/pick_primary_camo
execute if score @s mgs.player.config matches 490..494 run function mgs:v5.1.0/multiplayer/editor/pick_secondary_camo
execute if score @s mgs.player.config matches 500..504 run function mgs:v5.1.0/multiplayer/editor/pick_equip1_camo
execute if score @s mgs.player.config matches 510..514 run function mgs:v5.1.0/multiplayer/editor/pick_equip2_camo
execute if score @s mgs.player.config matches 600..604 run function mgs:v5.1.0/multiplayer/editor/pick_knife_camo
# Custom loadout actions.
execute if score @s mgs.player.config matches 10000..19999 run function mgs:v5.1.0/multiplayer/custom/select
execute if score @s mgs.player.config matches 20000..29999 run function mgs:v5.1.0/multiplayer/custom/toggle_favorite
execute if score @s mgs.player.config matches 30000..39999 run function mgs:v5.1.0/multiplayer/custom/like
execute if score @s mgs.player.config matches 40000..49999 run function mgs:v5.1.0/multiplayer/custom/delete
execute if score @s mgs.player.config matches 50000..59999 run function mgs:v5.1.0/multiplayer/custom/toggle_visibility
execute if score @s mgs.player.config matches 60000..69998 run function mgs:v5.1.0/multiplayer/custom/set_default
execute if score @s mgs.player.config matches 69999 run function mgs:v5.1.0/multiplayer/custom/unset_default
execute if score @s mgs.player.config matches 70000..79999 run function mgs:v5.1.0/multiplayer/custom/edit
execute if score @s mgs.player.config matches 80000..89999 run function mgs:v5.1.0/multiplayer/my_loadouts/manage
# Marketplace and My Loadouts filters.
execute if score @s mgs.player.config matches 1600 run function mgs:v5.1.0/multiplayer/marketplace/browse
execute if score @s mgs.player.config matches 1601 run function mgs:v5.1.0/multiplayer/marketplace/browse_fav_only
execute if score @s mgs.player.config matches 1602 run function mgs:v5.1.0/multiplayer/marketplace/browse_likes
execute if score @s mgs.player.config matches 1603 run function mgs:v5.1.0/multiplayer/my_loadouts/browse_fav_only

function mgs:v5.1.0/multiplayer/editor/save_state with storage mgs:temp

scoreboard players set @s mgs.player.config 0

