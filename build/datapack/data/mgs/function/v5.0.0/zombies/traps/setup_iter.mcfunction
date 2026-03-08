
#> mgs:v5.0.0/zombies/traps/setup_iter
#
# @within	mgs:v5.0.0/zombies/traps/setup
#			mgs:v5.0.0/zombies/traps/setup_iter
#

# Assign incrementing ID
scoreboard players add #_trap_counter mgs.data 1

# Read trap center position (relative) and convert to absolute
execute store result score #_tx mgs.data run data get storage mgs:temp _trap_iter[0].pos[0]
execute store result score #_ty mgs.data run data get storage mgs:temp _trap_iter[0].pos[1]
execute store result score #_tz mgs.data run data get storage mgs:temp _trap_iter[0].pos[2]
scoreboard players operation #_tx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_ty mgs.data += #gm_base_y mgs.data
scoreboard players operation #_tz mgs.data += #gm_base_z mgs.data

# Compute interaction entity position (trap center + offset_pos)
execute store result score #_tix mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[0]
execute store result score #_tiy mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[1]
execute store result score #_tiz mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[2]
scoreboard players operation #_tix mgs.data += #_tx mgs.data
scoreboard players operation #_tiy mgs.data += #_ty mgs.data
scoreboard players operation #_tiz mgs.data += #_tz mgs.data

# Store positions for macros
execute store result storage mgs:temp _trap.cx int 1 run scoreboard players get #_tx mgs.data
execute store result storage mgs:temp _trap.cy int 1 run scoreboard players get #_ty mgs.data
execute store result storage mgs:temp _trap.cz int 1 run scoreboard players get #_tz mgs.data
execute store result storage mgs:temp _trap.ix int 1 run scoreboard players get #_tix mgs.data
execute store result storage mgs:temp _trap.iy int 1 run scoreboard players get #_tiy mgs.data
execute store result storage mgs:temp _trap.iz int 1 run scoreboard players get #_tiz mgs.data

# Summon entities
function mgs:v5.0.0/zombies/traps/place_at with storage mgs:temp _trap

# Set scoreboards on interaction entity
scoreboard players operation @n[tag=_trap_new_i] mgs.zb.trap.id = #_trap_counter mgs.data
execute store result score @n[tag=_trap_new_i] mgs.zb.trap.price run data get storage mgs:temp _trap_iter[0].price
execute store result score @n[tag=_trap_new_i] mgs.zb.trap.power run data get storage mgs:temp _trap_iter[0].power
tag @e[tag=_trap_new_i] remove _trap_new_i

# Set scoreboards on marker entity
scoreboard players operation @n[tag=_trap_new_m] mgs.zb.trap.id = #_trap_counter mgs.data
execute store result score @n[tag=_trap_new_m] mgs.zb.trap.type run data get storage mgs:temp _trap_iter[0].type
execute store result score @n[tag=_trap_new_m] mgs.zb.trap.dur run data get storage mgs:temp _trap_iter[0].duration
execute store result score @n[tag=_trap_new_m] mgs.zb.trap.cd_max run data get storage mgs:temp _trap_iter[0].cooldown
scoreboard players set @n[tag=_trap_new_m] mgs.zb.trap.timer 0
scoreboard players set @n[tag=_trap_new_m] mgs.zb.trap.cd 0

# Compute max radius from effect_radius
execute store result score #_tr_x mgs.data run data get storage mgs:temp _trap_iter[0].effect_radius[0]
execute store result score #_tr_y mgs.data run data get storage mgs:temp _trap_iter[0].effect_radius[1]
execute store result score #_tr_z mgs.data run data get storage mgs:temp _trap_iter[0].effect_radius[2]
scoreboard players operation #_tr_max mgs.data = #_tr_x mgs.data
execute if score #_tr_y mgs.data > #_tr_max mgs.data run scoreboard players operation #_tr_max mgs.data = #_tr_y mgs.data
execute if score #_tr_z mgs.data > #_tr_max mgs.data run scoreboard players operation #_tr_max mgs.data = #_tr_z mgs.data
scoreboard players operation @n[tag=_trap_new_m] mgs.zb.trap.radius = #_tr_max mgs.data
tag @e[tag=_trap_new_m] remove _trap_new_m

# Register Bookshelf events on interaction entity
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/traps/on_right_click",executor:"source"}
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_hover_enter {run:"function mgs:v5.0.0/zombies/traps/on_hover_enter",executor:"source"}
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_hover_leave {run:"function mgs:v5.0.0/zombies/traps/on_hover_leave",executor:"source"}
tag @e[tag=_trap_new_bs] remove _trap_new_bs

# Continue iteration
data remove storage mgs:temp _trap_iter[0]
execute if data storage mgs:temp _trap_iter[0] run function mgs:v5.0.0/zombies/traps/setup_iter

