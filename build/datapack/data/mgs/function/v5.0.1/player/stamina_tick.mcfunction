
#> mgs:v5.0.1/player/stamina_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/tick
#

# First tick in this game (or a fresh late-joiner / respawn): start at full stamina. stam_seen is
# reset to 0 at game start (see regen_enable_lines) and on respawn/revive, so this re-inits then.
execute if score @s mgs.stam_seen matches 0 run function mgs:v5.0.1/player/stamina_init

# Max stamina = base + perk bonus (Stamin-Up doubles the endurance budget); clamp current to it
scoreboard players set @s mgs.stam_max 200
scoreboard players operation @s mgs.stam_max += @s mgs.stam_bonus
scoreboard players operation @s mgs.stam < @s mgs.stam_max

# Detect sprinting via the is_sprinting entity flag: unlike the sprint_one_cm stat (which only
# increments on the ground), the flag stays set through the whole jump arc, so jump-sprinting
# drains exactly like ground sprinting
scoreboard players set #stam_sprinting mgs.data 0
execute if predicate mgs:v5.0.1/is_sprinting run scoreboard players set #stam_sprinting mgs.data 1

# Sprinting → drain stamina and (re)arm the rest delay before regen can start
execute if score #stam_sprinting mgs.data matches 1 run scoreboard players remove @s mgs.stam 2
execute if score #stam_sprinting mgs.data matches 1 run scoreboard players set @s mgs.stam_rest 20

# Resting → count down the delay, then regen stamina
execute if score #stam_sprinting mgs.data matches 0 if score @s mgs.stam_rest matches 1.. run scoreboard players remove @s mgs.stam_rest 1
execute if score #stam_sprinting mgs.data matches 0 if score @s mgs.stam_rest matches 0 run scoreboard players add @s mgs.stam 2

# Clamp 0..max
execute if score @s mgs.stam matches ..-1 run scoreboard players set @s mgs.stam 0
scoreboard players operation @s mgs.stam < @s mgs.stam_max

# Become winded when stamina hits 0; silently recover once it regenerates past the hysteresis
# threshold. No sound, no "out of breath" message — the empty bar is the feedback (stamina.md).
execute if score @s mgs.stam_out matches 0 if score @s mgs.stam matches 0 run scoreboard players set @s mgs.stam_out 1
execute if score @s mgs.stam_out matches 1 if score @s mgs.stam matches 80.. run scoreboard players set @s mgs.stam_out 0

# Map stamina to the hunger-bar target (6..20); winded → held at the no-sprint level
scoreboard players operation #stam_t mgs.data = @s mgs.stam
scoreboard players operation #stam_t mgs.data *= #14 mgs.data
scoreboard players operation #stam_t mgs.data /= @s mgs.stam_max
scoreboard players add #stam_t mgs.data 6
execute if score @s mgs.stam_out matches 1 run scoreboard players set #stam_t mgs.data 6

# Nudge the visible bar toward the target
function mgs:v5.0.1/player/stamina_bar

