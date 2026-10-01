
#> mgs:v5.1.0/grenade/detonate_flash
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/detonate
#

playsound minecraft:entity.firework_rocket.blast player @a[distance=..32] ~ ~ ~ 2 2
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..16] ~ ~ ~ 0.3 2

particle flash{color:[1.0,1.0,1.0,1.0]} ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]
particle end_rod ~ ~ ~ 1 1 1 0.1 50 force @a[distance=..64]

# For the visibility checks.
tag @s add mgs.flash_source

function mgs:v5.1.0/grenade/flash_apply

tag @s remove mgs.flash_source

data modify storage mgs:signals on_explosion set value {}
data modify storage mgs:signals on_explosion.config set from entity @s data.config
data modify storage mgs:signals on_explosion.position set from entity @s Pos
data modify storage mgs:signals on_explosion.grenade set value true
function #mgs:signals/on_explosion

function mgs:v5.1.0/grenade/delete

