
#> stoupgun:v5.0.0/zoom/remove
#
# @within	stoupgun:v5.0.0/zoom/main
#

# Remove zoom state from gun stats
data remove storage stoupgun:gun all.stats.is_zoom

# Prepare input storage for model update
data modify storage stoupgun:input with set value {"item_model":""}
data modify storage stoupgun:input with.item_model set from storage stoupgun:gun all.stats.models.normal

# Update weapon model and stats
function stoupgun:v5.0.0/utils/update_model with storage stoupgun:input with
item modify entity @s weapon.mainhand stoupgun:v5.0.0/update_stats

# Apply unzoom effects
playsound stoupgun:common/lean_out player @s ~ ~1000000 ~ 1000000
scoreboard players reset @s stoupgun.zoom
effect clear @s slowness

