
#> mgs:v5.1.0/zoom/remove
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/main
#

data remove storage mgs:gun all.stats.is_zoom

data modify storage mgs:input with set value {"item_model":""}
data modify storage mgs:input with.item_model set from storage mgs:gun all.stats.models.normal

function mgs:v5.1.0/utils/update_model with storage mgs:input with
function mgs:v5.1.0/ammo/modify_lore {slot:"weapon.mainhand"}
item modify entity @s weapon.mainhand mgs:v5.1.0/update_stats

playsound mgs:common/lean_out player
scoreboard players reset @s mgs.zoom
effect clear @s slowness

# The scope overlay switches to its fade-out id.
function mgs:v5.1.0/zoom/fx_leave

# Run as the player; weapon data in mgs:signals.
data modify storage mgs:signals on_unzoom set value {}
data modify storage mgs:signals on_unzoom.weapon set from storage mgs:gun all
function #mgs:signals/on_unzoom

