
#> mgs:v5.1.0/tick
#
# @within	mgs:v5.1.0/load/tick_verification
#

# Infinitely incrementing tick counter for general timing purposes
scoreboard players add #total_tick mgs.data 1

# Player loop
execute as @e[type=player,sort=random] at @s run function mgs:v5.1.0/player/tick

# Tick function for slow bullets (projectiles)
execute if score #slow_bullet_count mgs.data matches 1.. as @e[tag=mgs.slow_bullet] at @s run function mgs:v5.1.0/projectile/tick

# Tick function for active grenades
execute if score #grenade_count mgs.data matches 1.. as @e[tag=mgs.grenade] at @s run function mgs:v5.1.0/grenade/tick

# Armed mob AI loop
execute if score #armed_mob_count mgs.data matches 1.. as @e[tag=mgs.armed] at @s run function mgs:v5.1.0/mob/tick

# Resync armed mob count every 5 seconds (mobs dying never decrement the counter)
scoreboard players operation #armed_mob_phase mgs.data = #total_tick mgs.data
scoreboard players operation #armed_mob_phase mgs.data %= #100 mgs.data
execute if score #armed_mob_count mgs.data matches 1.. if score #armed_mob_phase mgs.data matches 0 store result score #armed_mob_count mgs.data if entity @e[tag=mgs.armed]

# Zombies game tick
execute if data storage mgs:zombies game{state:"active"} run function mgs:v5.1.0/zombies/game_tick
execute if data storage mgs:zombies game{state:"preparing"} run function mgs:v5.1.0/zombies/prep_tick

# Multiplayer game tick
execute if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.1.0/multiplayer/game_tick
execute if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.1.0/multiplayer/prep_tick

# Missions game tick
execute if data storage mgs:missions game{state:"active"} run function mgs:v5.1.0/missions/game_tick
execute if data storage mgs:missions game{state:"preparing"} run function mgs:v5.1.0/missions/prep_tick

