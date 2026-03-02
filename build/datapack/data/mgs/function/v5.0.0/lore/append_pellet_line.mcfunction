
#> mgs:v5.0.0/lore/append_pellet_line
#
# @within	mgs:v5.0.0/lore/build_gun with storage mgs:input lore
#
# @args		pellets (unknown)
#

data modify storage mgs:temp lore_line set from storage mgs:lore_templates pellets
$data modify storage mgs:temp lore_line append value "$(pellets)"
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

