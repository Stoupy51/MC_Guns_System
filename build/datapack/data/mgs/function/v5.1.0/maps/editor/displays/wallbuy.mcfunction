
#> mgs:v5.1.0/maps/editor/displays/wallbuy
#
# @executed	as @e[tag=mgs.element.wallbuy] & at @s
#
# @within	mgs:v5.1.0/maps/editor/refresh_displays [ as @e[tag=mgs.element.wallbuy] & at @s ]
#

# @s = wallbuy marker, at @s (marker Rotation is synced from data.yaw)
data modify storage mgs:temp _ed_disp.weapon_id set from entity @s data.weapon_id
data modify storage mgs:temp _ed_disp.yaw set value 0.0f
data modify storage mgs:temp _ed_disp.yaw set from entity @s data.yaw
function mgs:v5.1.0/maps/editor/displays/summon_wallbuy with storage mgs:temp _ed_disp

