
#> mgs:v5.0.0/zoom/remove
#
# @within	mgs:v5.0.0/zoom/main
#

# Remove zoom state from gun stats
data remove storage mgs:gun all.stats.is_zoom

# Prepare input storage for model update
data modify storage mgs:input with set value {"item_model":""}
data modify storage mgs:input with.item_model set from storage mgs:gun all.stats.models.normal

# Update weapon model and stats
function mgs:v5.0.0/utils/update_model with storage mgs:input with
function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}
item modify entity @s weapon.mainhand mgs:v5.0.0/update_stats

# Apply unzoom effects
playsound mgs:common/lean_out player
scoreboard players reset @s mgs.zoom
effect clear @s slowness

