
#> mgs:v5.0.0/raycast/on_targeted_entity
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/main
#

# Blood particles
scoreboard players set #last_callback mgs.data 2
particle block{block_state:"redstone_wire"} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Get base damage with 3 digits of precision
data modify storage mgs:input with set value {target:"@s", amount:0.0f, attacker:"@n[tag=mgs.ticking]"}
execute store result score #damage mgs.data run data get storage mgs:temp damage 10

# Apply decay and headshot calculations
function mgs:v5.0.0/raycast/apply_decay
function mgs:v5.0.0/raycast/check_headshot

# Instant kill: if shooter has active instant kill and target is not immune, set damage to 99999
execute as @n[tag=mgs.ticking] if score @s mgs.special.instant_kill matches 1.. as @s[tag=!mgs.no_instant_kill] run scoreboard players set #damage mgs.data 99999

# Signal: on_headshot (if headshot detected, @s = hit entity)
execute if score #is_headshot mgs.data matches 1 run data modify storage mgs:signals on_headshot set value {}
execute if score #is_headshot mgs.data matches 1 run data modify storage mgs:signals on_headshot.weapon set from storage mgs:gun all
execute if score #is_headshot mgs.data matches 1 run execute store result storage mgs:signals on_headshot.damage float 0.1 run scoreboard players get #damage mgs.data
execute if score #is_headshot mgs.data matches 1 run function #mgs:signals/on_headshot

# Damage entity
execute store result storage mgs:input with.amount float 0.1 run scoreboard players get #damage mgs.data
function mgs:v5.0.0/utils/damage with storage mgs:input with
function #mgs:signals/damage with storage mgs:input with

# Signal: on_hit_entity (@s = hit entity, weapon/damage info in mgs:signals)
data modify storage mgs:signals on_hit_entity set value {}
data modify storage mgs:signals on_hit_entity.weapon set from storage mgs:gun all
execute store result storage mgs:signals on_hit_entity.damage float 0.1 run scoreboard players get #damage mgs.data
execute store result storage mgs:signals on_hit_entity.headshot int 1 run scoreboard players get #is_headshot mgs.data
data modify storage mgs:signals on_hit_entity.target set from entity @s UUID
function #mgs:signals/on_hit_entity

# Signal: on_kill (if entity died, @s switches to shooter player)
execute unless entity @s as @n[tag=mgs.ticking] run data modify storage mgs:signals on_kill set value {}
execute unless entity @s as @n[tag=mgs.ticking] run data modify storage mgs:signals on_kill.weapon set from storage mgs:gun all
execute unless entity @s as @n[tag=mgs.ticking] run function #mgs:signals/on_kill

