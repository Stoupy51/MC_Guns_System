
#> mgs:v5.4.4/ammo/modify_lore
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/player/right_click {slot:"weapon.mainhand"}
#			mgs:v5.4.4/zoom/remove {slot:"weapon.mainhand"}
#			mgs:v5.4.4/zoom/set {slot:"weapon.mainhand"}
#			mgs:v5.4.4/ammo/set_count {slot:"$(slot)"}
#			mgs:v5.4.4/ammo/end_reload {slot:"weapon.mainhand"}
#			mgs:v5.4.4/zombies/bonus/reload_weapon_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Target of the item_display.
tag @s add mgs.modify_lore

$execute summon item_display run function mgs:v5.4.4/ammo/get_current_lore {"slot":"$(slot)"}

scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.4.4/ammo/search_lore_loop {"slot":"$(slot)"}

tag @s remove mgs.modify_lore

