
#> mgs:v5.4.1/switch/do_toggle_fire_mode
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/switch/fire_mode_on_dropped_weapon
#

# The current mode moves to the back, the next one comes first.
data modify storage mgs:gun all.stats.fire_modes append from storage mgs:gun all.stats.fire_modes[0]
data remove storage mgs:gun all.stats.fire_modes[0]
data modify storage mgs:gun all.stats.fire_mode set from storage mgs:gun all.stats.fire_modes[0].name
scoreboard players set @s mgs.burst_count 0

item modify entity @s weapon.mainhand mgs:v5.4.1/set_fire_mode

# Run as the player; weapon and new mode in mgs:signals.
data modify storage mgs:signals on_fire_mode_change set value {}
data modify storage mgs:signals on_fire_mode_change.weapon set from storage mgs:gun all
data modify storage mgs:signals on_fire_mode_change.fire_mode set from storage mgs:gun all.stats.fire_mode
function #mgs:signals/on_fire_mode_change

playsound mgs:common/fireselect player @s

# So the fire-mode highlight follows at once.
scoreboard players set @s mgs.ab_force 1

