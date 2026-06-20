
#> mgs:v5.0.1/zombies/traps/setup_iter
#
# @within	mgs:v5.0.1/zombies/traps/setup
#			mgs:v5.0.1/zombies/traps/setup_iter
#

# Assign incrementing ID
scoreboard players add #trap_counter mgs.data 1

# Read interaction position (relative) and convert to absolute
execute store result score #tix mgs.data run data get storage mgs:temp _trap_iter[0].pos[0]
execute store result score #tiy mgs.data run data get storage mgs:temp _trap_iter[0].pos[1]
execute store result score #tiz mgs.data run data get storage mgs:temp _trap_iter[0].pos[2]
scoreboard players operation #tix mgs.data += #gm_base_x mgs.data
scoreboard players operation #tiy mgs.data += #gm_base_y mgs.data
scoreboard players operation #tiz mgs.data += #gm_base_z mgs.data

# Compute trap effect center from interaction position + offset_pos
execute store result score #tx mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[0]
execute store result score #ty mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[1]
execute store result score #tz mgs.data run data get storage mgs:temp _trap_iter[0].offset_pos[2]
scoreboard players operation #tx mgs.data += #tix mgs.data
scoreboard players operation #ty mgs.data += #tiy mgs.data
scoreboard players operation #tz mgs.data += #tiz mgs.data

# Store positions for macros
execute store result storage mgs:temp _trap.cx int 1 run scoreboard players get #tx mgs.data
execute store result storage mgs:temp _trap.cy int 1 run scoreboard players get #ty mgs.data
execute store result storage mgs:temp _trap.cz int 1 run scoreboard players get #tz mgs.data
execute store result storage mgs:temp _trap.ix int 1 run scoreboard players get #tix mgs.data
execute store result storage mgs:temp _trap.iy int 1 run scoreboard players get #tiy mgs.data
execute store result storage mgs:temp _trap.iz int 1 run scoreboard players get #tiz mgs.data

# Summon entities
function mgs:v5.0.1/zombies/traps/place_at with storage mgs:temp _trap

# Set scoreboards on interaction entity (type is also stored here for the hover text)
scoreboard players operation @n[tag=mgs._trap_new_i] mgs.zb.trap.id = #trap_counter mgs.data
execute store result score @n[tag=mgs._trap_new_i] mgs.zb.trap.price run data get storage mgs:temp _trap_iter[0].price
execute store result score @n[tag=mgs._trap_new_i] mgs.zb.trap.power run data get storage mgs:temp _trap_iter[0].power
execute store result score @n[tag=mgs._trap_new_i] mgs.zb.trap.type run data get storage mgs:temp _trap_iter[0].type
tag @e[tag=mgs._trap_new_i] remove mgs._trap_new_i

# Set scoreboards on marker entity
scoreboard players operation @n[tag=mgs._trap_new_m] mgs.zb.trap.id = #trap_counter mgs.data
execute store result score @n[tag=mgs._trap_new_m] mgs.zb.trap.type run data get storage mgs:temp _trap_iter[0].type
execute store result score @n[tag=mgs._trap_new_m] mgs.zb.trap.dur run data get storage mgs:temp _trap_iter[0].duration
execute store result score @n[tag=mgs._trap_new_m] mgs.zb.trap.cd_max run data get storage mgs:temp _trap_iter[0].cooldown
scoreboard players set @n[tag=mgs._trap_new_m] mgs.zb.trap.timer 0
scoreboard players set @n[tag=mgs._trap_new_m] mgs.zb.trap.cd 0

# Store per-axis effect radius
execute store result score @n[tag=mgs._trap_new_m] mgs.zb.trap.rx run data get storage mgs:temp _trap_iter[0].effect_radius[0]
execute store result score @n[tag=mgs._trap_new_m] mgs.zb.trap.ry run data get storage mgs:temp _trap_iter[0].effect_radius[1]
execute store result score @n[tag=mgs._trap_new_m] mgs.zb.trap.rz run data get storage mgs:temp _trap_iter[0].effect_radius[2]
tag @e[tag=mgs._trap_new_m] remove mgs._trap_new_m

# Register Bookshelf events on interaction entity
execute as @e[tag=mgs._trap_new_bs] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.1/zombies/traps/on_right_click",executor:"source"}
execute as @e[tag=mgs._trap_new_bs] run function #bs.interaction:on_hover {run:"function mgs:v5.0.1/zombies/traps/on_hover",executor:"source"}
tag @e[tag=mgs._trap_new_bs] remove mgs._trap_new_bs

# Turret traps (type 2) get a visible two-part model: a stationary base + a head that aims at its
# target. The head carries this trap's id so turret_fire can find and rotate the matching head.
execute store result score #trap_type mgs.data run data get storage mgs:temp _trap_iter[0].type
data modify storage mgs:temp _trap.yaw set value 0.0f
execute if data storage mgs:temp _trap_iter[0].rotation[0] run data modify storage mgs:temp _trap.yaw set from storage mgs:temp _trap_iter[0].rotation[0]
execute if score #trap_type mgs.data matches 2 run function mgs:v5.0.1/zombies/traps/place_turret_at with storage mgs:temp _trap
execute if score #trap_type mgs.data matches 2 run scoreboard players operation @n[tag=mgs._trap_new_head] mgs.zb.trap.id = #trap_counter mgs.data
execute if score #trap_type mgs.data matches 2 run tag @e[tag=mgs._trap_new_head] remove mgs._trap_new_head

# Continue iteration
data remove storage mgs:temp _trap_iter[0]
execute if data storage mgs:temp _trap_iter[0] run function mgs:v5.0.1/zombies/traps/setup_iter

