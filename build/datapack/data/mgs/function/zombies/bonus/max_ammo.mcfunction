
#> mgs:zombies/bonus/max_ammo
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/powerups/activate/max_ammo [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#

# Copy gun data for current weapon (needed for ammo scoreboard sync)
function mgs:v5.0.0/utils/copy_gun_data

# Refill all magazines in inventory to max capacity
execute if items entity @s hotbar.0 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.0"}
execute if items entity @s hotbar.1 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.1"}
execute if items entity @s hotbar.2 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.2"}
execute if items entity @s hotbar.3 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.3"}
execute if items entity @s hotbar.4 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.4"}
execute if items entity @s hotbar.5 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.5"}
execute if items entity @s hotbar.6 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.6"}
execute if items entity @s hotbar.7 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.7"}
execute if items entity @s hotbar.8 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"hotbar.8"}
execute if items entity @s weapon.offhand *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"weapon.offhand"}
execute if items entity @s inventory.0 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.0"}
execute if items entity @s inventory.1 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.1"}
execute if items entity @s inventory.2 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.2"}
execute if items entity @s inventory.3 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.3"}
execute if items entity @s inventory.4 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.4"}
execute if items entity @s inventory.5 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.5"}
execute if items entity @s inventory.6 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.6"}
execute if items entity @s inventory.7 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.7"}
execute if items entity @s inventory.8 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.8"}
execute if items entity @s inventory.9 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.9"}
execute if items entity @s inventory.10 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.10"}
execute if items entity @s inventory.11 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.11"}
execute if items entity @s inventory.12 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.12"}
execute if items entity @s inventory.13 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.13"}
execute if items entity @s inventory.14 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.14"}
execute if items entity @s inventory.15 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.15"}
execute if items entity @s inventory.16 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.16"}
execute if items entity @s inventory.17 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.17"}
execute if items entity @s inventory.18 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.18"}
execute if items entity @s inventory.19 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.19"}
execute if items entity @s inventory.20 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.20"}
execute if items entity @s inventory.21 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.21"}
execute if items entity @s inventory.22 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.22"}
execute if items entity @s inventory.23 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.23"}
execute if items entity @s inventory.24 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.24"}
execute if items entity @s inventory.25 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.25"}
execute if items entity @s inventory.26 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"inventory.26"}
execute if items entity @s player.cursor *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"player.cursor"}
execute if items entity @s player.crafting.0 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"player.crafting.0"}
execute if items entity @s player.crafting.1 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"player.crafting.1"}
execute if items entity @s player.crafting.2 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"player.crafting.2"}
execute if items entity @s player.crafting.3 *[custom_data~{mgs:{magazine:true}}] run function mgs:v5.0.0/zombies/bonus/refill_magazine {slot:"player.crafting.3"}

# Also reload all weapons in inventory if config allows (1 = recent zombies, 0 = OG magazines only)
execute if score #max_ammo_reload_weapons mgs.config matches 1.. run function mgs:v5.0.0/zombies/bonus/max_ammo_reload_weapons

# Recompute reserve ammo display after refilling all magazines
function mgs:v5.0.0/ammo/compute_reserve

