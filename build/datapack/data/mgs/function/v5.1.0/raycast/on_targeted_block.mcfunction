
#> mgs:v5.1.0/raycast/on_targeted_block
#
# @within	string in mgs:v5.1.0/raycast/main
#

# https://docs.mcbookshelf.dev/en/latest/modules/block.html#get
scoreboard players set #is_entity_hit mgs.data 0
scoreboard players set #is_water mgs.data 0
scoreboard players set #is_pass_through mgs.data 0
execute if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through mgs.data 1
execute if block ~ ~ ~ #mgs:v5.1.0/sounds/water run scoreboard players set #is_water mgs.data 1
function #bs.block:get_type
data modify storage mgs:temp block set from storage bs:out block

# Pass-through blocks give the piercing back; only water continues below.
execute if score #is_pass_through mgs.data matches 1 run scoreboard players add $raycast.piercing bs.lambda 1
execute if score #is_pass_through mgs.data matches 1 unless block ~ ~ ~ #mgs:v5.1.0/sounds/water run return 1

# Water and pass-through blocks: -5% damage.
execute if score #is_pass_through mgs.data matches 1 store result score #new_damage mgs.data run data get storage mgs:temp damage 1000
execute if score #is_pass_through mgs.data matches 1 store result storage mgs:temp damage float 0.00095 run scoreboard players get #new_damage mgs.data

# Solid blocks: look up the hardness.
execute if score #is_pass_through mgs.data matches 0 run function #bs.block:lookup_type with storage bs:out block
execute if score #is_pass_through mgs.data matches 0 store result score #hardness mgs.data run data get storage bs:out block.hardness 1000

# Indestructible (bedrock, hardness -1) stops the bullet; barrier is in the raycast's ignored_blocks, so bullets fly through it.
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches ..-1 run data modify storage mgs:temp damage set value 0.0d
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches ..-1 run return 0

# The first solid block caps piercing at 6 (it starts at 10).
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 0.. if score $raycast.piercing bs.lambda matches 7.. run scoreboard players set $raycast.piercing bs.lambda 6
# In the callback, where the lambda score is reachable.
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 0..299 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 300..999 run scoreboard players remove $raycast.piercing bs.lambda 2
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 1000..2999 run scoreboard players remove $raycast.piercing bs.lambda 3
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 3000.. run scoreboard players set $raycast.piercing bs.lambda 0

# Bookshelf only stops at exactly 0, not below.
execute if score #is_pass_through mgs.data matches 0 if score $raycast.piercing bs.lambda matches ..-1 run scoreboard players set $raycast.piercing bs.lambda 0

execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 0.. run function mgs:v5.1.0/raycast/apply_block_hardness

# Solid blocks only; run as the raycast marker, at the block.
execute if score #is_pass_through mgs.data matches 0 run data modify storage mgs:signals on_hit_block set value {}
execute if score #is_pass_through mgs.data matches 0 run data modify storage mgs:signals on_hit_block.block set from storage mgs:temp block
execute if score #is_pass_through mgs.data matches 0 run data modify storage mgs:signals on_hit_block.weapon set from storage mgs:gun all
execute if score #is_pass_through mgs.data matches 0 run function #mgs:signals/on_hit_block

# Hardness 1.0+: impact sound, and the ray stops.
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 1000.. if score #played_solid mgs.data matches 0 store success score #played_solid mgs.data run playsound mgs:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 1000.. run return 0

## Each sound plays once per shot (#played_* set to 1); `return run` tries only one sound per block hit.
execute if score #is_pass_through mgs.data matches 1 run return run execute if score #played_water mgs.data matches 0 store success score #played_water mgs.data run playsound minecraft:entity.axolotl.splash block @a[distance=..24] ~ ~ ~ 0.8 1.5
execute if block ~ ~ ~ #mgs:v5.1.0/sounds/glass run return run execute if score #played_glass mgs.data matches 0 store success score #played_glass mgs.data run playsound minecraft:block.glass.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.1.0/sounds/cloth run return run execute if score #played_cloth mgs.data matches 0 store success score #played_cloth mgs.data run playsound mgs:common/cloth_bullet_impact block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.1.0/sounds/dirt run return run execute if score #played_dirt mgs.data matches 0 store success score #played_dirt mgs.data run playsound mgs:common/dirt_bullet_impact block @a[distance=..24] ~ ~ ~ 0.3
execute if block ~ ~ ~ #mgs:v5.1.0/sounds/mud run return run execute if score #played_mud mgs.data matches 0 store success score #played_mud mgs.data run playsound mgs:common/mud_bullet_impact block @a[distance=..24] ~ ~ ~ 0.4
execute if block ~ ~ ~ #mgs:v5.1.0/sounds/wood run return run execute if score #played_wood mgs.data matches 0 store success score #played_wood mgs.data run playsound mgs:common/wood_bullet_impact block @a[distance=..24] ~ ~ ~ 0.5
execute if block ~ ~ ~ #mgs:v5.1.0/plant run return run execute if score #played_plant mgs.data matches 0 store success score #played_plant mgs.data run playsound minecraft:block.azalea_leaves.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.1.0/solid run return run execute if score #played_solid mgs.data matches 0 store success score #played_solid mgs.data run playsound mgs:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #played_soft mgs.data matches 0 store success score #played_soft mgs.data run playsound mgs:common/soft_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2

