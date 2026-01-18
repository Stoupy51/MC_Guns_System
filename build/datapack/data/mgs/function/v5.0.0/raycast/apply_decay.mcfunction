
#> mgs:v5.0.0/raycast/apply_decay
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/on_targeted_entity
#

## Apply decay using `damage *= pow(decay, distance / 10)`
# Get decay into x
data modify storage bs:in math.pow.x set from storage mgs:gun all.stats.decay

# Get raycast distance / 10 into y
execute store result score #raycast_distance mgs.data run data get storage bs:lambda raycast.distance 1000000
scoreboard players operation #raycast_distance mgs.data /= #10 mgs.data
execute store result storage bs:in math.pow.y float 0.000001 run scoreboard players get #raycast_distance mgs.data

# Compute power using https://docs.mcbookshelf.dev/en/latest/modules/math.html#power
function #bs.math:pow

# Collect computed value and multiply to the damage
execute store result score #pow_decay_distance mgs.data run data get storage bs:out math.pow 1000000
scoreboard players operation #damage mgs.data *= #pow_decay_distance mgs.data

# Divide by 1000000 because we're multiplying two scaled integers with each other (10*1000000 = 10000000)
scoreboard players operation #damage mgs.data /= #1000000 mgs.data

