
#> mgs:v5.0.1/player/stamina_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/tick
#

# First tick in this game (or a fresh late-joiner): start at full stamina. stam_seen is reset to 0
# for everyone at game start (see regen_enable_lines), so this re-inits every game.
execute if score @s mgs.stam_seen matches 0 run function mgs:v5.0.1/player/stamina_init

# Detect sprinting via the distance-sprinted stat delta (cm gained since last tick)
scoreboard players operation #stam_delta mgs.data = @s mgs.sprint
scoreboard players operation #stam_delta mgs.data -= @s mgs.stam_prev
scoreboard players operation @s mgs.stam_prev = @s mgs.sprint

# Sprinting → drain stamina and (re)arm the rest delay before regen can start
execute if score #stam_delta mgs.data matches 1.. run scoreboard players remove @s mgs.stam 2
execute if score #stam_delta mgs.data matches 1.. run scoreboard players set @s mgs.stam_rest 20

# Resting → count down the delay, then regen stamina
execute if score #stam_delta mgs.data matches ..0 if score @s mgs.stam_rest matches 1.. run scoreboard players remove @s mgs.stam_rest 1
execute if score #stam_delta mgs.data matches ..0 if score @s mgs.stam_rest matches 0 run scoreboard players add @s mgs.stam 1

# Clamp 0..MAX
execute if score @s mgs.stam matches ..-1 run scoreboard players set @s mgs.stam 0
execute if score @s mgs.stam matches 101.. run scoreboard players set @s mgs.stam 100

# Become winded when stamina hits 0; recover once it regenerates back past the hysteresis threshold
execute if score @s mgs.stam_out matches 0 if score @s mgs.stam matches 0 run function mgs:v5.0.1/player/stamina_wind
execute if score @s mgs.stam_out matches 1 if score @s mgs.stam matches 40.. run function mgs:v5.0.1/player/stamina_recover

# Not winded → keep the hunger bar full while stamina remains. Vanilla sprint exhaustion slowly
# drains real food, which would otherwise lock sprint before OUR meter is actually empty.
execute if score @s mgs.stam_out matches 0 store result score #stam_food mgs.data run data get entity @s foodLevel
execute if score @s mgs.stam_out matches 0 if score #stam_food mgs.data matches ..19 run effect give @s minecraft:saturation 1 20 true

# While winded, hold the hunger bar at the no-sprint level (foodLevel <= 6). Push down with a short
# hunger pulse while it's still above 6, and clear it once at/below 6 so it can't drain to starvation.
execute if score @s mgs.stam_out matches 1 run function mgs:v5.0.1/player/stamina_hold

