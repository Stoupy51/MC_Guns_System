
#> mgs:v5.1.0/mob/apply_inaccuracy
#
# @executed	anchored eyes & facing entity @e[tag=mgs.target,limit=1] feet
#
# @within	mgs:v5.1.0/mob/fire_weapon
#

# -20 to +20 degrees (-200..200 at 0.1).
execute store result storage mgs:temp _rot.yaw double 0.1 run random value -200..200
execute store result storage mgs:temp _rot.pitch double 0.1 run random value -200..200
function mgs:v5.1.0/mob/apply_rotation_offset with storage mgs:temp _rot

