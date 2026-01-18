
#> mgs:v5.0.0/zoom/set
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/zoom/main
#

# Set zoom state in gun stats
data modify storage mgs:gun all.stats.is_zoom set value true

# Prepare input storage for model update
data modify storage mgs:input with set value {"item_model":""}
data modify storage mgs:input with.item_model set from storage mgs:gun all.stats.models.zoom

# Update weapon model and stats
function mgs:v5.0.0/utils/update_model with storage mgs:input with
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}
item modify entity @s weapon.mainhand mgs:v5.0.0/update_stats

# Apply zoom effects
playsound mgs:common/lean_in player @s
effect give @s slowness infinite 2 true
scoreboard players set @s mgs.zoom 1

