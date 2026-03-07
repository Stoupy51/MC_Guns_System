
#> mgs:v5.0.0/mob/apply_inaccuracy
#
# @executed	anchored eyes & facing entity @n[tag=mgs.target] feet
#
# @within	mgs:v5.0.0/mob/fire_weapon
#

# Random yaw offset: -20.0 to +20.0 degrees (stored as -200..200, applied with 0.1 scale)
execute store result storage mgs:temp _rot.yaw double 0.1 run random value -200..200
execute store result storage mgs:temp _rot.pitch double 0.1 run random value -200..200
function mgs:v5.0.0/mob/apply_rotation_offset with storage mgs:temp _rot

