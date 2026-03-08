
#> mgs:v5.0.0/zombies/perks/check_owned
#
# @within	mgs:v5.0.0/zombies/perks/on_right_click with storage mgs:temp _pk_data
#
# @args		perk_id (unknown)
#

scoreboard players set #_pk_owned mgs.data 0
$execute if score @s mgs.zb.perk.$(perk_id) matches 1 run scoreboard players set #_pk_owned mgs.data 1

