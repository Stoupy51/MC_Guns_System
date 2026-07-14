
#> mgs:v5.1.0/multiplayer/apply_perks
#
# @within	mgs:v5.1.0/multiplayer/apply_class_dynamic
#

# Sleight of Hand / Fast Hands: percentages (50 = 50% faster), 0 when absent
execute if data storage mgs:temp current_class{perks:["quick_reload"]} run scoreboard players set @s mgs.special.quick_reload 50
execute unless data storage mgs:temp current_class{perks:["quick_reload"]} run scoreboard players set @s mgs.special.quick_reload 0
execute if data storage mgs:temp current_class{perks:["quick_swap"]} run scoreboard players set @s mgs.special.quick_swap 50
execute unless data storage mgs:temp current_class{perks:["quick_swap"]} run scoreboard players set @s mgs.special.quick_swap 0

# Flag perks (0/1), read by the systems they affect
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["scavenger"]}
scoreboard players operation @s mgs.special.scavenger = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["flak_jacket"]}
scoreboard players operation @s mgs.special.flak_jacket = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["tracker"]}
scoreboard players operation @s mgs.special.tracker = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["tactical_mask"]}
scoreboard players operation @s mgs.special.tactical_mask = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["overkill"]}
scoreboard players operation @s mgs.special.overkill = #has_perk mgs.data
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["quick_fix"]}
scoreboard players operation @s mgs.special.quick_fix = #has_perk mgs.data

# Juggernaut: flag + raised max health (24 HP), reset to default 20 otherwise
execute store success score #has_perk mgs.data if data storage mgs:temp current_class{perks:["juggernaut"]}
scoreboard players operation @s mgs.special.juggernaut = #has_perk mgs.data
execute if score #has_perk mgs.data matches 1 run attribute @s minecraft:max_health base set 24
execute if score #has_perk mgs.data matches 0 run attribute @s minecraft:max_health base reset

# Loadouts never grant the admin/powerup buffs — clear any leftovers
scoreboard players set @s mgs.special.infinite_ammo 0
scoreboard players set @s mgs.special.instant_kill 0

