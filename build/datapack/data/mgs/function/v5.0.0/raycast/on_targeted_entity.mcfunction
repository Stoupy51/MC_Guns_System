
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
data modify storage mgs:input with set value {target:"@s", amount:0.0f, attacker:"@p[tag=mgs.ticking]"}
execute store result score #damage mgs.data run data get storage mgs:gun all.stats.damage 10

# Apply decay and headshot calculations
function mgs:v5.0.0/raycast/apply_decay
function mgs:v5.0.0/raycast/check_headshot

# Damage entity
execute store result storage mgs:input with.amount float 0.1 run scoreboard players get #damage mgs.data
function mgs:v5.0.0/utils/damage with storage mgs:input with

