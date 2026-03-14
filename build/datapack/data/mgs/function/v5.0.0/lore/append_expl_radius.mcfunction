
#> mgs:v5.0.0/lore/append_expl_radius
#
# @within	mgs:v5.0.0/lore/build_grenade with storage mgs:input lore
#
# @args		expl_radius (unknown)
#

data modify storage mgs:temp lore_line set from storage mgs:lore_templates expl_radius
$data modify storage mgs:temp lore_line append value "$(expl_radius)"
data modify storage mgs:temp lore_line append value [{"text":" ","color":"#c77e36"}, {"translate":"mgs.blocks"}]
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

