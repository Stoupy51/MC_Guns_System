
#> mgs:v5.0.0/zombies/traps/setup_iter
#
# @within	mgs:v5.0.0/zombies/traps/setup
#			mgs:v5.0.0/zombies/traps/setup_iter
#

# Assign incrementing ID
scoreboard players add #trap_counter mgs.data 1

# Read trap center position (relative) and convert to absolute
execute store result score #tx mgs.data run data get storage mgs:temp _trap_iter[0].pos[0]
execute store result score #ty mgs.data run data get storage mgs:temp _trap_iter[0].pos[1]
execute store result score #tz mgs.data run data get storage mgs:temp _trap_iter[0].pos[2]
scoreboard players operation #tx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ty mgs.data += #gm_base_y mgs.data
scoreboard players operation #tz mgs.data += #gm_base_z mgs.data

# Compute interaction entity position (trap center + offset_pos)
execute store result score #tix mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[0]
execute store result score #tiy mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[1]
execute store result score #tiz mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[2]
scoreboard players operation #tix mgs.data += #tx mgs.data
scoreboard players operation #tiy mgs.data += #ty mgs.data
scoreboard players operation #tiz mgs.data += #tz mgs.data

# Store positions for macros
execute store result storage mgs:temp _trap.cx int 1 run scoreboard players get #tx mgs.data
execute store result storage mgs:temp _trap.cy int 1 run scoreboard players get #ty mgs.data
execute store result storage mgs:temp _trap.cz int 1 run scoreboard players get #tz mgs.data
execute store result storage mgs:temp _trap.ix int 1 run scoreboard players get #tix mgs.data
execute store result storage mgs:temp _trap.iy int 1 run scoreboard players get #tiy mgs.data
execute store result storage mgs:temp _trap.iz int 1 run scoreboard players get #tiz mgs.data

# Summon entities
function mgs:v5.0.0/zombies/traps/place_at with storage mgs:temp _trap

# Set scoreboards on interaction entity
scoreboard players operation @n[tag=_trap_new_i] mgs.zb.trap.id = #trap_counter mgs.data
execute store result score @n[tag=_trap_new_i] mgs.zb.trap.price run data get storage mgs:temp _trap_iter[0].price
execute store result score @n[tag=_trap_new_i] mgs.zb.trap.power run data get storage mgs:temp _trap_iter[0].power
tag @e[tag=_trap_new_i] remove _trap_new_i

# Set scoreboards on marker entity
scoreboard players operation @n[tag=_trap_new_m] mgs.zb.trap.id = #trap_counter mgs.data
execute store result score @n[tag=_trap_new_m] mgs.zb.trap.type run data get storage mgs:temp _trap_iter[0].type
execute store result score @n[tag=_trap_new_m] mgs.zb.trap.dur run data get storage mgs:temp _trap_iter[0].duration
execute store result score @n[tag=_trap_new_m] mgs.zb.trap.cd_max run data get storage mgs:temp _trap_iter[0].cooldown
scoreboard players set @n[tag=_trap_new_m] mgs.zb.trap.timer 0
scoreboard players set @n[tag=_trap_new_m] mgs.zb.trap.cd 0

# Compute max radius from effect_radius
execute store result score #tr_x mgs.data run data get storage mgs:temp _trap_iter[0].effect_radius[0]
execute store result score #tr_y mgs.data run data get storage mgs:temp _trap_iter[0].effect_radius[1]
execute store result score #tr_z mgs.data run data get storage mgs:temp _trap_iter[0].effect_radius[2]
scoreboard players operation #tr_max mgs.data = #tr_x mgs.data
execute if score #tr_y mgs.data > #tr_max mgs.data run scoreboard players operation #tr_max mgs.data = #tr_y mgs.data
execute if score #tr_z mgs.data > #tr_max mgs.data run scoreboard players operation #tr_max mgs.data = #tr_z mgs.data
scoreboard players operation @n[tag=_trap_new_m] mgs.zb.trap.radius = #tr_max mgs.data
tag @e[tag=_trap_new_m] remove _trap_new_m

# Register Bookshelf events on interaction entity
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/traps/on_right_click",executor:"source"}
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_hover_enter {run:"function mgs:v5.0.0/zombies/traps/on_hover_enter",executor:"source"}
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_hover_leave {run:"function mgs:v5.0.0/zombies/traps/on_hover_leave",executor:"source"}
tag @e[tag=_trap_new_bs] remove _trap_new_bs

# Continue iteration
data remove storage mgs:temp _trap_iter[0]
execute if data storage mgs:temp _trap_iter[0] run function mgs:v5.0.0/zombies/traps/setup_iter

