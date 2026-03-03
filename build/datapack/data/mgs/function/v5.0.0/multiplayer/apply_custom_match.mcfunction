
#> mgs:v5.0.0/multiplayer/apply_custom_match
#
# @executed	as @a & at @s
#
# @within	mgs:v5.0.0/multiplayer/apply_custom_found
#

# Copy found loadout's slots to the format expected by apply_class_dynamic
data modify storage mgs:temp current_class set value {slots:[]}
data modify storage mgs:temp current_class.slots set from storage mgs:temp _find_iter[0].slots

# Apply the loadout (clears inventory and gives items)
function mgs:v5.0.0/multiplayer/apply_class_dynamic

# Copy the loadout compound to a flat temp for perk checks (since [0]{filter} is invalid syntax)
data modify storage mgs:temp _cur_loadout set from storage mgs:temp _find_iter[0]

# Apply perks from the loadout (new Pick-10 system)
# Passive perks: set scoreboard scores that are checked by the game logic
execute if data storage mgs:temp _cur_loadout{perks:["quick_reload"]} run scoreboard players set @s mgs.special.quick_reload 1
execute unless data storage mgs:temp _cur_loadout{perks:["quick_reload"]} run scoreboard players set @s mgs.special.quick_reload 0
execute if data storage mgs:temp _cur_loadout{perks:["quick_swap"]} run scoreboard players set @s mgs.special.quick_swap 1
execute unless data storage mgs:temp _cur_loadout{perks:["quick_swap"]} run scoreboard players set @s mgs.special.quick_swap 0

# Timed perks: grant limited-duration buff (set score to timer ticks)
# Overkill (infinite_ammo): unlimited ammo for 30 seconds (600 ticks)
execute if data storage mgs:temp _cur_loadout{perks:["infinite_ammo"]} run scoreboard players set @s mgs.special.infinite_ammo 600
execute unless data storage mgs:temp _cur_loadout{perks:["infinite_ammo"]} run scoreboard players set @s mgs.special.infinite_ammo 0
# Assassin (instant_kill): one-shot kill for 10 seconds (200 ticks)
execute if data storage mgs:temp _cur_loadout{perks:["instant_kill"]} run scoreboard players set @s mgs.special.instant_kill 200
execute unless data storage mgs:temp _cur_loadout{perks:["instant_kill"]} run scoreboard players set @s mgs.special.instant_kill 0

