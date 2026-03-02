
#> mgs:v5.0.0/grenade/on_bounce
#
# @within	???
#

# Apply damped bounce (reduce velocity and reverse direction on collision axis)
function #bs.move:callback/damped_bounce

# Play bounce sound
playsound minecraft:entity.item.pickup player @a[distance=..32] ~ ~ ~ 0.5 0.5

