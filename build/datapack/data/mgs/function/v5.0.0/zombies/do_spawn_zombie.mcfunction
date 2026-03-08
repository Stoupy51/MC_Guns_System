
#> mgs:v5.0.0/zombies/do_spawn_zombie
#
# @within	mgs:v5.0.0/zombies/spawn_zombie_at_idx
#

# Read relative position
execute store result score #_zx mgs.data run data get storage mgs:temp _zs_iter[0][0]
execute store result score #_zy mgs.data run data get storage mgs:temp _zs_iter[0][1]
execute store result score #_zz mgs.data run data get storage mgs:temp _zs_iter[0][2]

# Convert to absolute
scoreboard players operation #_zx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_zy mgs.data += #gm_base_y mgs.data
scoreboard players operation #_zz mgs.data += #gm_base_z mgs.data

# Store absolute position for macro
execute store result storage mgs:temp _zpos.x double 1 run scoreboard players get #_zx mgs.data
execute store result storage mgs:temp _zpos.y double 1 run scoreboard players get #_zy mgs.data
execute store result storage mgs:temp _zpos.z double 1 run scoreboard players get #_zz mgs.data

# Determine zombie level based on round
# Rounds 1-5: level 1, 6-10: level 2, 11-15: level 3, 16+: level 4
execute if score #zb_round mgs.data matches ..5 run data modify storage mgs:temp _zpos.level set value "1"
execute if score #zb_round mgs.data matches 6..10 run data modify storage mgs:temp _zpos.level set value "2"
execute if score #zb_round mgs.data matches 11..15 run data modify storage mgs:temp _zpos.level set value "3"
execute if score #zb_round mgs.data matches 16.. run data modify storage mgs:temp _zpos.level set value "4"

# Spawn the zombie
function mgs:v5.0.0/zombies/summon_zombie_at with storage mgs:temp _zpos

