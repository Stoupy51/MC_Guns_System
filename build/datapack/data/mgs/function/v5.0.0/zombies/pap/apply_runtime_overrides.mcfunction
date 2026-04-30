
#> mgs:v5.0.0/zombies/pap/apply_runtime_overrides
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#

execute if data storage mgs:temp _pap_extract.stats.pap_stats.capacity run function mgs:v5.0.0/zombies/pap/apply_field/capacity
execute if data storage mgs:temp _pap_extract.stats.pap_stats.remaining_bullets run function mgs:v5.0.0/zombies/pap/apply_field/remaining_bullets
execute if data storage mgs:temp _pap_extract.stats.pap_stats.reload_time run function mgs:v5.0.0/zombies/pap/apply_field/reload_time
execute if data storage mgs:temp _pap_extract.stats.pap_stats.reload_end run function mgs:v5.0.0/zombies/pap/apply_field/reload_end
execute if data storage mgs:temp _pap_extract.stats.pap_stats.reload_mid run function mgs:v5.0.0/zombies/pap/apply_field/reload_mid
execute if data storage mgs:temp _pap_extract.stats.pap_stats.cooldown run function mgs:v5.0.0/zombies/pap/apply_field/cooldown
execute if data storage mgs:temp _pap_extract.stats.pap_stats.burst run function mgs:v5.0.0/zombies/pap/apply_field/burst
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pellet_count run function mgs:v5.0.0/zombies/pap/apply_field/pellet_count
execute if data storage mgs:temp _pap_extract.stats.pap_stats.damage run function mgs:v5.0.0/zombies/pap/apply_field/damage
execute if data storage mgs:temp _pap_extract.stats.pap_stats.decay run function mgs:v5.0.0/zombies/pap/apply_field/decay
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_base run function mgs:v5.0.0/zombies/pap/apply_field/acc_base
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_sneak run function mgs:v5.0.0/zombies/pap/apply_field/acc_sneak
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_walk run function mgs:v5.0.0/zombies/pap/apply_field/acc_walk
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_sprint run function mgs:v5.0.0/zombies/pap/apply_field/acc_sprint
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_jump run function mgs:v5.0.0/zombies/pap/apply_field/acc_jump
execute if data storage mgs:temp _pap_extract.stats.pap_stats.switch run function mgs:v5.0.0/zombies/pap/apply_field/switch
execute if data storage mgs:temp _pap_extract.stats.pap_stats.kick run function mgs:v5.0.0/zombies/pap/apply_field/kick
execute if data storage mgs:temp _pap_extract.stats.pap_stats.weight run function mgs:v5.0.0/zombies/pap/apply_field/weight
execute if data storage mgs:temp _pap_extract.stats.pap_stats.proj_speed run function mgs:v5.0.0/zombies/pap/apply_field/proj_speed
execute if data storage mgs:temp _pap_extract.stats.pap_stats.proj_gravity run function mgs:v5.0.0/zombies/pap/apply_field/proj_gravity
execute if data storage mgs:temp _pap_extract.stats.pap_stats.proj_lifetime run function mgs:v5.0.0/zombies/pap/apply_field/proj_lifetime
execute if data storage mgs:temp _pap_extract.stats.pap_stats.expl_radius run function mgs:v5.0.0/zombies/pap/apply_field/expl_radius
execute if data storage mgs:temp _pap_extract.stats.pap_stats.expl_damage run function mgs:v5.0.0/zombies/pap/apply_field/expl_damage
execute if data storage mgs:temp _pap_extract.stats.pap_stats.expl_decay run function mgs:v5.0.0/zombies/pap/apply_field/expl_decay
execute if data storage mgs:temp _pap_extract.stats.pap_stats.fire_mode run function mgs:v5.0.0/zombies/pap/apply_field/fire_mode
execute if data storage mgs:temp _pap_extract.stats.pap_stats.can_auto run function mgs:v5.0.0/zombies/pap/apply_field/can_auto
execute if data storage mgs:temp _pap_extract.stats.pap_stats.can_burst run function mgs:v5.0.0/zombies/pap/apply_field/can_burst

