
#> mgs:v5.1.0/actionbar/show
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Idle gate: everything on the bar (ammo, cooldown dot, fire mode, dps) can only change while
# the weapon is in use, so while idle we refresh every 10 ticks instead of rebuilding the whole
# bar (~50 commands + a macro parse) every tick. ab_force (set by the fire-mode toggle) forces
# an immediate refresh for changes the use-detection below can't see.
scoreboard players set #ab_active mgs.data 0
execute if score @s mgs.cooldown > #total_tick mgs.data run scoreboard players set #ab_active mgs.data 1
execute if score @s mgs.pending_clicks matches 0.. run scoreboard players set #ab_active mgs.data 1
execute if score @s mgs.previous_dps matches 1.. run scoreboard players set #ab_active mgs.data 1
execute if score @s mgs.ab_force matches 1 run scoreboard players set #ab_active mgs.data 1
scoreboard players operation #ab_phase mgs.data = #total_tick mgs.data
scoreboard players operation #ab_phase mgs.data %= #10 mgs.data
execute if score #ab_active mgs.data matches 0 unless score #ab_phase mgs.data matches 0 run return 0
scoreboard players set @s mgs.ab_force 0

# Initialize actionbar with fire mode indicator
function mgs:v5.1.0/actionbar/build_fire_mode_indicator

# Add cooldown ready indicator
function mgs:v5.1.0/actionbar/add_cooldown_indicator

# Get capacity and remaining bullets
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute store result score #remaining mgs.data run scoreboard players get @s mgs.remaining_bullets

# Add separator between fire mode and ammo
data modify storage mgs:temp actionbar.list append value " "

# Check if capacity > 15 (use numeric display) or <= 15 (use icons)
execute if score #capacity mgs.data matches 16.. run function mgs:v5.1.0/actionbar/add_numeric_ammo
execute if score #capacity mgs.data matches ..15 run function mgs:v5.1.0/actionbar/add_icon_ammo

# Add DPS display
function mgs:v5.1.0/actionbar/add_dps

# Display actionbar
function mgs:v5.1.0/actionbar/display with storage mgs:temp actionbar

