
#> mgs:v5.0.0/tick
#
# @within	mgs:v5.0.0/load/tick_verification
#

# Player loop
execute as @e[type=player,sort=random] at @s run function mgs:v5.0.0/player/tick

# Tick function for slow bullets (projectiles)
execute if score #slow_bullet_count mgs.data matches 1.. as @e[tag=mgs.slow_bullet] at @s run function mgs:v5.0.0/projectile/tick

# Tick function for active grenades
execute if score #grenade_count mgs.data matches 1.. as @e[tag=mgs.grenade] at @s run function mgs:v5.0.0/grenade/tick

# Armed mob AI loop
execute if score #armed_mob_count mgs.data matches 1.. as @e[tag=mgs.armed] at @s run function mgs:v5.0.0/mob/tick

# Multiplayer game tick
execute if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.0.0/multiplayer/game_tick
execute if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.0.0/multiplayer/prep_tick

