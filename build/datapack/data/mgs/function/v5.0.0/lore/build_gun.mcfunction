
#> mgs:v5.0.0/lore/build_gun
#
# @within	mgs:v5.0.0/utils/update_all_lore with storage mgs:input lore
#
# @args		damage (unknown)
#			remaining (unknown)
#			capacity (unknown)
#			reload_int (unknown)
#			reload_dec (unknown)
#			rate_int (unknown)
#			rate_dec (unknown)
#			decay_pct (unknown)
#			switch_int (unknown)
#			switch_dec (unknown)
#

# Initialize new lore array
data modify storage mgs:temp new_lore set value []

# -- Damage Per Bullet --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates damage
$data modify storage mgs:temp lore_line append value "$(damage)"
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Ammo Remaining (X/Y) --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates ammo
$data modify storage mgs:temp lore_line append value "$(remaining)"
data modify storage mgs:temp lore_line append value {"text":"/","color":"#c77e36"}
$data modify storage mgs:temp lore_line append value "$(capacity)"
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Reloading Time --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates reload
$data modify storage mgs:temp lore_line append value "$(reload_int).$(reload_dec)"
data modify storage mgs:temp lore_line append value {"text":"s","color":"#c77e36"}
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Fire Rate (conditional unit: shots/s or s/shot) --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates fire_rate
$data modify storage mgs:temp lore_line append value "$(rate_int).$(rate_dec) "
execute if score #fire_rate_tenths mgs.data matches 10.. run data modify storage mgs:temp lore_line append from storage mgs:lore_templates fire_rate_sps
execute if score #fire_rate_tenths mgs.data matches ..9 run data modify storage mgs:temp lore_line append from storage mgs:lore_templates fire_rate_spshot
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Pellets Per Shot (optional, only for shotguns) --
execute if score #has_pellets mgs.data matches 1 run function mgs:v5.0.0/lore/append_pellet_line with storage mgs:input lore

# -- Damage Decay --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates decay
$data modify storage mgs:temp lore_line append value "$(decay_pct)"
data modify storage mgs:temp lore_line append value {"text":"%","color":"#c77e36"}
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Switch Time --
data modify storage mgs:temp lore_line set from storage mgs:lore_templates switch_time
$data modify storage mgs:temp lore_line append value "$(switch_int).$(switch_dec)"
data modify storage mgs:temp lore_line append value {"text":"s","color":"#c77e36"}
data modify storage mgs:temp new_lore append from storage mgs:temp lore_line

# -- Empty line separator --
data modify storage mgs:temp new_lore append value ""

