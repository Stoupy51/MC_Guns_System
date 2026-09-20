
#> mgs:v5.1.0/zombies/perks/electric_cherry_shock
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/electric_cherry_on_reload [ at @s ]
#			mgs:v5.1.0/zombies/revive/on_down [ at @s ]
#

# Feedback
particle minecraft:electric_spark ~ ~1 ~ 2 1 2 0.25 80 force @a[distance=..48]
particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..32] ~ ~ ~ 0.6 1.6
playsound minecraft:block.beacon.deactivate player @a[distance=..24] ~ ~ ~ 0.6 2

# Radius (blocks x1000): 2500 + 3500 * used/cap  ->  2.5 .. 6.0 blocks
scoreboard players operation #ec_r mgs.data = #ec_used mgs.data
scoreboard players operation #ec_r mgs.data *= #3500 mgs.data
scoreboard players operation #ec_r mgs.data /= #ec_cap mgs.data
scoreboard players add #ec_r mgs.data 2500
execute store result storage mgs:temp _ec.radius float 0.001 run scoreboard players get #ec_r mgs.data

# Damage as a fraction of each zombie's max health (percent x0.01): 40 + 60 * used/cap  ->  0.40 .. 1.00
scoreboard players operation #ec_frac mgs.data = #ec_used mgs.data
scoreboard players operation #ec_frac mgs.data *= #60 mgs.data
scoreboard players operation #ec_frac mgs.data /= #ec_cap mgs.data
scoreboard players add #ec_frac mgs.data 40
execute store result storage mgs:temp _ec.scale double 0.01 run scoreboard players get #ec_frac mgs.data

function mgs:v5.1.0/zombies/perks/electric_cherry_damage with storage mgs:temp _ec

