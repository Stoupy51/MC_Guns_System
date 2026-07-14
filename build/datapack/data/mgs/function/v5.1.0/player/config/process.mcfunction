
#> mgs:v5.1.0/player/config/process
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Load per-player editor state (isolates simultaneous editors)
execute store result storage mgs:temp _pid int 1 run scoreboard players get @s bs.id
function mgs:v5.1.0/multiplayer/editor/load_state with storage mgs:temp

# 1 = Show config menu
# 2 = Toggle hitmarker Sound
# 3 = Toggle damage debug in chat
# 4 = Open multiplayer class selection menu
# 6-9 = Zombies perk selection (passive/ability via trigger from dialog)
# 11-20 = Select class 1-10 (via trigger from class menu)
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

# === Custom Loadout Editor (CoD-style hub) ===
# 100 = Open loadout editor (create new), then show the hub
execute if score @s mgs.player.config matches 100 run function mgs:v5.1.0/multiplayer/editor/start
# 101 = Open marketplace browser
execute if score @s mgs.player.config matches 101 run function mgs:v5.1.0/multiplayer/marketplace/browse
# 102 = Open my loadouts manager
execute if score @s mgs.player.config matches 102 run function mgs:v5.1.0/multiplayer/my_loadouts/browse
# 103 = Re-open the editor hub (also the no-op target for grayed-out rows)
execute if score @s mgs.player.config matches 103 run function mgs:v5.1.0/multiplayer/editor/hub
# Hub category rows → open submenus
execute if score @s mgs.player.config matches 104 run function mgs:v5.1.0/multiplayer/editor/show_primary_dialog
execute if score @s mgs.player.config matches 105 run function mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog
execute if score @s mgs.player.config matches 106 run function mgs:v5.1.0/multiplayer/editor/show_secondary_dialog
execute if score @s mgs.player.config matches 107 run function mgs:v5.1.0/multiplayer/editor/show_secondary_mags_dialog
execute if score @s mgs.player.config matches 108 run function mgs:v5.1.0/multiplayer/editor/show_equip_slot1_dialog
execute if score @s mgs.player.config matches 109 run function mgs:v5.1.0/multiplayer/editor/show_equip_slot2_dialog
execute if score @s mgs.player.config matches 110 run function mgs:v5.1.0/multiplayer/editor/show_perks_dialog
# Remove weapon buttons
execute if score @s mgs.player.config matches 111 run function mgs:v5.1.0/multiplayer/editor/remove_primary
execute if score @s mgs.player.config matches 112 run function mgs:v5.1.0/multiplayer/editor/remove_secondary
# 200-222 = Editor: pick primary weapon
execute if score @s mgs.player.config matches 200..222 run function mgs:v5.1.0/multiplayer/editor/pick_primary
# 230-234 = Editor: pick primary scope
execute if score @s mgs.player.config matches 230..234 run function mgs:v5.1.0/multiplayer/editor/pick_primary_scope
# 250-256 = Editor: pick secondary weapon
execute if score @s mgs.player.config matches 250..256 run function mgs:v5.1.0/multiplayer/editor/pick_secondary
# 520-542 = Editor: pick a primary as the Overkill secondary
execute if score @s mgs.player.config matches 520..542 run function mgs:v5.1.0/multiplayer/editor/pick_overkill_secondary
# 260-264 = Editor: pick secondary scope
execute if score @s mgs.player.config matches 260..264 run function mgs:v5.1.0/multiplayer/editor/pick_secondary_scope
# 350-351 = Editor: save loadout (350=public, 351=private)
execute if score @s mgs.player.config matches 350..351 run function mgs:v5.1.0/multiplayer/editor/save
# 391-395 = Editor: pick primary mag count (1-5)
execute if score @s mgs.player.config matches 391..395 run function mgs:v5.1.0/multiplayer/editor/pick_primary_mags
# 396-401 = Editor: pick secondary mag count (0-5)
execute if score @s mgs.player.config matches 396..401 run function mgs:v5.1.0/multiplayer/editor/pick_secondary_mags
# 410-418 = Editor: toggle perk
execute if score @s mgs.player.config matches 410..418 run function mgs:v5.1.0/multiplayer/editor/pick_perk
# 460-464 = Editor: pick equipment slot 1 grenade
execute if score @s mgs.player.config matches 460..464 run function mgs:v5.1.0/multiplayer/editor/pick_equip_slot1
# 470-474 = Editor: pick equipment slot 2 grenade
execute if score @s mgs.player.config matches 470..474 run function mgs:v5.1.0/multiplayer/editor/pick_equip_slot2
# 480-484 = Editor: pick primary camo (free)
execute if score @s mgs.player.config matches 480..484 run function mgs:v5.1.0/multiplayer/editor/pick_primary_camo
# 490-494 = Editor: pick secondary camo (free)
execute if score @s mgs.player.config matches 490..494 run function mgs:v5.1.0/multiplayer/editor/pick_secondary_camo
# 500-504 = Editor: pick grenade slot 1 camo (free)
execute if score @s mgs.player.config matches 500..504 run function mgs:v5.1.0/multiplayer/editor/pick_equip1_camo
# 510-514 = Editor: pick grenade slot 2 camo (free)
execute if score @s mgs.player.config matches 510..514 run function mgs:v5.1.0/multiplayer/editor/pick_equip2_camo
# === Custom Loadout Actions ===
# 10000-19999 = Select/use a custom loadout
execute if score @s mgs.player.config matches 10000..19999 run function mgs:v5.1.0/multiplayer/custom/select
# 20000-29999 = Toggle favorite on a loadout
execute if score @s mgs.player.config matches 20000..29999 run function mgs:v5.1.0/multiplayer/custom/toggle_favorite
# 30000-39999 = Like a loadout
execute if score @s mgs.player.config matches 30000..39999 run function mgs:v5.1.0/multiplayer/custom/like
# 40000-49999 = Delete own loadout
execute if score @s mgs.player.config matches 40000..49999 run function mgs:v5.1.0/multiplayer/custom/delete
# 50000-59999 = Toggle public/private on own loadout
execute if score @s mgs.player.config matches 50000..59999 run function mgs:v5.1.0/multiplayer/custom/toggle_visibility
# 60000-69998 = Set default custom loadout
execute if score @s mgs.player.config matches 60000..69998 run function mgs:v5.1.0/multiplayer/custom/set_default
# 69999 = Unset default loadout
execute if score @s mgs.player.config matches 69999 run function mgs:v5.1.0/multiplayer/custom/unset_default
# 70000-79999 = Edit own loadout (re-opens the hub pre-filled; saving overwrites)
execute if score @s mgs.player.config matches 70000..79999 run function mgs:v5.1.0/multiplayer/custom/edit
# 80000-89999 = Open the per-loadout manage submenu (My Loadouts)
execute if score @s mgs.player.config matches 80000..89999 run function mgs:v5.1.0/multiplayer/my_loadouts/manage
# === Marketplace / My Loadouts Filter & Sort ===
# 1600 = Marketplace: all public (favorites first)
execute if score @s mgs.player.config matches 1600 run function mgs:v5.1.0/multiplayer/marketplace/browse
# 1601 = Marketplace: only favorited loadouts
execute if score @s mgs.player.config matches 1601 run function mgs:v5.1.0/multiplayer/marketplace/browse_fav_only
# 1602 = Marketplace: sorted by most likes
execute if score @s mgs.player.config matches 1602 run function mgs:v5.1.0/multiplayer/marketplace/browse_likes
# 1603 = My Loadouts: favorites only
execute if score @s mgs.player.config matches 1603 run function mgs:v5.1.0/multiplayer/my_loadouts/browse_fav_only

# Save per-player editor state back to isolated storage
function mgs:v5.1.0/multiplayer/editor/save_state with storage mgs:temp

# Reset score
scoreboard players set @s mgs.player.config 0

