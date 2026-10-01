
#> mgs:v5.1.0/sound/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#

## A Pack-a-Punched gun with a pap_fire sound plays it instead.
scoreboard players set #do_pap_sound mgs.data 0
execute if data storage mgs:gun all.stats.pap_level if data storage mgs:gun all.sounds.pap_fire run scoreboard players set #do_pap_sound mgs.data 1
execute if score #do_pap_sound mgs.data matches 1 run function mgs:v5.1.0/sound/fire_pap with storage mgs:gun all.sounds

## TODO: a mode check to choose between fire and fire_alt.
execute if score #do_pap_sound mgs.data matches 0 if data storage mgs:gun all.sounds.fire_alt run function mgs:v5.1.0/sound/fire_alt with storage mgs:gun all.sounds
execute if score #do_pap_sound mgs.data matches 0 unless data storage mgs:gun all.sounds.fire_alt run function mgs:v5.1.0/sound/fire_simple with storage mgs:gun all.sounds

# Sniper rifles.
execute if data storage mgs:gun all.sounds.cycle run function mgs:v5.1.0/sound/cycle with storage mgs:gun all.sounds

execute if data storage mgs:gun all.sounds.crack run function mgs:v5.1.0/sound/acoustics_main with storage mgs:gun all.sounds

