
#> mgs:v5.0.0/zombies/pap/pick_list_value
#
# @within	mgs:v5.0.0/zombies/pap/apply_field/capacity
#			mgs:v5.0.0/zombies/pap/apply_field/remaining_bullets
#			mgs:v5.0.0/zombies/pap/apply_field/reload_time
#			mgs:v5.0.0/zombies/pap/apply_field/reload_end
#			mgs:v5.0.0/zombies/pap/apply_field/reload_mid
#			mgs:v5.0.0/zombies/pap/apply_field/cooldown
#			mgs:v5.0.0/zombies/pap/apply_field/burst
#			mgs:v5.0.0/zombies/pap/apply_field/pellet_count
#			mgs:v5.0.0/zombies/pap/apply_field/damage
#			mgs:v5.0.0/zombies/pap/apply_field/decay
#			mgs:v5.0.0/zombies/pap/apply_field/acc_base
#			mgs:v5.0.0/zombies/pap/apply_field/acc_sneak
#			mgs:v5.0.0/zombies/pap/apply_field/acc_walk
#			mgs:v5.0.0/zombies/pap/apply_field/acc_sprint
#			mgs:v5.0.0/zombies/pap/apply_field/acc_jump
#			mgs:v5.0.0/zombies/pap/apply_field/switch
#			mgs:v5.0.0/zombies/pap/apply_field/kick
#			mgs:v5.0.0/zombies/pap/apply_field/proj_speed
#			mgs:v5.0.0/zombies/pap/apply_field/proj_gravity
#			mgs:v5.0.0/zombies/pap/apply_field/proj_lifetime
#			mgs:v5.0.0/zombies/pap/apply_field/expl_radius
#			mgs:v5.0.0/zombies/pap/apply_field/expl_damage
#			mgs:v5.0.0/zombies/pap/apply_field/expl_decay
#			mgs:v5.0.0/zombies/pap/resolve_runtime_name
#

scoreboard players set #pap_pick_i mgs.data 0
data modify storage mgs:temp _pap_pick.value set from storage mgs:temp _pap_pick.list[0]
function mgs:v5.0.0/zombies/pap/pick_list_value_step

