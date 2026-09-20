
#> mgs:v5.1.0/zombies/wallbuys/hover_knife
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_hover with storage mgs:temp _wb_weapon
#
# @args		weapon_id (unknown)
#

$execute if items entity @s hotbar.0 *[custom_data~{mgs:{$(weapon_id):true}}] run data modify storage mgs:temp _wb_price_suffix set value " (Owned)"
function mgs:v5.1.0/zombies/wallbuys/render_hover

