
#> mgs:v5.1.0/zombies/perks/read_price
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#			mgs:v5.1.0/zombies/perks/on_hover with storage mgs:temp _pk_data
#
# @args		perk_id (unknown)
#

execute store result score #pk_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.price
execute store result score #pk_partial mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.partial
$execute store result score #pk_paid mgs.data run scoreboard players get @s mgs.zb.perkpaid.$(perk_id)
scoreboard players operation #pk_total mgs.data = #pk_price mgs.data

# Remaining, clamped at 0: solo Quick Revive rewrites the price live, so it can drop below the
# progress already paid. Clamping makes that last click free instead of refunding points.
scoreboard players operation #pk_left mgs.data = #pk_total mgs.data
scoreboard players operation #pk_left mgs.data -= #pk_paid mgs.data
execute if score #pk_left mgs.data matches ..0 run scoreboard players set #pk_left mgs.data 0

# Fixed chunks, last one is the remainder
execute if score #pk_partial mgs.data matches 1.. run scoreboard players operation #pk_price mgs.data = #pk_partial mgs.data
execute if score #pk_partial mgs.data matches 1.. run scoreboard players operation #pk_price mgs.data < #pk_left mgs.data

