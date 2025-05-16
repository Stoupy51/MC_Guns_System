
#> stoupgun:v5.0.0/raycast/on_targeted_entity
#
# @within	stoupgun:v5.0.0/raycast/main
#

# Blood particles
particle block{block_state:"redstone_wire"} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Get base damage with 3 digits of precision
data modify storage stoupgun:input with set value {target:"@s", amount:0.0f, attacker:"@p[tag=stoupgun.attacker]"}
execute store result score #damage stoupgun.data run data get storage stoupgun:gun stats.damage 10

# Apply decay using `damage *= pow(decay, distance)` (https://docs.mcbookshelf.dev/en/latest/modules/math.html#power)
data modify storage bs:in math.pow.x set from storage stoupgun:gun stats.decay
data modify storage bs:in math.pow.y set from storage bs:lambda raycast.distance
function #bs.math:pow
execute store result score #pow_decay_distance stoupgun.data run data get storage bs:out math.pow 1000000
scoreboard players operation #damage stoupgun.data *= #pow_decay_distance stoupgun.data

# Divide by 1000000 because we're multiplying two scaled integers with each other (10*1000000 = 10000000)
scoreboard players operation #damage stoupgun.data /= #1000000 stoupgun.data

# Divide damage by 2 if not headshot
scoreboard players set #is_headshot stoupgun.data 0
execute store result score #entity_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #hit_y stoupgun.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff stoupgun.data = #hit_y stoupgun.data
scoreboard players operation #y_diff stoupgun.data -= #entity_y stoupgun.data
execute if score #y_diff stoupgun.data matches 1200.. run scoreboard players set #is_headshot stoupgun.data 1
execute unless score #is_headshot stoupgun.data matches 1 run scoreboard players operation #damage stoupgun.data /= #2 stoupgun.data

# Damage entity
execute store result storage stoupgun:input with.amount float 0.1 run scoreboard players get #damage stoupgun.data
function stoupgun:v5.0.0/utils/damage with storage stoupgun:input with

