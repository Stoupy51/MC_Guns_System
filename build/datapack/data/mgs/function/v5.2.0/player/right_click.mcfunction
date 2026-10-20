
#> mgs:v5.2.0/player/right_click
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/player/tick
#

execute if score @s mgs.mp.in_game matches 1 if data storage mgs:multiplayer game{state:"preparing"} run return run scoreboard players set @s mgs.pending_clicks 0

# No shooting during prep.
execute if score @s mgs.zb.in_game matches 1 if data storage mgs:zombies game{state:"preparing"} run return run scoreboard players set @s mgs.pending_clicks 0


scoreboard players remove @s mgs.pending_clicks 1

# 3 s after the last click, the lore and reserve ammo are refreshed.
execute if score @s mgs.pending_clicks matches -60 if data storage mgs:gun all.gun run function mgs:v5.2.0/ammo/modify_lore {slot:"weapon.mainhand"}

execute if score @s mgs.cooldown > #total_tick mgs.data run return fail
execute if score @s mgs.pending_clicks matches ..-1 run return fail

execute unless data storage mgs:gun all.gun run return fail
execute unless score @s mgs.special.infinite_ammo matches 1.. if score @s mgs.remaining_bullets matches ..0 run return run function mgs:v5.2.0/ammo/reload

# From the fire mode and the held-click state.
scoreboard players set #bullets_to_fire mgs.data 1

execute store result score #fire_mode_is_burst mgs.data if data storage mgs:gun all.stats{fire_mode:"burst"}

# Semi and pump: single taps only.
execute if score @s mgs.held_click matches 1.. if data storage mgs:gun all.stats{fire_mode:"semi"} run return fail
execute if score @s mgs.held_click matches 1.. if data storage mgs:gun all.stats{fire_mode:"pump"} run return fail

# Burst: no more once the burst limit is reached.
execute if score #fire_mode_is_burst mgs.data matches 1 store result score #burst_limit mgs.data run data get storage mgs:gun all.stats.fire_modes[0].burst
execute if score #fire_mode_is_burst mgs.data matches 1 if score @s mgs.burst_count >= #burst_limit mgs.data run return fail

# The fire mode's cooldown when it has one, its Pack-a-Punch value on an upgraded gun.
execute store result score #cooldown mgs.data run data get storage mgs:gun all.stats.cooldown
execute if data storage mgs:gun all.stats.fire_modes[0].cooldown store result score #cooldown mgs.data run data get storage mgs:gun all.stats.fire_modes[0].cooldown
execute if data storage mgs:gun all.stats.pap_level if data storage mgs:gun all.stats.fire_modes[0].pap_cooldown store result score #cooldown mgs.data run data get storage mgs:gun all.stats.fire_modes[0].pap_cooldown
execute if score #fire_mode_is_burst mgs.data matches 1 run function mgs:v5.2.0/player/burst_cooldown

# Timeslip (zombies): halves the throw cooldown of grenades and equipment.
execute if score @s mgs.special.timeslip matches 1 if data storage mgs:gun all.stats.grenade_type run scoreboard players operation #cooldown mgs.data /= #2 mgs.data

# As an expiry tick: now + cooldown.
scoreboard players operation #cooldown mgs.data += #total_tick mgs.data
scoreboard players operation @s mgs.cooldown = #cooldown mgs.data

function mgs:v5.2.0/player/fire_weapon

# Weapon data in mgs:signals.
data modify storage mgs:signals on_shoot set value {}
data modify storage mgs:signals on_shoot.weapon set from storage mgs:gun all
function #mgs:signals/on_shoot

function mgs:v5.2.0/kicks/main

execute unless data storage mgs:gun all.stats{fire_mode:"pump"} run function mgs:v5.2.0/casing/main

function mgs:v5.2.0/ammo/decrease

function mgs:v5.2.0/sound/main

