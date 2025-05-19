
#> stoupgun:v5.0.0/raycast/on_targeted_entity
#
# @within	stoupgun:v5.0.0/raycast/main
#

# Blood particles
particle block{block_state:"redstone_wire"} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Get base damage with 3 digits of precision
data modify storage stoupgun:input with set value {target:"@s", amount:0.0f, attacker:"@p[tag=stoupgun.ticking]"}
execute store result score #damage stoupgun.data run data get storage stoupgun:gun all.stats.damage 10

# Apply decay and headshot calculations
function stoupgun:v5.0.0/raycast/apply_decay
function stoupgun:v5.0.0/raycast/check_headshot

# Damage entity
execute store result storage stoupgun:input with.amount float 0.1 run scoreboard players get #damage stoupgun.data
function stoupgun:v5.0.0/utils/damage with storage stoupgun:input with

