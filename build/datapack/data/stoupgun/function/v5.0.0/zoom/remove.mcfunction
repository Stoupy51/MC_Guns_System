
#> stoupgun:v5.0.0/zoom/remove
#
# @within	stoupgun:v5.0.0/zoom/main
#

data remove storage stoupgun:gun stats.is_zoom
data modify storage stoupgun:input with set value {"item_model":""}
data modify storage stoupgun:input with.item_model set from storage stoupgun:gun stats.models.normal
function stoupgun:v5.0.0/zoom/update_model with storage stoupgun:input with
item modify entity @s weapon.mainhand stoupgun:v5.0.0/update_stats

