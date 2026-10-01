
#> mgs:v5.1.0/switch/do_toggle_fire_mode
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/fire_mode_on_dropped_weapon
#

function mgs:v5.1.0/utils/copy_gun_data
data modify storage mgs:temp fire_mode set from storage mgs:gun all.stats.fire_mode

execute store result score #has_auto mgs.data if data storage mgs:gun all.stats.can_auto
execute store result score #has_burst mgs.data if data storage mgs:gun all.stats.can_burst

execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"auto"} run data modify storage mgs:gun all.stats.fire_mode set value "semi"
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"semi"} run data modify storage mgs:gun all.stats.fire_mode set value "burst"
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"burst"} run data modify storage mgs:gun all.stats.fire_mode set value "auto"

execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 0 if data storage mgs:temp {fire_mode:"auto"} run data modify storage mgs:gun all.stats.fire_mode set value "semi"
execute if score #has_auto mgs.data matches 1 if score #has_burst mgs.data matches 0 if data storage mgs:temp {fire_mode:"semi"} run data modify storage mgs:gun all.stats.fire_mode set value "auto"

execute if score #has_auto mgs.data matches 0 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"semi"} run data modify storage mgs:gun all.stats.fire_mode set value "burst"
execute if score #has_auto mgs.data matches 0 if score #has_burst mgs.data matches 1 if data storage mgs:temp {fire_mode:"burst"} run data modify storage mgs:gun all.stats.fire_mode set value "semi"

# Missing mode: auto when supported, else semi.
execute unless data storage mgs:temp fire_mode if score #has_auto mgs.data matches 1 run data modify storage mgs:gun all.stats.fire_mode set value "auto"
execute unless data storage mgs:temp fire_mode if score #has_auto mgs.data matches 0 run data modify storage mgs:gun all.stats.fire_mode set value "semi"

item modify entity @s weapon.mainhand mgs:v5.1.0/set_fire_mode

# Run as the player; weapon and new mode in mgs:signals.
data modify storage mgs:signals on_fire_mode_change set value {}
data modify storage mgs:signals on_fire_mode_change.weapon set from storage mgs:gun all
data modify storage mgs:signals on_fire_mode_change.fire_mode set from storage mgs:gun all.stats.fire_mode
function #mgs:signals/on_fire_mode_change

# @p would pay a needless distance sort.
playsound minecraft:block.note_block.hat ambient @s

# So the fire-mode highlight follows at once.
scoreboard players set @s mgs.ab_force 1

