
#> mgs:v5.0.0/mob/apply_inaccuracy
#
# @executed	anchored eyes & facing entity @n[tag=mgs.target] feet
#
# @within	mgs:v5.0.0/mob/fire_weapon
#

# Random yaw offset: -20.00 to +20.00 degrees (stored as -2000..2000, applied with 0.01 scale)
execute store result storage mgs:temp _rot.yaw double 0.01 run random value -2000..2000
execute store result storage mgs:temp _rot.pitch double 0.01 run random value -2000..2000
function mgs:v5.0.0/mob/apply_rotation_offset with storage mgs:temp _rot

