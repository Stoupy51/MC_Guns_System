
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ...config.stats import (
    BASE_WEAPON,
    DAMAGE,
    EXPLOSION_DAMAGE,
    EXPLOSION_DECAY,
    EXPLOSION_RADIUS,
    PROJECTILE_GRAVITY,
    PROJECTILE_LIFETIME,
    PROJECTILE_MODEL,
    PROJECTILE_SPEED,
)


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    ## Summon loop (supports pellet_count for multiple projectiles)
    write_versioned_function("projectile/summon_loop",
f"""
# Summon a projectile
function {ns}:v{version}/projectile/summon

# Loop for remaining pellets
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/projectile/summon_loop
""")

    ## Summon projectile
    # Called from projectile/summon_loop
    write_versioned_function("projectile/summon",
f"""
# Get accuracy value and apply spread
function {ns}:v{version}/raycast/accuracy/get_value

# Prepare projectile data in storage before summoning
data modify storage {ns}:temp proj set value {{}}
data modify storage {ns}:temp proj.{EXPLOSION_DAMAGE} set from storage {ns}:gun all.stats.{EXPLOSION_DAMAGE}
data modify storage {ns}:temp proj.{EXPLOSION_DECAY} set from storage {ns}:gun all.stats.{EXPLOSION_DECAY}
data modify storage {ns}:temp proj.{EXPLOSION_RADIUS} set from storage {ns}:gun all.stats.{EXPLOSION_RADIUS}
data modify storage {ns}:temp proj.{DAMAGE} set from storage {ns}:gun all.stats.{DAMAGE}
data modify storage {ns}:temp proj.{PROJECTILE_GRAVITY} set from storage {ns}:gun all.stats.{PROJECTILE_GRAVITY}
data modify storage {ns}:temp proj.{PROJECTILE_SPEED} set from storage {ns}:gun all.stats.{PROJECTILE_SPEED}
data modify storage {ns}:temp proj.{PROJECTILE_LIFETIME} set from storage {ns}:gun all.stats.{PROJECTILE_LIFETIME}
data modify storage {ns}:temp proj.{PROJECTILE_MODEL} set from storage {ns}:gun all.stats.{PROJECTILE_MODEL}
data modify storage {ns}:temp proj.{BASE_WEAPON} set from storage {ns}:gun all.stats.{BASE_WEAPON}

# Summon the projectile entity at the player's eye position
execute anchored eyes positioned ^ ^ ^0.69 summon item_display run function {ns}:v{version}/projectile/init

# Increment slow bullet counter
scoreboard players add #slow_bullet_count {ns}.data 1
""")

    ## Initialize the newly summoned projectile marker
    write_versioned_function("projectile/init",
f"""
# Tag as slow bullet
tag @s add {ns}.slow_bullet

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag={ns}.ticking] UUID

# Copy explosion and projectile config from temp storage
data modify entity @s data.config set from storage {ns}:temp proj

# Set the visual model on the item_display entity (ray_gun is invisible - no projectile model)
execute store success score #is_ray_gun {ns}.data if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}}
execute if score #is_ray_gun {ns}.data matches 0 run function {ns}:v{version}/projectile/set_model with entity @s data.config

# Set lifetime score
execute store result score @s {ns}.data run data get storage {ns}:temp proj.{PROJECTILE_LIFETIME}

# Calculate velocity from the player's look direction
# Step 1: Record current position for teleporting back later
execute store result score #proj_ox {ns}.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy {ns}.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz {ns}.data run data get entity @s Pos[2] 1000

# Step 2: Apply accuracy spread to the marker's rotation
tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Step 3: Get direction vector by teleporting from origin (avoids subtraction)
execute positioned 0.0 0.0 0.0 positioned ^ ^ ^1 run tp @s ~ ~ ~

# Step 4: Read direction directly as velocity components (thousandths of a block)
execute store result score #proj_vx {ns}.data run data get entity @s Pos[0] 1000
execute store result score #proj_vy {ns}.data run data get entity @s Pos[1] 1000
execute store result score #proj_vz {ns}.data run data get entity @s Pos[2] 1000

# Step 5: Multiply direction by speed / 1000 to get velocity
execute store result score #proj_speed {ns}.data run data get entity @s data.config.{PROJECTILE_SPEED}
scoreboard players operation #proj_vx {ns}.data *= #proj_speed {ns}.data
scoreboard players operation #proj_vy {ns}.data *= #proj_speed {ns}.data
scoreboard players operation #proj_vz {ns}.data *= #proj_speed {ns}.data
scoreboard players operation #proj_vx {ns}.data /= #1000 {ns}.data
scoreboard players operation #proj_vy {ns}.data /= #1000 {ns}.data
scoreboard players operation #proj_vz {ns}.data /= #1000 {ns}.data

# Step 6: Store velocity into bs.vel scores for bs.move module
scoreboard players operation @s bs.vel.x = #proj_vx {ns}.data
scoreboard players operation @s bs.vel.y = #proj_vy {ns}.data
scoreboard players operation @s bs.vel.z = #proj_vz {ns}.data

# Step 7: Teleport back to original position
execute store result storage {ns}:temp proj_pos.x double 0.001 run scoreboard players get #proj_ox {ns}.data
execute store result storage {ns}:temp proj_pos.y double 0.001 run scoreboard players get #proj_oy {ns}.data
execute store result storage {ns}:temp proj_pos.z double 0.001 run scoreboard players get #proj_oz {ns}.data
function {ns}:v{version}/projectile/tp_back with storage {ns}:temp proj_pos
""")

    # Set visual model on the item_display (macro function)
    write_versioned_function("projectile/set_model",
f"""
$data modify entity @s item set value {{id:"minecraft:paper", count:1, components:{{"minecraft:item_model":"{ns}:$({PROJECTILE_MODEL})"}}}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {{sky: 15, block: 15}}
""")

    # Teleport back to original position (macro function)
    write_versioned_function("projectile/tp_back",
"""
$tp @s $(x) $(y) $(z)
""")

    ## Tick function for each projectile entity
    write_versioned_function("projectile/tick",
f"""
# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Move the projectile using Bookshelf's move module with collision detection
function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:true,on_collision:"function {ns}:v{version}/projectile/on_collision"}}}}

# If collision was detected, explode and stop processing
execute at @s run function {ns}:v{version}/projectile/post_vel
""")
    write_versioned_function("projectile/post_vel",
f"""
# If collision was detected, explode and stop processing
execute if entity @s[tag={ns}.exploding] run return run function {ns}:v{version}/projectile/explode

# Trail particles: ray_gun = green dust swirl, others = flame + smoke
execute store success score #is_ray_gun {ns}.data if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}}
execute if score #is_ray_gun {ns}.data matches 1 run particle dust{{color:[0.0,0.8,0.0],scale:1.5}} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 1 run particle glow ~ ~ ~ 0.1 0.1 0.1 0 3 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 0 run particle flame ~ ~ ~ 0.05 0.05 0.05 0.02 3 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 0 run particle smoke ~ ~ ~ 0.1 0.1 0.1 0.01 2 force @a[distance=..128]

# Decrement lifetime
scoreboard players remove @s {ns}.data 1

# If lifetime expired, explode
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/projectile/explode
""")

    ## Collision callback (called by bs.move:apply_vel when hitting a block or entity)
    write_versioned_function("projectile/on_collision",
f"""
# Tag the nearest non-immune entity as directly hit (for bullet damage in explode)
# distance=..2.5 covers feet-to-head hit at any entity height up to 2.5 blocks
execute as @n[distance=..2.5,type=!#bs.hitbox:intangible,tag=!{ns}.slow_bullet] run tag @s add {ns}.direct_hit

# Mark for explosion
tag @s add {ns}.exploding

# Stop all remaining velocity to prevent further movement
scoreboard players set $move.vel.x bs.lambda 0
scoreboard players set $move.vel.y bs.lambda 0
scoreboard players set $move.vel.z bs.lambda 0
""")

    ## Explosion effect
    write_versioned_function("projectile/explode",
f"""
# Explosion particles - ray_gun: green energy burst (no smoke)
execute store success score #is_ray_gun {ns}.data if data entity @s data.config{{{BASE_WEAPON}:"ray_gun"}}
execute if score #is_ray_gun {ns}.data matches 1 run particle flash{{color:[0.0,0.8,0.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 1 run particle dust{{color:[0.0,0.8,0.0],scale:1.5}} ~ ~ ~ 0.5 0.5 0.5 0 200 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 1 run particle glow ~ ~ ~ 0.5 0.5 0.5 0.1 80 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 1 run particle electric_spark ~ ~ ~ 0.5 0.5 0.5 0.05 100 force @a[distance=..128]
# Explosion particles - standard weapons: fire + smoke
execute if score #is_ray_gun {ns}.data matches 0 run particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 0 run particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 0 run particle large_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 50 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 0 run particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
execute if score #is_ray_gun {ns}.data matches 0 run particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound - ray_gun is silent (no explosion sound)
execute if score #is_ray_gun {ns}.data matches 0 run playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if RPG_EXPLOSION_POWER > 0)
execute if score #projectile_explosion_power {ns}.config matches 1.. run function {ns}:v{version}/projectile/realistic_explosion

# Store explosion center position for damage calculation
execute store result score #ctr_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #ctr_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #ctr_z {ns}.data run data get entity @s Pos[2] 1000

# Copy explosion config from entity data to temp storage
data modify storage {ns}:temp expl.{EXPLOSION_DAMAGE} set from entity @s data.config.{EXPLOSION_DAMAGE}
data modify storage {ns}:temp expl.{EXPLOSION_DECAY} set from entity @s data.config.{EXPLOSION_DECAY}
data modify storage {ns}:temp expl.{EXPLOSION_RADIUS} set from entity @s data.config.{EXPLOSION_RADIUS}

# Resolve shooter: copy UUID to storage, then find matching player
data modify storage {ns}:temp expl.shooter_uuid set from entity @s data.shooter

# Tag the matching shooter for damage attribution
scoreboard players set #found {ns}.data 0
execute as @a run function {ns}:v{version}/projectile/match_shooter
execute if score #found {ns}.data matches 0 as @e[tag={ns}.armed] run function {ns}:v{version}/projectile/match_shooter

# Apply bullet direct-hit damage to the entity tagged in on_collision (if entity was hit, not just a block)
# Read damage amount from projectile config (@s = projectile here)
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.temp_shooter]"}}
execute store result storage {ns}:input with.amount float 0.1 run data get entity @s data.config.{DAMAGE} 10
execute as @n[tag={ns}.direct_hit,tag=!{ns}.temp_shooter] run function {ns}:v{version}/utils/signal_and_damage
tag @e[tag={ns}.direct_hit] remove {ns}.direct_hit

# Apply area damage to nearby entities (macro for configurable radius)
execute store result storage {ns}:temp expl.radius_float float 1 run data get entity @s data.config.{EXPLOSION_RADIUS}
function {ns}:v{version}/projectile/damage_area with storage {ns}:temp expl

# Signal: on_explosion (@s = projectile entity, explosion data in mgs:signals)
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
function #{ns}:signals/on_explosion

# Clean up shooter tag
tag @e[tag={ns}.temp_shooter] remove {ns}.temp_shooter

# Delete the projectile
function {ns}:v{version}/projectile/delete
""")

    ## Realistic block destruction (calls RealisticExplosionLibrary)
    write_versioned_function("projectile/realistic_explosion",
f"""
# Set explosion power from config and call the library
scoreboard players operation #explosion_power realistic_explosion.data = #projectile_explosion_power {ns}.config
execute if score #projectile_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #projectile_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode
""")

    ## Match shooter by UUID comparison
    write_versioned_function("projectile/match_shooter",
f"""
# Compare this player's UUID with the stored shooter UUID
# data modify returns 0 (no change) when values are identical, 1 when modified
data modify storage {ns}:temp copy_uuid set from entity @s UUID
execute store success score #is_match {ns}.data run data modify storage {ns}:temp copy_uuid set from storage {ns}:temp expl.shooter_uuid

# If #is_match is 0, the UUIDs were identical (no change was made), so this is the shooter
execute if score #is_match {ns}.data matches 0 run scoreboard players set #found {ns}.data 1
execute if score #is_match {ns}.data matches 0 run tag @s add {ns}.temp_shooter
""")

    ## Area damage (macro function for configurable radius)
    write_versioned_function("projectile/damage_area",
f"""
$execute as @e[type=!#bs.hitbox:intangible,distance=..$(radius_float)] run function {ns}:v{version}/projectile/damage_entity
""")

    ## Per-entity damage with distance-based falloff
    write_versioned_function("projectile/damage_entity",
f"""
# Skip non-living entities and other projectiles
# Skip the shooter (prevent self-damage from own explosions)
execute if entity @s[tag={ns}.slow_bullet] run return fail
execute if entity @s[tag={ns}.temp_shooter] run return fail

# Get this entity's position (scaled by 1000)
execute store result score #ent_x {ns}.data run data get entity @s Pos[0] 1000
execute store result score #ent_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #ent_z {ns}.data run data get entity @s Pos[2] 1000

# Calculate distance squared: dx*dx + dy*dy + dz*dz
scoreboard players operation #dx {ns}.data = #ent_x {ns}.data
scoreboard players operation #dx {ns}.data -= #ctr_x {ns}.data
scoreboard players operation #dy {ns}.data = #ent_y {ns}.data
scoreboard players operation #dy {ns}.data -= #ctr_y {ns}.data
scoreboard players operation #dz {ns}.data = #ent_z {ns}.data
scoreboard players operation #dz {ns}.data -= #ctr_z {ns}.data

# Square each component
scoreboard players operation #dx2 {ns}.data = #dx {ns}.data
scoreboard players operation #dx2 {ns}.data *= #dx {ns}.data
scoreboard players operation #dy2 {ns}.data = #dy {ns}.data
scoreboard players operation #dy2 {ns}.data *= #dy {ns}.data
scoreboard players operation #dz2 {ns}.data = #dz {ns}.data
scoreboard players operation #dz2 {ns}.data *= #dz {ns}.data

# Sum: dist_sq = dx2 + dy2 + dz2 (in millionths of blocks squared)
scoreboard players operation #dist_sq {ns}.data = #dx2 {ns}.data
scoreboard players operation #dist_sq {ns}.data += #dy2 {ns}.data
scoreboard players operation #dist_sq {ns}.data += #dz2 {ns}.data

# Get distance using sqrt (https://docs.mcbookshelf.dev/en/latest/modules/math.html#square-root)
execute store result storage bs:in math.sqrt.x double 0.000001 run scoreboard players get #dist_sq {ns}.data
function #bs.math:sqrt
# Store distance in tenths of blocks (x10) for sub-block decimal precision in decay
execute store result score #distance {ns}.data run data get storage bs:out math.sqrt 10

# Apply decay-based falloff: damage *= pow(decay, distance)
# decay into x
data modify storage bs:in math.pow.x set from storage {ns}:temp expl.{EXPLOSION_DECAY}

# distance into y (float tenths-of-blocks * 0.1 = actual block distance as float)
execute store result storage bs:in math.pow.y float 0.1 run scoreboard players get #distance {ns}.data

# Compute pow(decay, distance)
function #bs.math:pow

# Get base damage and multiply by decay factor
execute store result score #expl_dmg {ns}.data run data get storage {ns}:temp expl.{EXPLOSION_DAMAGE} 10
execute store result score #decay_factor {ns}.data run data get storage bs:out math.pow 1000000

scoreboard players operation #expl_dmg {ns}.data *= #decay_factor {ns}.data
scoreboard players operation #expl_dmg {ns}.data /= #1000000 {ns}.data

# Skip if damage is negligible (less than 0.1)
execute if score #expl_dmg {ns}.data matches ..0 run return fail

# Instant kill: if shooter has active instant kill and target is not immune, set damage to 99999
tag @n[tag={ns}.temp_shooter] add {ns}.ticking
execute as @n[tag={ns}.temp_shooter] if score @s {ns}.special.instant_kill matches 1.. as @s[tag=!{ns}.no_instant_kill] run scoreboard players set #expl_dmg {ns}.data 99999

# Apply damage using the existing damage utility
# Prepare macro arguments: target=@s, amount=damage (float with 0.1 precision), attacker=shooter
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.temp_shooter]"}}
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #expl_dmg {ns}.data
function {ns}:v{version}/utils/signal_and_damage

# Signal: on_hit_entity (@s = hit entity, weapon/damage info in mgs:signals)
data modify storage {ns}:signals on_hit_entity set value {{}}
data modify storage {ns}:signals on_hit_entity.weapon set from storage {ns}:gun all
execute store result storage {ns}:signals on_hit_entity.damage float 0.1 run scoreboard players get #expl_dmg {ns}.data
data modify storage {ns}:signals on_hit_entity.target set from entity @s UUID
function #{ns}:signals/on_hit_entity

# Signal: on_kill (if entity died after explosion damage, @s switches to shooter)
execute unless entity @s as @n[tag={ns}.temp_shooter] run data modify storage {ns}:signals on_kill set value {{}}
execute unless entity @s as @n[tag={ns}.temp_shooter] run data modify storage {ns}:signals on_kill.explosion set value true
execute unless entity @s as @n[tag={ns}.temp_shooter] run function #{ns}:signals/on_kill

# Remove temporary tag
tag @n[tag={ns}.temp_shooter] remove {ns}.ticking
""")

    ## Delete projectile
    write_versioned_function("projectile/delete",
f"""
# Decrease slow bullet counter and kill entity
scoreboard players remove #slow_bullet_count {ns}.data 1
kill @s
""")

    ## Tick file entry for projectile movement
    write_tick_file(
f"""
# Tick function for slow bullets (projectiles)
execute if score #slow_bullet_count {ns}.data matches 1.. as @e[tag={ns}.slow_bullet] at @s run function {ns}:v{version}/projectile/tick
""")

