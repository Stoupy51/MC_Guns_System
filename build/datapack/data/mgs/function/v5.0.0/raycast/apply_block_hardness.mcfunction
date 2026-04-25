
#> mgs:v5.0.0/raycast/apply_block_hardness
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/on_targeted_block
#

#tellraw @a[distance=..128] [{"translate":"mgs.hardness","color":"gray","extra":[{"score":{"name":"#hardness","objective":"mgs.data"},"color":"white"}]},{"text":" $raycast.piercing bs.lambda: ","color":"gray","extra":[{"score":{"name":"$raycast.piercing","objective":"bs.lambda"},"color":"white"}]}]

# Calculate damage reduction: reduction = hardness * 400 / 1000, capped at 950
scoreboard players operation #reduction mgs.data = #hardness mgs.data
scoreboard players operation #reduction mgs.data /= #10 mgs.data
scoreboard players operation #reduction mgs.data *= #2 mgs.data
scoreboard players operation #reduction mgs.data *= #2 mgs.data
execute if score #reduction mgs.data matches 951.. run scoreboard players set #reduction mgs.data 950

# Apply: damage = damage * (1000 - reduction) / 1000
execute store result score #new_damage mgs.data run data get storage mgs:temp damage 1000
scoreboard players set #remaining_pct mgs.data 1000
scoreboard players operation #remaining_pct mgs.data -= #reduction mgs.data
scoreboard players operation #new_damage mgs.data *= #remaining_pct mgs.data
scoreboard players operation #new_damage mgs.data /= #1000 mgs.data
execute store result storage mgs:temp damage float 0.001 run scoreboard players get #new_damage mgs.data

