
#> mgs:v5.0.0/raycast/apply_damage
#
# @executed	at @s
#
# @within	mgs:v5.0.0/raycast/headshot_and_damage [ at @s ]
#

# Instant kill check
execute as @n[tag=mgs.ticking] if score @s mgs.special.instant_kill matches 1.. as @s[tag=!mgs.no_instant_kill] run scoreboard players set #damage mgs.data 99999

# Signal: on_headshot
execute if score #is_headshot mgs.data matches 1 run data modify storage mgs:signals on_headshot set value {}
execute if score #is_headshot mgs.data matches 1 run data modify storage mgs:signals on_headshot.weapon set from storage mgs:gun all
execute if score #is_headshot mgs.data matches 1 store result storage mgs:signals on_headshot.damage float 0.1 run scoreboard players get #damage mgs.data
execute if score #is_headshot mgs.data matches 1 run function #mgs:signals/on_headshot

# Damage entity
execute store result storage mgs:input with.amount float 0.1 run scoreboard players get #damage mgs.data
data modify storage mgs:input with.weapon set from storage mgs:gun all
execute store result storage mgs:input with.headshot int 1 run scoreboard players get #is_headshot mgs.data
function mgs:v5.0.0/utils/signal_and_damage

# Signal: on_kill
scoreboard players set #victim_hp mgs.data 0
execute store result score #victim_hp mgs.data run data get entity @s Health 100
execute if score #victim_hp mgs.data matches ..0 run data modify storage mgs:signals on_kill set value {}
execute if score #victim_hp mgs.data matches ..0 run data modify storage mgs:signals on_kill.weapon set from storage mgs:gun all
execute if score #victim_hp mgs.data matches ..0 as @n[tag=mgs.ticking] run function #mgs:signals/on_kill

