
#> mgs:v5.1.0/sound/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#

## A Pack-a-Punched gun with a pap_fire sound plays it instead.
scoreboard players set #do_pap_sound mgs.data 0
execute if data storage mgs:gun all.stats.pap_level if data storage mgs:gun all.sounds.pap_fire run scoreboard players set #do_pap_sound mgs.data 1
data modify storage mgs:temp fire_sound set value {}
execute if score #do_pap_sound mgs.data matches 0 run data modify storage mgs:temp fire_sound.others set from storage mgs:gun all.sounds.fire
execute if score #do_pap_sound mgs.data matches 1 run data modify storage mgs:temp fire_sound.others set from storage mgs:gun all.sounds.pap_fire

# The shooter hears the fire mode's own sound when it has one (a missing path leaves the weapon's).
data modify storage mgs:temp fire_sound.self set from storage mgs:temp fire_sound.others
execute if score #do_pap_sound mgs.data matches 0 run data modify storage mgs:temp fire_sound.self set from storage mgs:gun all.stats.fire_modes[0].fire_sound
execute if score #do_pap_sound mgs.data matches 1 run data modify storage mgs:temp fire_sound.self set from storage mgs:gun all.stats.fire_modes[0].pap_fire_sound
function mgs:v5.1.0/sound/fire with storage mgs:temp fire_sound

# Sniper rifles.
execute if data storage mgs:gun all.sounds.cycle run function mgs:v5.1.0/sound/cycle with storage mgs:gun all.sounds

execute if data storage mgs:gun all.sounds.crack run function mgs:v5.1.0/sound/acoustics_main with storage mgs:gun all.sounds

