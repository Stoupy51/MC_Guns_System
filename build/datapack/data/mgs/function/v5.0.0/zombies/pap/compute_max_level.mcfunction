
#> mgs:v5.0.0/zombies/pap/compute_max_level
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#			mgs:v5.0.0/zombies/pap/on_free_pap
#

scoreboard players set #pap_max mgs.data 1
execute if data storage mgs:temp _pap_extract.stats.pap_stats.capacity[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.capacity
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.remaining_bullets[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.remaining_bullets
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.reload_time[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.reload_time
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.reload_end[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.reload_end
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.reload_mid[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.reload_mid
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.cooldown[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.cooldown
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.burst[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.burst
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pellet_count[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.pellet_count
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.damage[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.damage
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.decay[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.decay
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_base[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.acc_base
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_sneak[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.acc_sneak
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_walk[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.acc_walk
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_sprint[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.acc_sprint
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.acc_jump[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.acc_jump
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.switch[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.switch
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.kick[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.kick
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.weight[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.weight
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.proj_speed[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.proj_speed
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.proj_gravity[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.proj_gravity
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.proj_lifetime[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.proj_lifetime
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.expl_radius[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.expl_radius
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.expl_damage[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.expl_damage
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.expl_decay[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.expl_decay
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.fire_mode[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.fire_mode
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.can_auto[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.can_auto
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.can_burst[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.can_burst
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pap_name[0] store result score #pap_len mgs.data run data get storage mgs:temp _pap_extract.stats.pap_stats.pap_name
execute if score #pap_len mgs.data > #pap_max mgs.data run scoreboard players operation #pap_max mgs.data = #pap_len mgs.data

