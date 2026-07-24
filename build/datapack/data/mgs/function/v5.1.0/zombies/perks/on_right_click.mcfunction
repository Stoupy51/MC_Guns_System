
#> mgs:v5.1.0/zombies/perks/on_right_click
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/setup_iter {run:"function mgs:v5.1.0/zombies/perks/on_right_click",executor:"source"} [ as @n[tag=mgs.pk_new] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Check power requirement. Quick Revive is exempt while solo (Black Ops rule).
execute store result score #pk_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.power
execute store result score #qr_solo mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
execute if score #pk_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 unless entity @n[tag=bs.interaction.target,tag=mgs.pk_quick_revive] run return run function mgs:v5.1.0/zombies/perks/deny_requires_power
execute if score #pk_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 if entity @n[tag=bs.interaction.target,tag=mgs.pk_quick_revive] if score #qr_solo mgs.data matches 2.. run return run function mgs:v5.1.0/zombies/perks/deny_requires_power

# Look up perk_id
execute store result storage mgs:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.id
function mgs:v5.1.0/zombies/perks/lookup_perk with storage mgs:temp _pk_buy

# Check if player already has this perk
function mgs:v5.1.0/zombies/perks/check_owned with storage mgs:temp _pk_data
execute if score #pk_owned mgs.data matches 1 run return run function mgs:v5.1.0/zombies/perks/deny_already_owned

# Get price and check points (chip-in machines charge one chunk per click)
function mgs:v5.1.0/zombies/perks/read_price with storage mgs:temp _pk_data
execute unless score @s mgs.zb.points >= #pk_price mgs.data run return run function mgs:v5.1.0/zombies/perks/deny_not_enough_points

# Deduct points
scoreboard players operation @s mgs.zb.points -= #pk_price mgs.data

# Chip-in: progress is LOCAL, each player pays down their own perk. Stop here unless this
# payment was the one that completed it.
scoreboard players operation #pk_paid mgs.data += #pk_price mgs.data
execute if score #pk_partial mgs.data matches 1.. run function mgs:v5.1.0/zombies/perks/store_progress with storage mgs:temp _pk_data
execute if score #pk_partial mgs.data matches 1.. if score #pk_paid mgs.data < #pk_total mgs.data run return run function mgs:v5.1.0/zombies/perks/announce_progress

# Apply perk effect (sets scoreboard + calls specific perk function)
function mgs:v5.1.0/zombies/perks/apply with storage mgs:temp _pk_data

# Signal
function #mgs:zombies/on_new_perk

# Sound
playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25

