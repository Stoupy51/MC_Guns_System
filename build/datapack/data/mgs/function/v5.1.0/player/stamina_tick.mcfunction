
#> mgs:v5.1.0/player/stamina_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Full stamina on the first tick of a game, a late join, a respawn or a revive: stam_seen is reset to 0 on each.
execute if score @s mgs.stam_seen matches 0 run function mgs:v5.1.0/player/stamina_init

# Base + perk bonus (Stamin-Up doubles it); the current value is clamped to it.
scoreboard players set @s mgs.stam_max 300
scoreboard players operation @s mgs.stam_max += @s mgs.stam_bonus
scoreboard players operation @s mgs.stam < @s mgs.stam_max

# The is_sprinting flag, unlike the sprint_one_cm stat (ground only), stays set through a jump, so jump-sprinting drains the same.
scoreboard players set #stam_sprinting mgs.data 0
execute if predicate mgs:v5.1.0/is_sprinting run scoreboard players set #stam_sprinting mgs.data 1

# Swimming costs 1/5 of the sprint rate: the swim pose needs sprint held, and a full rate emptied the bar before any water was crossed.
scoreboard players set #stam_swimming mgs.data 0
execute if predicate mgs:v5.1.0/is_swimming run scoreboard players set #stam_swimming mgs.data 1

# Sprinting drains and re-arms the delay before regen.
execute if score #stam_sprinting mgs.data matches 1 if score #stam_swimming mgs.data matches 0 run scoreboard players remove @s mgs.stam 2
execute if score #stam_sprinting mgs.data matches 1 if score #stam_swimming mgs.data matches 1 run function mgs:v5.1.0/player/stamina_swim_drain
execute if score #stam_sprinting mgs.data matches 1 run scoreboard players set @s mgs.stam_rest 20

# At rest, the delay counts down, then stamina regenerates.
execute if score #stam_sprinting mgs.data matches 0 if score @s mgs.stam_rest matches 1.. run scoreboard players remove @s mgs.stam_rest 1
execute if score #stam_sprinting mgs.data matches 0 if score @s mgs.stam_rest matches 0 run scoreboard players add @s mgs.stam 3

execute if score @s mgs.stam matches ..-1 run scoreboard players set @s mgs.stam 0
scoreboard players operation @s mgs.stam < @s mgs.stam_max

# Winded at 0, recovered silently past the hysteresis threshold: the empty bar is the only feedback.
execute if score @s mgs.stam_out matches 0 if score @s mgs.stam matches 0 run scoreboard players set @s mgs.stam_out 1
execute if score @s mgs.stam_out matches 1 if score @s mgs.stam matches 120.. run scoreboard players set @s mgs.stam_out 0

# Stamina to the hunger bar target (6..20); winded holds it at the no-sprint level.
scoreboard players operation #stam_t mgs.data = @s mgs.stam
scoreboard players operation #stam_t mgs.data *= #14 mgs.data
scoreboard players operation #stam_t mgs.data /= @s mgs.stam_max
scoreboard players add #stam_t mgs.data 6
execute if score @s mgs.stam_out matches 1 run scoreboard players set #stam_t mgs.data 6

function mgs:v5.1.0/player/stamina_bar

