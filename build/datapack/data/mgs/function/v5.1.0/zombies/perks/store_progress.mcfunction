
#> mgs:v5.1.0/zombies/perks/store_progress
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#
# @args		perk_id (unknown)
#

$scoreboard players operation @s mgs.zb.perkpaid.$(perk_id) = #pk_paid mgs.data

