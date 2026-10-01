
#> mgs:v5.1.0/player/right_click
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

execute if score @s mgs.mp.in_game matches 1 if data storage mgs:multiplayer game{state:"preparing"} run return run scoreboard players set @s mgs.pending_clicks 0

# No shooting during prep.
execute if score @s mgs.zb.in_game matches 1 if data storage mgs:zombies game{state:"preparing"} run return run scoreboard players set @s mgs.pending_clicks 0


scoreboard players remove @s mgs.pending_clicks 1

# 3 s after the last click, the lore and reserve ammo are refreshed.
execute if score @s mgs.pending_clicks matches -60 if data storage mgs:gun all.gun run function mgs:v5.1.0/ammo/modify_lore {slot:"weapon.mainhand"}

execute if score @s mgs.cooldown > #total_tick mgs.data run return fail
execute if score @s mgs.pending_clicks matches ..-1 run return fail

execute unless data storage mgs:gun all.gun run return fail
execute unless score @s mgs.special.infinite_ammo matches 1.. if score @s mgs.remaining_bullets matches ..0 run return run function mgs:v5.1.0/ammo/reload

# From the fire mode and the held-click state.
scoreboard players set #bullets_to_fire mgs.data 1

execute store result score #fire_mode_is_semi mgs.data if data storage mgs:gun all.stats{fire_mode:"semi"}
execute store result score #fire_mode_is_burst mgs.data if data storage mgs:gun all.stats{fire_mode:"burst"}

# Semi: single taps only.
execute if score #fire_mode_is_semi mgs.data matches 1 if score @s mgs.held_click matches 1.. run return fail

# Burst: no more once the burst limit is reached.
execute if score #fire_mode_is_burst mgs.data matches 1 store result score #burst_limit mgs.data run data get storage mgs:gun all.stats.burst
execute if score #fire_mode_is_burst mgs.data matches 1 if score @s mgs.burst_count >= #burst_limit mgs.data run return fail

# First shot of a burst: pending_clicks = (BURST - 1) x COOLDOWN sustains it.
execute if score #fire_mode_is_burst mgs.data matches 1 if score @s mgs.burst_count matches 0 run function mgs:v5.1.0/player/init_burst_clicks

execute if score #fire_mode_is_burst mgs.data matches 1 run scoreboard players add @s mgs.burst_count 1

# Auto: continuous fire.

# As an expiry tick: now + cooldown.
execute store result score #cooldown mgs.data run data get storage mgs:gun all.stats.cooldown
# Timeslip (zombies): halves the throw cooldown of grenades and equipment.
execute if score @s mgs.special.timeslip matches 1 if data storage mgs:gun all.stats.grenade_type run scoreboard players operation #cooldown mgs.data /= #2 mgs.data
scoreboard players operation #cooldown mgs.data += #total_tick mgs.data
scoreboard players operation @s mgs.cooldown = #cooldown mgs.data

function mgs:v5.1.0/player/fire_weapon

# Weapon data in mgs:signals.
data modify storage mgs:signals on_shoot set value {}
data modify storage mgs:signals on_shoot.weapon set from storage mgs:gun all
function #mgs:signals/on_shoot

function mgs:v5.1.0/kicks/main

function mgs:v5.1.0/casing/main

function mgs:v5.1.0/ammo/decrease

function mgs:v5.1.0/sound/main

