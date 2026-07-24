
#> mgs:v5.1.0/zombies/pap/apply_field
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"capacity"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"remaining_bullets"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"reload_time"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"reload_end"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"reload_mid"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"cooldown"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"burst"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"pellet_count"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"damage"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"decay"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"acc_base"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"acc_sneak"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"acc_walk"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"acc_sprint"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"acc_jump"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"switch"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"kick"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"weight"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"speed_multiply_base"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"proj_speed"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"proj_gravity"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"proj_lifetime"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"expl_radius"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"expl_damage"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"expl_decay"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"fire_mode"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"can_auto"}
#			mgs:v5.1.0/zombies/pap/apply_runtime_overrides {field:"can_burst"}
#
# @args		field (string)
#

$data modify storage mgs:temp _pap_pick.list set from storage mgs:temp _pap_extract.stats.pap_stats.$(field)
execute if data storage mgs:temp _pap_pick.list[0] run function mgs:v5.1.0/zombies/pap/pick_list_value
$execute if data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.stats.$(field) set from storage mgs:temp _pap_pick.value
$execute unless data storage mgs:temp _pap_pick.list[0] run data modify storage mgs:temp _pap_extract.stats.$(field) set from storage mgs:temp _pap_extract.stats.pap_stats.$(field)

