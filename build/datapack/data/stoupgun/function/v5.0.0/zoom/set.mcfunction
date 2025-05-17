
#> stoupgun:v5.0.0/zoom/set
#
# @within	stoupgun:v5.0.0/zoom/main
#

# Set zoom state in gun stats
data modify storage stoupgun:gun stats.is_zoom set value true

# Prepare input storage for model update
data modify storage stoupgun:input with set value {"item_model":""}
data modify storage stoupgun:input with.item_model set from storage stoupgun:gun stats.models.zoom

# Update weapon model and stats
function stoupgun:v5.0.0/utils/update_model with storage stoupgun:input with
item modify entity @s weapon.mainhand stoupgun:v5.0.0/update_stats

# Apply zoom effects
playsound stoupgun:common/lean_in player @s ~ ~1000000 ~ 1000000
effect give @s slowness infinite 2 true
scoreboard players set @s stoupgun.zoom 1

