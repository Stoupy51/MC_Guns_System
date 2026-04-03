
#> mgs:v5.0.0/zombies/perks/on_right_click
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.0.0/zombies/perks/setup_iter {run:"function mgs:v5.0.0/zombies/perks/on_right_click",executor:"source"} [ as @n[tag=mgs.pk_new] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Check power requirement
execute store result score #pk_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.power
execute if score #pk_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 run return run function mgs:v5.0.0/zombies/perks/deny_requires_power

# Look up perk_id
execute store result storage mgs:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.id
function mgs:v5.0.0/zombies/perks/lookup_perk with storage mgs:temp _pk_buy

# Check if player already has this perk
function mgs:v5.0.0/zombies/perks/check_owned with storage mgs:temp _pk_data
execute if score #pk_owned mgs.data matches 1 run return run function mgs:v5.0.0/zombies/perks/deny_already_owned

# Get price and check points
execute store result score #pk_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.price
execute unless score @s mgs.zb.points >= #pk_price mgs.data run return run function mgs:v5.0.0/zombies/perks/deny_not_enough_points

# Deduct points
scoreboard players operation @s mgs.zb.points -= #pk_price mgs.data

# Apply perk effect (sets scoreboard + calls specific perk function)
function mgs:v5.0.0/zombies/perks/apply with storage mgs:temp _pk_data

# Signal
function #mgs:zombies/on_new_perk

# Sound
function mgs:v5.0.0/zombies/feedback/sound_success

