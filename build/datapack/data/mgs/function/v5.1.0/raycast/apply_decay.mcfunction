
#> mgs:v5.1.0/raycast/apply_decay
#
# @within	mgs:v5.1.0/raycast/on_targeted_entity
#

## damage *= pow(decay, distance / 10)
data modify storage bs:in math.pow.x set from storage mgs:gun all.stats.decay

execute store result score #raycast_distance mgs.data run scoreboard players get $raycast.entry_distance bs.lambda
scoreboard players operation #raycast_distance mgs.data /= #10 mgs.data
execute store result storage bs:in math.pow.y float 0.001 run scoreboard players get #raycast_distance mgs.data

# https://docs.mcbookshelf.dev/en/latest/modules/math.html#power
function #bs.math:pow

execute store result score #pow_decay_distance mgs.data run data get storage bs:out math.pow 1000
scoreboard players operation #damage mgs.data *= #pow_decay_distance mgs.data

# Two values scaled by 1000 were multiplied.
scoreboard players operation #damage mgs.data /= #1000 mgs.data

