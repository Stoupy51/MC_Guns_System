
#> mgs:v5.1.0/zoom/set
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/main
#

data modify storage mgs:gun all.stats.is_zoom set value true

data modify storage mgs:input with set value {"item_model":""}
data modify storage mgs:input with.item_model set from storage mgs:gun all.stats.models.zoom

function mgs:v5.1.0/utils/update_model with storage mgs:input with
function mgs:v5.1.0/ammo/modify_lore {slot:"weapon.mainhand"}
item modify entity @s weapon.mainhand mgs:v5.1.0/update_stats

playsound mgs:common/lean_in player @s
effect give @s slowness infinite 2 true
scoreboard players set @s mgs.zoom 1

# Overlay level from the weapon's scope_level.
function mgs:v5.1.0/zoom/fx_enter

# Run as the player; weapon data in mgs:signals.
data modify storage mgs:signals on_zoom set value {}
data modify storage mgs:signals on_zoom.weapon set from storage mgs:gun all
function #mgs:signals/on_zoom

