
#> mgs:v5.0.0/lore/append_expl_damage
#
# @within	mgs:v5.0.0/lore/build_grenade with storage mgs:input lore
#
# @args		expl_damage (unknown)
#

data modify storage mgs:temp lore_line set from storage mgs:lore_templates expl_damage
$data modify storage mgs:temp lore_line append value "$(expl_damage)"
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

