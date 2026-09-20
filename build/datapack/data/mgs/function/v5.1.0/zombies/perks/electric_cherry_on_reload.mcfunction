
#> mgs:v5.1.0/zombies/perks/electric_cherry_on_reload
#
# @within	#mgs:signals/on_reload
#

execute unless score @s mgs.zb.in_game matches 1.. run return fail
execute unless score @s mgs.special.electric_cherry matches 1 run return fail

# Bullets discharged = capacity - remaining (read capacity from the reload signal payload)
execute store result score #ec_cap mgs.data run data get storage mgs:signals on_reload.weapon.stats.capacity
execute store result score #ec_rem mgs.data run scoreboard players get @s mgs.remaining_bullets
execute if score #ec_rem mgs.data matches ..-1 run scoreboard players set #ec_rem mgs.data 0
scoreboard players operation #ec_used mgs.data = #ec_cap mgs.data
scoreboard players operation #ec_used mgs.data -= #ec_rem mgs.data
execute if score #ec_used mgs.data matches ..0 run return fail

# Cooldown gate: since = now - last discharge. Allowed if since>=200 (10s), or since>=100 (5s) on a dry reload.
execute store result score #ec_now mgs.data run time query gametime
scoreboard players operation #ec_since mgs.data = #ec_now mgs.data
scoreboard players operation #ec_since mgs.data -= @s mgs.zb.ec_last
scoreboard players set #ec_ok mgs.data 0
execute if score #ec_since mgs.data matches 200.. run scoreboard players set #ec_ok mgs.data 1
execute if score #ec_since mgs.data matches 100.. if score #ec_rem mgs.data matches 0 run scoreboard players set #ec_ok mgs.data 1
execute if score #ec_ok mgs.data matches 0 run return fail

# Fire the discharge and stamp the time
scoreboard players operation @s mgs.zb.ec_last = #ec_now mgs.data
execute at @s run function mgs:v5.1.0/zombies/perks/electric_cherry_shock

