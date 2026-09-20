
#> mgs:v5.1.0/lore/append_fire_rate_line
#
# @within	mgs:v5.1.0/lore/build_gun with storage mgs:input lore
#
# @args		rate_int (unknown)
#			rate_dec (unknown)
#

data modify storage mgs:temp lore_line set from storage mgs:lore_templates fire_rate
$data modify storage mgs:temp lore_line append value "$(rate_int).$(rate_dec) "
execute if score #fire_rate_tenths mgs.data matches 10.. run data modify storage mgs:temp lore_line append from storage mgs:lore_templates fire_rate_sps
execute if score #fire_rate_tenths mgs.data matches ..9 run data modify storage mgs:temp lore_line append from storage mgs:lore_templates fire_rate_spshot
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

