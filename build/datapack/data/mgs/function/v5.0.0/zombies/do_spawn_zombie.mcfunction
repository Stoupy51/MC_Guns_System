
#> mgs:v5.0.0/zombies/do_spawn_zombie
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/spawn_zombie [ as @n[tag=mgs.zb_near,sort=random] & at @s ]
#

# Store position for macro
execute store result storage mgs:temp _zpos.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _zpos.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _zpos.z double 1 run data get entity @s Pos[2]

# Determine zombie level based on round
# Rounds 1-5: level 1, 6-10: level 2, 11-15: level 3, 16+: level 4
execute if score #zb_round mgs.data matches ..5 run data modify storage mgs:temp _zpos.level set value "1"
execute if score #zb_round mgs.data matches 6..10 run data modify storage mgs:temp _zpos.level set value "2"
execute if score #zb_round mgs.data matches 11..15 run data modify storage mgs:temp _zpos.level set value "3"
execute if score #zb_round mgs.data matches 16.. run data modify storage mgs:temp _zpos.level set value "4"

# Spawn the zombie
function mgs:v5.0.0/zombies/summon_zombie_at with storage mgs:temp _zpos

