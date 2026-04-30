
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
    GRENADE_TYPE,
    PELLET_COUNT,
    PROJECTILE_SPEED,
)


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Handle pending clicks
    write_versioned_function("player/right_click", f"""
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

# Set cooldown as expiration tick: end_tick = current_tick + cooldown_duration
execute store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
scoreboard players operation #cooldown {ns}.data += #total_tick {ns}.data
scoreboard players operation @s {ns}.cooldown = #cooldown {ns}.data

# Route to the appropriate firing method (projectile or hitscan)
function {ns}:v{version}/player/fire_weapon

# Signal: on_shoot (weapon data available in mgs:signals)
data modify storage {ns}:signals on_shoot set value {{}}
data modify storage {ns}:signals on_shoot.weapon set from storage {ns}:gun all
function #{ns}:signals/on_shoot
""")

    # Fire weapon routing: grenade vs projectile vs hitscan
    write_versioned_function("player/fire_weapon", f"""
# For weapons with pellet count, set bullets_to_fire appropriately
execute if data storage {ns}:gun all.stats.{PELLET_COUNT} store result score #bullets_to_fire {ns}.data run data get storage {ns}:gun all.stats.{PELLET_COUNT}

# If weapon is a grenade, throw it instead
execute if data storage {ns}:gun all.stats.{GRENADE_TYPE} run return run function {ns}:v{version}/grenade/throw

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage {ns}:gun all.stats.{PROJECTILE_SPEED} run return run function {ns}:v{version}/projectile/summon_loop

# Shoot with hitscan raycast
function {ns}:v{version}/player/shoot
""")

    # Initialize burst mode pending clicks
    write_versioned_function("player/init_burst_clicks", f"""
# Calculate (BURST - 1) * COOLDOWN
execute store result score #burst_clicks {ns}.data run data get storage {ns}:gun all.stats.{BURST}
scoreboard players remove #burst_clicks {ns}.data 1
execute store result score #cooldown_value {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
scoreboard players operation #burst_clicks {ns}.data *= #cooldown_value {ns}.data

# Set pending_clicks to sustain burst firing
scoreboard players operation @s {ns}.pending_clicks = #burst_clicks {ns}.data
""")

    # Handle pending clicks
    write_versioned_function("player/shoot", f"""
# Check which type of movement the player is doing
function {ns}:v{version}/raycast/accuracy/get_value

# Shoot with raycast & launch cloud particle forward
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^2 run particle minecraft:cloud ~ ~ ~ ^ ^ ^1000000000 0.00000002 0 force @a[tag=!bs.raycast.omit,distance=..32]
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/player/shoot
""")

    # Handle pending clicks
    write_versioned_function("raycast/main", f"""
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
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.entities set value true
data modify storage {ns}:input with.piercing set value 10
data modify storage {ns}:input with.max_distance set value 128
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.ignored_entities set value "#{ns}:ignore"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/raycast/on_entry_point"
data modify storage {ns}:input with.on_targeted_block set value "function {ns}:v{version}/raycast/on_targeted_block"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/raycast/on_targeted_entity"
data modify storage {ns}:input with.on_exit_point set value "function {ns}:v{version}/raycast/on_exit_point"

# Launch raycast with callbacks (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast)
execute at @s run function #bs.raycast:run with storage {ns}:input

# Kill marker
kill @s
""")

    # On exit point - headshot calculation and damage
    write_versioned_function("raycast/on_exit_point", f"""
# If entity, calculate headshot and apply damage to entity
execute if score #is_entity_hit {ns}.data matches 1 as @e[tag={ns}.raycast_target] run function {ns}:v{version}/raycast/headshot_and_damage
scoreboard players set #is_entity_hit {ns}.data 0
""")

    # On entry point
    write_versioned_function("raycast/on_entry_point", f"""
# If targeted entity, return to prevent showing particles
execute if score #is_entity_hit {ns}.data matches 1 run return 0

# Make block particles (if not passing through) (on_targeted_block runs first to set passing through)
data modify storage {ns}:input with set value {{block:"minecraft:air"}}
data modify storage {ns}:input with.block set from storage {ns}:temp block.type
execute if score #is_pass_through {ns}.data matches 0 run return run function {ns}:v{version}/raycast/block_particles with storage {ns}:input with

# Change particles if passing through
execute if score #is_water {ns}.data matches 1 run data modify storage {ns}:input with.block set value "minecraft:bubble"
execute if score #is_water {ns}.data matches 0 run data modify storage {ns}:input with.block set value "minecraft:mycelium"

# Create particles every third iteration to maintain visual clarity while reducing particle density
scoreboard players add #next_air_particle {ns}.data 1
execute if score #next_air_particle {ns}.data matches 2 run function {ns}:v{version}/raycast/air_particles with storage {ns}:input with
execute if score #next_air_particle {ns}.data matches 3.. run scoreboard players set #next_air_particle {ns}.data 0
""")
    write_versioned_function("raycast/block_particles", r"""$particle block{block_state:"$(block)"} ~ ~ ~ 0.1 0.1 0.1 1 10 force @a[distance=..128]""")
    write_versioned_function("raycast/air_particles", r"""$particle $(block) ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]""")

    # On targeted block
    write_versioned_function("raycast/on_targeted_block", f"""
# Get current block (https://docs.mcbookshelf.dev/en/latest/modules/block.html#get)
scoreboard players set #is_entity_hit {ns}.data 0
scoreboard players set #is_water {ns}.data 0
scoreboard players set #is_pass_through {ns}.data 0
execute if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through {ns}.data 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/water run scoreboard players set #is_water {ns}.data 1
function #bs.block:get_type
data modify storage {ns}:temp block set from storage bs:out block
#tellraw @a {{"nbt":"block","storage":"{ns}:temp","interpret":false}}

# If the block can be passed through, increment back piercing, and stop here if it's not water
execute if score #is_pass_through {ns}.data matches 1 run scoreboard players add $raycast.piercing bs.lambda 1
execute if score #is_pass_through {ns}.data matches 1 unless block ~ ~ ~ #{ns}:v{version}/sounds/water run return 1

# For water/pass-through: reduce damage by 5%
execute if score #is_pass_through {ns}.data matches 1 store result score #new_damage {ns}.data run data get storage {ns}:temp damage 1000
execute if score #is_pass_through {ns}.data matches 1 store result storage {ns}:temp damage float 0.00095 run scoreboard players get #new_damage {ns}.data

# For solid blocks: lookup hardness
execute if score #is_pass_through {ns}.data matches 0 run function #bs.block:lookup_type with storage bs:out block
execute if score #is_pass_through {ns}.data matches 0 store result score #hardness {ns}.data run data get storage bs:out block.hardness 1000

# Indestructible blocks (bedrock, barriers, hardness=-1): stop bullet completely
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches ..-1 run data modify storage {ns}:temp damage set value 0.0d
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches ..-1 run return 0

# Piercing: cap on first solid block hit (initial piercing is 10, cap to 6)
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 0.. if score $raycast.piercing bs.lambda matches 7.. run scoreboard players set $raycast.piercing bs.lambda 6
# Reduce piercing based on hardness tiers (directly in callback for lambda score access)
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 0..299 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 300..999 run scoreboard players remove $raycast.piercing bs.lambda 2
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 1000..2999 run scoreboard players remove $raycast.piercing bs.lambda 3
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 3000.. run scoreboard players set $raycast.piercing bs.lambda 0

# Clamp piercing to 0 (Bookshelf raycast only stops at exactly 0, not negative)
execute if score #is_pass_through {ns}.data matches 0 if score $raycast.piercing bs.lambda matches ..-1 run scoreboard players set $raycast.piercing bs.lambda 0

# Apply hardness damage reduction (non-indestructible solid blocks only)
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 0.. run function {ns}:v{version}/raycast/apply_block_hardness

# Signal: on_hit_block (only for solid blocks, @s = raycast marker, positioned at block)
execute if score #is_pass_through {ns}.data matches 0 run data modify storage {ns}:signals on_hit_block set value {{}}
execute if score #is_pass_through {ns}.data matches 0 run data modify storage {ns}:signals on_hit_block.block set from storage {ns}:temp block
execute if score #is_pass_through {ns}.data matches 0 run data modify storage {ns}:signals on_hit_block.weapon set from storage {ns}:gun all
execute if score #is_pass_through {ns}.data matches 0 run function #{ns}:signals/on_hit_block

# Hard blocks (hardness >= 1.0): play impact sound and stop the ray
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 1000.. if score #played_solid {ns}.data matches 0 store success score #played_solid {ns}.data run playsound {ns}:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 1000.. run return 0

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

    # Apply block hardness-based damage reduction (called from on_targeted_block, #hardness already set)
    write_versioned_function("raycast/apply_block_hardness", f"""
#tellraw @a[distance=..128] [{{"text":"Hardness: ","color":"gray","extra":[{{"score":{{"name":"#hardness","objective":"{ns}.data"}},"color":"white"}}]}},{{"text":" $raycast.piercing bs.lambda: ","color":"gray","extra":[{{"score":{{"name":"$raycast.piercing","objective":"bs.lambda"}},"color":"white"}}]}}]

# Calculate damage reduction: reduction = hardness * 400 / 1000, capped at 950
scoreboard players operation #reduction {ns}.data = #hardness {ns}.data
scoreboard players operation #reduction {ns}.data /= #10 {ns}.data
scoreboard players operation #reduction {ns}.data *= #2 {ns}.data
scoreboard players operation #reduction {ns}.data *= #2 {ns}.data
execute if score #reduction {ns}.data matches 951.. run scoreboard players set #reduction {ns}.data 950

# Apply: damage = damage * (1000 - reduction) / 1000
execute store result score #new_damage {ns}.data run data get storage {ns}:temp damage 1000
scoreboard players set #remaining_pct {ns}.data 1000
scoreboard players operation #remaining_pct {ns}.data -= #reduction {ns}.data
scoreboard players operation #new_damage {ns}.data *= #remaining_pct {ns}.data
scoreboard players operation #new_damage {ns}.data /= #1000 {ns}.data
execute store result storage {ns}:temp damage float 0.001 run scoreboard players get #new_damage {ns}.data
""")  # noqa: E501

    # On targeted entity
    write_versioned_function("raycast/on_targeted_entity", f"""
# Friendly fire check: skip if target is a teammate (but not the shooter themselves)
execute if entity @s[type=player,gamemode=spectator] run return 0
execute if entity @s[type=player] unless entity @s[tag={ns}.ticking] store result score #shooter_team {ns}.data run scoreboard players get @n[tag={ns}.ticking] {ns}.mp.team
execute if entity @s[type=player] unless entity @s[tag={ns}.ticking] if score #shooter_team {ns}.data matches 1.. if score @s {ns}.mp.team = #shooter_team {ns}.data run return fail

# Mark that we hit an entity
scoreboard players set #is_entity_hit {ns}.data 1
tag @s add {ns}.raycast_target

# Blood particles
execute at @s run particle block{{block_state:"redstone_wire"}} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Store attack info and calculate decay
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.ticking]"}}
execute if entity @n[tag={ns}.ticking,type=player] run data modify storage {ns}:input with.attacker set value "@p[tag={ns}.ticking]"
execute store result score #damage {ns}.data run data get storage {ns}:temp damage 10
function {ns}:v{version}/raycast/apply_decay
""")

    # Apply decay using `damage *= pow(decay, distance / 10)`
    write_versioned_function("raycast/apply_decay", f"""
## Apply decay using `damage *= pow(decay, distance / 10)`
# Get decay into x
data modify storage bs:in math.pow.x set from storage {ns}:gun all.stats.{DECAY}

# Get raycast distance / 10 into y
execute store result score #raycast_distance {ns}.data run scoreboard players get $raycast.entry_distance bs.lambda
scoreboard players operation #raycast_distance {ns}.data /= #10 {ns}.data
execute store result storage bs:in math.pow.y float 0.001 run scoreboard players get #raycast_distance {ns}.data

# Compute power using https://docs.mcbookshelf.dev/en/latest/modules/math.html#power
function #bs.math:pow

# Collect computed value and multiply to the damage
execute store result score #pow_decay_distance {ns}.data run data get storage bs:out math.pow 1000
scoreboard players operation #damage {ns}.data *= #pow_decay_distance {ns}.data

# Divide by 1000 because we're multiplying two scaled integers with each other (10*1000 = 10000)
scoreboard players operation #damage {ns}.data /= #1000 {ns}.data
""")

    # Calculate headshot bonus based on center distance and apply damage
    write_versioned_function("raycast/headshot_and_damage", f"""
# Remove raycast target tag
tag @s remove {ns}.raycast_target

# Check if in head zone (Y above 1400 relative to entity), if not apply normal damage
scoreboard players set #is_headshot {ns}.data 0
scoreboard players set #headshot_multiplier {ns}.data 1000
execute unless score $raycast.entry_point.y bs.lambda matches 1400.. at @s run return run function {ns}:v{version}/raycast/apply_damage

# Calculate center of trajectory through head: ((entry_x + exit_x) / 2, (entry_z + exit_z) / 2)
execute store result score #entry_x {ns}.data run scoreboard players get $raycast.entry_point.x bs.lambda
execute store result score #entry_z {ns}.data run scoreboard players get $raycast.entry_point.z bs.lambda
execute store result score #exit_x {ns}.data run scoreboard players get $raycast.exit_point.x bs.lambda
execute store result score #exit_z {ns}.data run scoreboard players get $raycast.exit_point.z bs.lambda

scoreboard players operation #exit_x {ns}.data += #entry_x {ns}.data
scoreboard players operation #exit_z {ns}.data += #entry_z {ns}.data
scoreboard players operation #exit_x {ns}.data /= #2 {ns}.data
scoreboard players operation #exit_z {ns}.data /= #2 {ns}.data

scoreboard players set #dist_sq {ns}.data 0
scoreboard players operation #dist_sq {ns}.data = #exit_x {ns}.data
scoreboard players operation #dist_sq {ns}.data *= #exit_x {ns}.data
scoreboard players operation #exit_z {ns}.data *= #exit_z {ns}.data
scoreboard players operation #dist_sq {ns}.data += #exit_z {ns}.data

# Get integer square root: https://docs.mcbookshelf.dev/en/latest/modules/math/#square-root
scoreboard players operation $math.isqrt.x bs.in = #dist_sq {ns}.data
function #bs.math:isqrt
scoreboard players operation #distance {ns}.data = $math.isqrt bs.out

# Clamp distance to 500 (0.5 block)
execute if score #distance {ns}.data matches 501.. run scoreboard players set #distance {ns}.data 500

# Calculate multiplier: 2000 - (distance * 2)
scoreboard players set #headshot_multiplier {ns}.data 2000
scoreboard players operation #distance {ns}.data *= #2 {ns}.data
scoreboard players operation #headshot_multiplier {ns}.data -= #distance {ns}.data

# Apply multiplier to damage
scoreboard players operation #damage {ns}.data *= #headshot_multiplier {ns}.data
scoreboard players operation #damage {ns}.data /= #1000 {ns}.data

# Apply damage
scoreboard players set #is_headshot {ns}.data 1
execute at @s run function {ns}:v{version}/raycast/apply_damage
""")

    # Apply final damage and signals
    write_versioned_function("raycast/apply_damage", f"""
# Instant kill check
execute as @n[tag={ns}.ticking] if score @s {ns}.special.instant_kill matches 1.. as @s[tag=!{ns}.no_instant_kill] run scoreboard players set #damage {ns}.data 99999

# Signal: on_headshot
execute if score #is_headshot {ns}.data matches 1 run data modify storage {ns}:signals on_headshot set value {{}}
execute if score #is_headshot {ns}.data matches 1 run data modify storage {ns}:signals on_headshot.weapon set from storage {ns}:gun all
execute if score #is_headshot {ns}.data matches 1 store result storage {ns}:signals on_headshot.damage float 0.1 run scoreboard players get #damage {ns}.data
execute if score #is_headshot {ns}.data matches 1 run function #{ns}:signals/on_headshot

# Damage entity
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #damage {ns}.data
data modify storage {ns}:input with.weapon set from storage {ns}:gun all
execute store result storage {ns}:input with.headshot int 1 run scoreboard players get #is_headshot {ns}.data
function {ns}:v{version}/utils/signal_and_damage

# Signal: on_kill (guard against double-fire on already-dying entities)
scoreboard players set #victim_hp {ns}.data 0
execute store result score #victim_hp {ns}.data run data get entity @s Health 100
scoreboard players set #is_new_kill {ns}.data 0
execute if score #victim_hp {ns}.data matches ..0 unless entity @s[tag={ns}.already_killed] run scoreboard players set #is_new_kill {ns}.data 1
execute if score #victim_hp {ns}.data matches ..0 unless entity @s[tag={ns}.already_killed] run tag @s add {ns}.already_killed
execute if score #is_new_kill {ns}.data matches 1 run data modify storage {ns}:signals on_kill set value {{}}
execute if score #is_new_kill {ns}.data matches 1 run data modify storage {ns}:signals on_kill.weapon set from storage {ns}:gun all
execute if score #is_new_kill {ns}.data matches 1 as @n[tag={ns}.ticking] run function #{ns}:signals/on_kill
""")


    ## Accuracy
    # Get values
    write_versioned_function("raycast/accuracy/get_value", f"""
## Order is important: Sneak+Air=Walk > Jump > Sneak > Sprint > Walk > Base
data remove storage {ns}:gun accuracy

# If sneaking in the air, treat as walking (not jump accuracy)
execute unless predicate {ns}:v{version}/is_on_ground if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_WALK}

# If not on ground (and not sneaking), return jump accuracy
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
    write_versioned_function("raycast/accuracy/apply_spread", f"""
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

