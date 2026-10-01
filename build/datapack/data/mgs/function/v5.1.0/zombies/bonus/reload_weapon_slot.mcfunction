
#> mgs:v5.1.0/zombies/bonus/reload_weapon_slot
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.0"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.1"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.2"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.3"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.4"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.5"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.6"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.7"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"hotbar.8"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"weapon.offhand"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.0"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.1"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.2"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.3"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.4"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.5"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.6"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.7"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.8"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.9"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.10"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.11"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.12"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.13"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.14"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.15"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.16"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.17"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.18"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.19"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.20"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.21"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.22"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.23"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.24"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.25"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"inventory.26"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.cursor"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.0"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.1"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.2"}
#			mgs:v5.1.0/zombies/bonus/max_ammo_reload_weapons {slot:"player.crafting.3"}
#			mgs:v5.1.0/zombies/pap/apply_to_slot {slot:"$(slot)"}
#			mgs:v5.1.0/zombies/wallbuys/give_to_slot {slot:"hotbar.$(hotbar)"}
#			mgs:v5.1.0/zombies/wallbuys/reload_pair {slot:"hotbar.$(hotbar)"}
#			mgs:v5.1.0/zombies/wallbuys/replace_pair {slot:"hotbar.$(hotbar)"}
#
# @args		slot (string)
#

tag @s add mgs.reloading_weapon
$execute summon item_display run function mgs:v5.1.0/zombies/bonus/extract_weapon_capacity {slot:"$(slot)"}
tag @s remove mgs.reloading_weapon

# Saved so reloading a slot that is not in hand leaves the HUD of the held weapon alone.
scoreboard players operation #rws_save mgs.data = @s mgs.remaining_bullets

# modify_lore reads this score.
scoreboard players operation @s mgs.remaining_bullets = #bullets mgs.data

# The held weapon (remaining_bullets -1) keeps its ammo in the score, so only its lore changes.
$execute if items entity @s $(slot) *[custom_data~{mgs:{stats:{remaining_bullets:-1}}}] run return run function mgs:v5.1.0/ammo/modify_lore {slot:"$(slot)"}

$item modify entity @s $(slot) mgs:v5.1.0/update_ammo

$function mgs:v5.1.0/ammo/modify_lore {slot:"$(slot)"}

scoreboard players operation @s mgs.remaining_bullets = #rws_save mgs.data

