
#> mgs:v5.0.0/ammo/end_reload
#
# @within	mgs:v5.0.0/player/tick
#

# Update weapon lore
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Remove reloading tag
tag @s remove mgs.reloading

