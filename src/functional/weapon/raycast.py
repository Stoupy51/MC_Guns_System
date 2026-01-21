
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.stats import (
    ACCURACY_BASE,
    ACCURACY_JUMP,
    ACCURACY_SNEAK,
    ACCURACY_SPRINT,
    ACCURACY_WALK,
    BURST,
    COOLDOWN,
    DAMAGE,
    DECAY,
    FIRE_MODE,
    PELLET_COUNT,
)


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Handle pending clicks
    write_versioned_function("player/right_click",
f"""
# Determine number of bullets to fire based on fire mode and held-click state
scoreboard players set #bullets_to_fire {ns}.data 1

# Check fire mode
execute store result score #fire_mode_is_semi {ns}.data if data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}}
execute store result score #fire_mode_is_burst {ns}.data if data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}}

# Semi-auto mode: block if holding (only allow single taps)
execute if score #fire_mode_is_semi {ns}.data matches 1 if score @s {ns}.held_click matches 1.. run return fail

# Burst mode: check if burst limit reached, if so block firing
execute if score #fire_mode_is_burst {ns}.data matches 1 store result score #burst_limit {ns}.data run data get storage {ns}:gun all.stats.{BURST}
execute if score #fire_mode_is_burst {ns}.data matches 1 if score @s {ns}.burst_count >= #burst_limit {ns}.data run return fail

# Burst mode: on first shot, set pending_clicks to (BURST-1) * COOLDOWN to sustain burst
execute if score #fire_mode_is_burst {ns}.data matches 1 if score @s {ns}.burst_count matches 0 run function {ns}:v{version}/player/init_burst_clicks

# Burst mode: increment counter
execute if score #fire_mode_is_burst {ns}.data matches 1 run scoreboard players add @s {ns}.burst_count 1

# Auto mode: allow continuous fire (no blocking)

# For shotguns (pellet count), multiply by pellet count instead
execute if data storage {ns}:gun all.stats.{PELLET_COUNT} store result score #bullets_to_fire {ns}.data run data get storage {ns}:gun all.stats.{PELLET_COUNT}

# Shoot
function {ns}:v{version}/player/shoot
""")

    # Initialize burst mode pending clicks
    write_versioned_function("player/init_burst_clicks",
f"""
# Calculate (BURST - 1) * COOLDOWN
execute store result score #burst_clicks {ns}.data run data get storage {ns}:gun all.stats.{BURST}
scoreboard players remove #burst_clicks {ns}.data 1
execute store result score #cooldown_value {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
scoreboard players operation #burst_clicks {ns}.data *= #cooldown_value {ns}.data

# Set pending_clicks to sustain burst firing
scoreboard players operation @s {ns}.pending_clicks = #burst_clicks {ns}.data
""")

    # Handle pending clicks
    write_versioned_function("player/shoot",
f"""
# Check which type of movement the player is doing
function {ns}:v{version}/raycast/accuracy/get_value

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/player/shoot
""")

    # Handle pending clicks
    write_versioned_function("raycast/main",
f"""
# Copy damage to temp storage to avoid modifying original for multiple pellets
data modify storage {ns}:temp damage set from storage {ns}:gun all.stats.{DAMAGE}

# Handle accuracy
tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Scores to remember to only play a sound type once
scoreboard players set #played_water {ns}.data 0
scoreboard players set #played_glass {ns}.data 0
scoreboard players set #played_cloth {ns}.data 0
scoreboard players set #played_dirt {ns}.data 0
scoreboard players set #played_mud {ns}.data 0
scoreboard players set #played_wood {ns}.data 0
scoreboard players set #played_plant {ns}.data 0
scoreboard players set #played_solid {ns}.data 0
scoreboard players set #played_soft {ns}.data 0
scoreboard players set #next_air_particle {ns}.data 0

# Prepare arguments
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_collision_with_fluid"
data modify storage {ns}:input with.entities set value true
data modify storage {ns}:input with.piercing set value 10
data modify storage {ns}:input with.max_distance set value 128
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.on_hit_point set value "function {ns}:v{version}/raycast/on_hit_point"
data modify storage {ns}:input with.on_targeted_block set value "function {ns}:v{version}/raycast/on_targeted_block"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/raycast/on_targeted_entity"

# Launch raycast with callbacks (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast)
execute at @s run function #bs.raycast:run with storage {ns}:input

# Kill marker
kill @s
""")

    # On hit point
    write_versioned_function("raycast/on_hit_point",
f"""
# If targeted entity, return to prevent showing particles
# (last_callback = 0 for on_hit_point, 1 for on_targeted_block, 2 for on_targeted_entity)
execute if score #last_callback {ns}.data matches 2 run return run scoreboard players set #last_callback {ns}.data 0
scoreboard players set #last_callback {ns}.data 0

# Make block particles (if not passing through) (on_targeted_block runs first to set passing through)
data modify storage {ns}:input with set value {{x:0,y:0,z:0,block:"minecraft:air"}}
data modify storage {ns}:input with.block set from storage {ns}:temp block.type
data modify storage {ns}:input with.x set from storage bs:lambda raycast.hit_point[0]
data modify storage {ns}:input with.y set from storage bs:lambda raycast.hit_point[1]
data modify storage {ns}:input with.z set from storage bs:lambda raycast.hit_point[2]
execute if score #is_pass_through {ns}.data matches 0 run return run function {ns}:v{version}/raycast/block_particles with storage {ns}:input with

# Change particles if passing through
execute if score #is_water {ns}.data matches 1 run data modify storage {ns}:input with.block set value "minecraft:bubble"
execute if score #is_water {ns}.data matches 0 run data modify storage {ns}:input with.block set value "minecraft:mycelium"

# Create particles every third iteration to maintain visual clarity while reducing particle density
scoreboard players add #next_air_particle {ns}.data 1
execute if score #next_air_particle {ns}.data matches 2 run function {ns}:v{version}/raycast/air_particles with storage {ns}:input with
execute if score #next_air_particle {ns}.data matches 3.. run scoreboard players set #next_air_particle {ns}.data 0
""")
    write_versioned_function("raycast/block_particles", r"""$particle block{block_state:"$(block)"} $(x) $(y) $(z) 0.1 0.1 0.1 1 10 force @a[distance=..128]""")
    write_versioned_function("raycast/air_particles", r"""$particle $(block) $(x) $(y) $(z) 0 0 0 0 1 force @a[distance=..128]""")

    # On targeted block
    write_versioned_function("raycast/on_targeted_block",
f"""
# Get current block (https://docs.mcbookshelf.dev/en/latest/modules/block.html#get)
scoreboard players set #last_callback {ns}.data 1
scoreboard players set #is_water {ns}.data 0
scoreboard players set #is_pass_through {ns}.data 0
execute if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through {ns}.data 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/water run scoreboard players set #is_water {ns}.data 1
function #bs.block:get_block
data modify storage {ns}:temp block set from storage bs:out block
#tellraw @a {{"nbt":"block","storage":"{ns}:temp","interpret":false}}

# If the block can be passed through, increment back piercing, and stop here if it's not water
execute if score #is_pass_through {ns}.data matches 1 run scoreboard players add $raycast.piercing bs.lambda 1
execute if score #is_pass_through {ns}.data matches 1 unless block ~ ~ ~ #{ns}:v{version}/sounds/water run return 1

# Allow bullets to pierce 2 blocks at most (if block isn't water)
execute if score #is_pass_through {ns}.data matches 0 if score $raycast.piercing bs.lambda matches 1..3 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score #is_pass_through {ns}.data matches 0 if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 3

# Reduce damage by 5% in water, and 50% in other blocks
execute store result score #new_damage {ns}.data run data get storage {ns}:temp damage 1000
execute if score #is_pass_through {ns}.data matches 0 store result storage {ns}:temp damage float 0.0005 run scoreboard players get #new_damage {ns}.data
execute if score #is_pass_through {ns}.data matches 1 store result storage {ns}:temp damage float 0.00095 run scoreboard players get #new_damage {ns}.data

## Playsounds
# Each sound type has a scoreboard objective that tracks if it has been played.
# The score is set to 1 when the sound plays, preventing it from playing again.
# The 'run return run' command ensures only one sound tries to play per block hit
# (e.g. if water already played and it's water again, it will not trigger soft)
execute if score #is_pass_through {ns}.data matches 1 run return run execute if score #played_water {ns}.data matches 0 store success score #played_water {ns}.data run playsound minecraft:entity.axolotl.splash block @a[distance=..24] ~ ~ ~ 0.8 1.5
execute if block ~ ~ ~ #{ns}:v{version}/sounds/glass run return run execute if score #played_glass {ns}.data matches 0 store success score #played_glass {ns}.data run playsound minecraft:block.glass.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/cloth run return run execute if score #played_cloth {ns}.data matches 0 store success score #played_cloth {ns}.data run playsound {ns}:common/cloth_bullet_impact block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/dirt run return run execute if score #played_dirt {ns}.data matches 0 store success score #played_dirt {ns}.data run playsound {ns}:common/dirt_bullet_impact block @a[distance=..24] ~ ~ ~ 0.3
execute if block ~ ~ ~ #{ns}:v{version}/sounds/mud run return run execute if score #played_mud {ns}.data matches 0 store success score #played_mud {ns}.data run playsound {ns}:common/mud_bullet_impact block @a[distance=..24] ~ ~ ~ 0.4
execute if block ~ ~ ~ #{ns}:v{version}/sounds/wood run return run execute if score #played_wood {ns}.data matches 0 store success score #played_wood {ns}.data run playsound {ns}:common/wood_bullet_impact block @a[distance=..24] ~ ~ ~ 0.5
execute if block ~ ~ ~ #{ns}:v{version}/plant run return run execute if score #played_plant {ns}.data matches 0 store success score #played_plant {ns}.data run playsound minecraft:block.azalea_leaves.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/solid run return run execute if score #played_solid {ns}.data matches 0 store success score #played_solid {ns}.data run playsound {ns}:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #played_soft {ns}.data matches 0 store success score #played_soft {ns}.data run playsound {ns}:common/soft_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
""")  # noqa: E501

    # On targeted entity
    write_versioned_function("raycast/on_targeted_entity",
f"""
# Blood particles
scoreboard players set #last_callback {ns}.data 2
particle block{{block_state:"redstone_wire"}} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Get base damage with 3 digits of precision
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@p[tag={ns}.ticking]"}}
execute store result score #damage {ns}.data run data get storage {ns}:temp damage 10

# Apply decay and headshot calculations
function {ns}:v{version}/raycast/apply_decay
function {ns}:v{version}/raycast/check_headshot

# Damage entity
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #damage {ns}.data
function {ns}:v{version}/utils/damage with storage {ns}:input with
""")

    # Apply decay using `damage *= pow(decay, distance / 10)`
    write_versioned_function("raycast/apply_decay",
f"""
## Apply decay using `damage *= pow(decay, distance / 10)`
# Get decay into x
data modify storage bs:in math.pow.x set from storage {ns}:gun all.stats.{DECAY}

# Get raycast distance / 10 into y
execute store result score #raycast_distance {ns}.data run data get storage bs:lambda raycast.distance 1000000
scoreboard players operation #raycast_distance {ns}.data /= #10 {ns}.data
execute store result storage bs:in math.pow.y float 0.000001 run scoreboard players get #raycast_distance {ns}.data

# Compute power using https://docs.mcbookshelf.dev/en/latest/modules/math.html#power
function #bs.math:pow

# Collect computed value and multiply to the damage
execute store result score #pow_decay_distance {ns}.data run data get storage bs:out math.pow 1000000
scoreboard players operation #damage {ns}.data *= #pow_decay_distance {ns}.data

# Divide by 1000000 because we're multiplying two scaled integers with each other (10*1000000 = 10000000)
scoreboard players operation #damage {ns}.data /= #1000000 {ns}.data
""")

    # Check if hit is a headshot and adjust damage accordingly
    write_versioned_function("raycast/check_headshot",
f"""
scoreboard players set #is_headshot {ns}.data 0
execute store result score #entity_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #hit_y {ns}.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff {ns}.data = #hit_y {ns}.data
scoreboard players operation #y_diff {ns}.data -= #entity_y {ns}.data
execute if score #y_diff {ns}.data matches 1200.. run scoreboard players set #is_headshot {ns}.data 1
execute unless score #is_headshot {ns}.data matches 1 run scoreboard players operation #damage {ns}.data /= #2 {ns}.data
""")


    ## Accuracy
    # Get values
    write_versioned_function("raycast/accuracy/get_value",
f"""
## Order is important: Jump > Sneak > Sprint > Walk > Base
data remove storage {ns}:gun accuracy

# If not on ground, return jump accuracy
execute unless predicate {ns}:v{version}/is_on_ground run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_JUMP}

# If sneaking, return sneak accuracy
execute if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_SNEAK}

# If sprinting, return sprint accuracy
execute if predicate {ns}:v{version}/is_sprinting run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_SPRINT}

# If moving horizontally, return walk accuracy
execute if predicate {ns}:v{version}/is_moving run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_WALK}

# Else, return base accuracy
data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_BASE}
""")

    # Apply random rotation spread
    write_versioned_function("raycast/accuracy/apply_spread",
f"""
# Get random uniform rotation spread (https://docs.mcbookshelf.dev/en/latest/modules/random.html#random-distributions)
data modify storage {ns}:input with set value {{}}
execute store result storage {ns}:input with.min int -1 run data get storage {ns}:gun accuracy
execute store result storage {ns}:input with.max int 1 run data get storage {ns}:gun accuracy
function #bs.random:uniform with storage {ns}:input with

# Add horizontal rotation (divided by 100) (https://docs.mcbookshelf.dev/en/latest/modules/position.html#add-position-and-rotation)
scoreboard players operation @s bs.rot.h = $random.uniform bs.out
function #bs.position:add_rot_h {{scale: 0.01}}

# Get a new random rotation spread
function #bs.random:uniform with storage {ns}:input with

# Add vertical rotation (divided by 100)
scoreboard players operation @s bs.rot.v = $random.uniform bs.out
function #bs.position:add_rot_v {{scale: 0.01}}
""")

