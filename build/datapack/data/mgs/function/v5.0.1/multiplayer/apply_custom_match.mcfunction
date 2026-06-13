
#> mgs:v5.0.1/multiplayer/apply_custom_match
#
# @within	mgs:v5.0.1/multiplayer/apply_custom_found
#

# Copy found loadout's slots to the format expected by apply_class_dynamic
data modify storage mgs:temp current_class set value {slots:[]}
data modify storage mgs:temp current_class.slots set from storage mgs:temp _find_iter[0].slots

# Apply the loadout (clears inventory and gives items)
function mgs:v5.0.1/multiplayer/apply_class_dynamic

# Copy the loadout compound to a flat temp for perk checks (since [0]{filter} is invalid syntax)
data modify storage mgs:temp _cur_loadout set from storage mgs:temp _find_iter[0]

# Apply perks from the loadout (Pick-10 system)
# Sleight of Hand / Fast Hands: percentages (50 = 50% faster)
execute if data storage mgs:temp _cur_loadout{perks:["quick_reload"]} run scoreboard players set @s mgs.special.quick_reload 50
execute unless data storage mgs:temp _cur_loadout{perks:["quick_reload"]} run scoreboard players set @s mgs.special.quick_reload 0
execute if data storage mgs:temp _cur_loadout{perks:["quick_swap"]} run scoreboard players set @s mgs.special.quick_swap 50
execute unless data storage mgs:temp _cur_loadout{perks:["quick_swap"]} run scoreboard players set @s mgs.special.quick_swap 0

# Flag perks (0/1), read by the systems they affect
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["scavenger"]}
scoreboard players operation @s mgs.special.scavenger = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["flak_jacket"]}
scoreboard players operation @s mgs.special.flak_jacket = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["tracker"]}
scoreboard players operation @s mgs.special.tracker = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["tactical_mask"]}
scoreboard players operation @s mgs.special.tactical_mask = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["overkill"]}
scoreboard players operation @s mgs.special.overkill = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["quick_fix"]}
scoreboard players operation @s mgs.special.quick_fix = #has_perk mgs.data

# Juggernaut: flag + raised max health (30 HP), reset to default 20 otherwise
execute store success score #has_perk mgs.data if data storage mgs:temp _cur_loadout{perks:["juggernaut"]}
scoreboard players operation @s mgs.special.juggernaut = #has_perk mgs.data
execute if score #has_perk mgs.data matches 1 run attribute @s minecraft:max_health base set 30
execute if score #has_perk mgs.data matches 0 run attribute @s minecraft:max_health base set 20

# Custom loadouts never grant the admin/powerup buffs — clear any leftovers
scoreboard players set @s mgs.special.infinite_ammo 0
scoreboard players set @s mgs.special.instant_kill 0

