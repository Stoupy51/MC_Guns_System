
#> mgs:v5.1.0/ammo/reload
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#			mgs:v5.1.0/player/swap_and_reload
#			mgs:v5.1.0/weapon/left_click
#			mgs:v5.1.0/ammo/decrease
#			mgs:v5.1.0/ammo/single_reload_continue
#

# Already reloading, or full.
execute if entity @s[tag=mgs.reloading] run return fail
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity
execute if score @s mgs.remaining_bullets >= #capacity mgs.data run return fail

# Magazines available, without consuming them.
scoreboard players set @s mgs.cooldown 5
scoreboard players operation @s mgs.cooldown += #total_tick mgs.data
execute unless data storage mgs:config no_magazine store success score #success mgs.data run function mgs:v5.1.0/ammo/inventory/has_ammo with storage mgs:gun all.stats
execute unless data storage mgs:config no_magazine if score #success mgs.data matches 0 run return run playsound mgs:common/empty ambient @s

# Reload duration, with the quick_reload reduction.
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.reload_time

# quick_reload is a percentage (20 = 20% faster).
execute if score @s mgs.special.quick_reload matches 1.. run function mgs:v5.1.0/ammo/apply_quick_reload

# As an expiry tick.
scoreboard players operation @s mgs.cooldown += #total_tick mgs.data

function mgs:v5.1.0/switch/force_switch_animation

# Each sound is guarded: not every weapon defines all of them, and a missing macro argument errors.
execute if data storage mgs:gun all.sounds.reload run function mgs:v5.1.0/sound/reload_start with storage mgs:gun all.sounds
execute if data storage mgs:gun all.sounds.playerbegin run function mgs:v5.1.0/sound/player_begin with storage mgs:gun all.sounds

tag @s add mgs.reloading

# Run as the player; weapon data in mgs:signals.
data modify storage mgs:signals on_reload set value {}
data modify storage mgs:signals on_reload.weapon set from storage mgs:gun all
function #mgs:signals/on_reload

