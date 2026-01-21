
#> mgs:v5.0.0/actionbar/show
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Initialize actionbar with fire mode indicator
function mgs:v5.0.0/actionbar/build_fire_mode_indicator

# Get capacity and remaining bullets
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute store result score #remaining mgs.data run scoreboard players get @s mgs.remaining_bullets

# Add separator between fire mode and ammo
data modify storage mgs:temp actionbar.list append value {"text":" "}

# Check if capacity > 15 (use numeric display) or <= 15 (use icons)
execute if score #capacity mgs.data matches 16.. run function mgs:v5.0.0/actionbar/add_numeric_ammo
execute if score #capacity mgs.data matches ..15 run function mgs:v5.0.0/actionbar/add_icon_ammo

# Display actionbar
function mgs:v5.0.0/actionbar/display with storage mgs:temp actionbar

