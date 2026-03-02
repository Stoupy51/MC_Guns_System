
#> mgs:v5.0.0/raycast/on_targeted_block
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/main
#

# Get current block (https://docs.mcbookshelf.dev/en/latest/modules/block.html#get)
scoreboard players set #last_callback mgs.data 1
scoreboard players set #is_water mgs.data 0
scoreboard players set #is_pass_through mgs.data 0
execute if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through mgs.data 1
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/water run scoreboard players set #is_water mgs.data 1
function #bs.block:get_type
data modify storage mgs:temp block set from storage bs:out block
#tellraw @a {"nbt":"block","storage":"mgs:temp","interpret":false}

# If the block can be passed through, increment back piercing, and stop here if it's not water
execute if score #is_pass_through mgs.data matches 1 run scoreboard players add $raycast.piercing bs.lambda 1
execute if score #is_pass_through mgs.data matches 1 unless block ~ ~ ~ #mgs:v5.0.0/sounds/water run return 1

# For water/pass-through: reduce damage by 5%
execute if score #is_pass_through mgs.data matches 1 store result score #new_damage mgs.data run data get storage mgs:temp damage 1000
execute if score #is_pass_through mgs.data matches 1 store result storage mgs:temp damage float 0.00095 run scoreboard players get #new_damage mgs.data

# For solid blocks: lookup hardness
execute if score #is_pass_through mgs.data matches 0 run function #bs.block:lookup_type with storage bs:out block
execute if score #is_pass_through mgs.data matches 0 store result score #hardness mgs.data run data get storage bs:out block.hardness 1000

# Indestructible blocks (bedrock, barriers, hardness=-1): stop bullet completely
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches ..-1 run data modify storage mgs:temp damage set value 0.0d
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches ..-1 run return 0

# Piercing: cap on first solid block hit (initial piercing is 10, cap to 3)
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 0.. if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 3
# Reduce piercing based on hardness tiers (directly in callback for lambda score access)
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 0..299 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 300..999 run scoreboard players remove $raycast.piercing bs.lambda 2
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 1000..2999 run scoreboard players remove $raycast.piercing bs.lambda 3
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 3000.. run scoreboard players set $raycast.piercing bs.lambda 0

# Clamp piercing to 0 (Bookshelf raycast only stops at exactly 0, not negative)
execute if score #is_pass_through mgs.data matches 0 if score $raycast.piercing bs.lambda matches ..-1 run scoreboard players set $raycast.piercing bs.lambda 0

# Apply hardness damage reduction (non-indestructible solid blocks only)
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 0.. run function mgs:v5.0.0/raycast/apply_block_hardness

# Signal: on_hit_block (only for solid blocks, @s = raycast marker, positioned at block)
execute if score #is_pass_through mgs.data matches 0 run data modify storage mgs:signals on_hit_block set value {}
execute if score #is_pass_through mgs.data matches 0 run data modify storage mgs:signals on_hit_block.block set from storage mgs:temp block
execute if score #is_pass_through mgs.data matches 0 run data modify storage mgs:signals on_hit_block.weapon set from storage mgs:gun all
execute if score #is_pass_through mgs.data matches 0 run function #mgs:signals/on_hit_block

# Hard blocks (hardness >= 1.0): play impact sound and stop the ray
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 1000.. if score #played_solid mgs.data matches 0 store success score #played_solid mgs.data run playsound mgs:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #is_pass_through mgs.data matches 0 if score #hardness mgs.data matches 1000.. run return 0

## Playsounds
# Each sound type has a scoreboard objective that tracks if it has been played.
# The score is set to 1 when the sound plays, preventing it from playing again.
# The 'run return run' command ensures only one sound tries to play per block hit
# (e.g. if water already played and it's water again, it will not trigger soft)
execute if score #is_pass_through mgs.data matches 1 run return run execute if score #played_water mgs.data matches 0 store success score #played_water mgs.data run playsound minecraft:entity.axolotl.splash block @a[distance=..24] ~ ~ ~ 0.8 1.5
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/glass run return run execute if score #played_glass mgs.data matches 0 store success score #played_glass mgs.data run playsound minecraft:block.glass.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/cloth run return run execute if score #played_cloth mgs.data matches 0 store success score #played_cloth mgs.data run playsound mgs:common/cloth_bullet_impact block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/dirt run return run execute if score #played_dirt mgs.data matches 0 store success score #played_dirt mgs.data run playsound mgs:common/dirt_bullet_impact block @a[distance=..24] ~ ~ ~ 0.3
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/mud run return run execute if score #played_mud mgs.data matches 0 store success score #played_mud mgs.data run playsound mgs:common/mud_bullet_impact block @a[distance=..24] ~ ~ ~ 0.4
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/wood run return run execute if score #played_wood mgs.data matches 0 store success score #played_wood mgs.data run playsound mgs:common/wood_bullet_impact block @a[distance=..24] ~ ~ ~ 0.5
execute if block ~ ~ ~ #mgs:v5.0.0/plant run return run execute if score #played_plant mgs.data matches 0 store success score #played_plant mgs.data run playsound minecraft:block.azalea_leaves.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.0.0/solid run return run execute if score #played_solid mgs.data matches 0 store success score #played_solid mgs.data run playsound mgs:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #played_soft mgs.data matches 0 store success score #played_soft mgs.data run playsound mgs:common/soft_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2

