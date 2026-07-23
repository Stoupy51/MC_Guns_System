
#> mgs:v5.1.0/zombies/inventory/place_perk/widows_wine
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/refresh_perk_items
#

execute store result storage mgs:temp _perk_place.slot int 1 run scoreboard players get #perk_inv_slot mgs.data
function mgs:v5.1.0/zombies/inventory/place_perk_at/widows_wine with storage mgs:temp _perk_place
scoreboard players remove #perk_inv_slot mgs.data 1

