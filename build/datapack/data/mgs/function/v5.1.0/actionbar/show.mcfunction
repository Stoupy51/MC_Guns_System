
#> mgs:v5.1.0/actionbar/show
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Everything on the bar only changes while the weapon is in use, so idle refreshes every 10 ticks instead of every tick
# (~50 commands and a macro parse); ab_force (fire-mode toggle) forces a refresh the use detection cannot see.
scoreboard players set #ab_active mgs.data 0
execute if score @s mgs.cooldown > #total_tick mgs.data run scoreboard players set #ab_active mgs.data 1
execute if score @s mgs.pending_clicks matches 0.. run scoreboard players set #ab_active mgs.data 1
execute if score @s mgs.previous_dps matches 1.. run scoreboard players set #ab_active mgs.data 1
execute if score @s mgs.ab_force matches 1 run scoreboard players set #ab_active mgs.data 1
scoreboard players operation #ab_phase mgs.data = #total_tick mgs.data
scoreboard players operation #ab_phase mgs.data %= #10 mgs.data
execute if score #ab_active mgs.data matches 0 unless score #ab_phase mgs.data matches 0 run return 0
scoreboard players set @s mgs.ab_force 0

function mgs:v5.1.0/actionbar/build_fire_mode_indicator

function mgs:v5.1.0/actionbar/add_cooldown_indicator

execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute store result score #remaining mgs.data run scoreboard players get @s mgs.remaining_bullets

data modify storage mgs:temp actionbar.list append value " "

# Above 15 bullets, numbers; otherwise icons.
execute if score #capacity mgs.data matches 16.. run function mgs:v5.1.0/actionbar/add_numeric_ammo
execute if score #capacity mgs.data matches ..15 run function mgs:v5.1.0/actionbar/add_icon_ammo

function mgs:v5.1.0/actionbar/add_dps

function mgs:v5.1.0/actionbar/display with storage mgs:temp actionbar

