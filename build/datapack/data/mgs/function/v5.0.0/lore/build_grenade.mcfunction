
#> mgs:v5.0.0/lore/build_grenade
#
# @within	mgs:v5.0.0/utils/update_all_lore with storage mgs:input lore
#
# @args		type_display (unknown)
#			fuse_int (unknown)
#			fuse_dec (unknown)
#

# Initialize new lore array
data modify storage mgs:temp new_lore set value []

# -- Type --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates grenade_type
$data modify storage mgs:temp lore_line append value "$(type_display)"
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Explosion Damage (optional) --
execute if score #has_expl_damage mgs.data matches 1 run function mgs:v5.0.0/lore/append_expl_damage with storage mgs:input lore

# -- Explosion Radius (optional) --
execute if score #has_expl_radius mgs.data matches 1 run function mgs:v5.0.0/lore/append_expl_radius with storage mgs:input lore

# -- Fuse Time --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates grenade_fuse
$data modify storage mgs:temp lore_line append value "$(fuse_int).$(fuse_dec)"
data modify storage mgs:temp lore_line append value {"text":"s","color":"#c77e36"}
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Empty line separator --
data modify storage mgs:temp new_lore append value ""

