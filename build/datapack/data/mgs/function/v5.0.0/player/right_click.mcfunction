
#> mgs:v5.0.0/player/right_click
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Decrease pending clicks by 1
scoreboard players remove @s mgs.pending_clicks 1

# If player stopped right clicking for 3 second, we update the item lore
execute if score @s mgs.pending_clicks matches -60 if data storage mgs:gun all.gun run function mgs:v5.0.0/ammo/modify_lore {slot:"weapon.mainhand"}

# Stop here is weapon cooldown OR pending clicks if negative
execute if score @s mgs.cooldown matches 1.. run return fail
execute if score @s mgs.pending_clicks matches ..-1 run return fail

# Stop if SelectedItem is not a gun or if not enough ammo
execute unless data storage mgs:gun all.gun run return fail
execute if score @s mgs.remaining_bullets matches ..0 run return run function mgs:v5.0.0/ammo/reload

# Set cooldown
execute store result score @s mgs.cooldown run data get storage mgs:gun all.stats.cooldown

# Shoot the gun
scoreboard players set #bullets_to_fire mgs.data 1
execute if data storage mgs:gun all.stats.pellet_count store result score #bullets_to_fire mgs.data run data get storage mgs:gun all.stats.pellet_count
function mgs:v5.0.0/player/shoot

# Simulate weapon kick
function mgs:v5.0.0/kicks/main

# Drop casing
function mgs:v5.0.0/casing/main

# Decrease bullet count
function mgs:v5.0.0/ammo/decrease

# Advanced Playsound
function mgs:v5.0.0/sound/main

# Summon flash
function mgs:v5.0.0/flash/summon

