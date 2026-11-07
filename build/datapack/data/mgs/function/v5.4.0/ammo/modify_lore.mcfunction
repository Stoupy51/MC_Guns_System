
#> mgs:v5.4.0/ammo/modify_lore
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/player/right_click {slot:"weapon.mainhand"}
#			mgs:v5.4.0/zoom/remove {slot:"weapon.mainhand"}
#			mgs:v5.4.0/zoom/set {slot:"weapon.mainhand"}
#			mgs:v5.4.0/ammo/set_count {slot:"$(slot)"}
#			mgs:v5.4.0/ammo/end_reload {slot:"weapon.mainhand"}
#			mgs:v5.4.0/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Target of the item_display.
tag @s add mgs.modify_lore

$execute summon item_display run function mgs:v5.4.0/ammo/get_current_lore {"slot":"$(slot)"}

scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.4.0/ammo/search_lore_loop {"slot":"$(slot)"}

tag @s remove mgs.modify_lore

