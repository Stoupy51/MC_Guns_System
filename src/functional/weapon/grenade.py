
# ruff: noqa: E501
# Imports
from beet import Font, Texture
from PIL import Image
from stewbeet import ItemModifier, Mem, set_json_encoder, write_tick_file, write_versioned_function

from ...config.stats import (
    EXPLOSION_DAMAGE,
    EXPLOSION_DECAY,
    EXPLOSION_RADIUS,
    GRENADE_DURATION,
    GRENADE_EFFECT_RADIUS,
    GRENADE_FUSE,
    GRENADE_TYPE,
    PROJECTILE_GRAVITY,
    PROJECTILE_MODEL,
    PROJECTILE_SPEED,
    REMAINING_BULLETS,
)


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Create item modifier to consume one grenade from the stack
    Mem.ctx.data[ns].item_modifiers[f"v{version}/grenade/consume_one"] = set_json_encoder(
        ItemModifier({"function": "minecraft:set_count", "count": -1, "add": True}),
        max_level=-1
    )

    # Create white pixel texture for flash grenade screen fill
    white_pixel = Image.new("RGB", (1, 1), (255, 255, 255))
    Mem.ctx.assets.textures[f"{ns}:font/flash_white"] = Texture(white_pixel)

    # Add font provider for flash screen (1x1 white pixel scaled to fill the screen)
    flash_font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:flash", Font({"providers": []}))
    flash_font.data["providers"].append({
        "type": "bitmap",
        "file": f"{ns}:font/flash_white.png",
        "ascent": 4000,
        "height": 8000,
        "chars": ["F"]
    })

    ## Throw grenade (called from fire_weapon when grenade_type is present)
    write_versioned_function("grenade/throw",
f"""
# Prepare grenade data in storage before summoning
data modify storage {ns}:temp grenade set value {{}}
data modify storage {ns}:temp grenade.{GRENADE_TYPE} set from storage {ns}:gun all.stats.{GRENADE_TYPE}
data modify storage {ns}:temp grenade.{GRENADE_FUSE} set from storage {ns}:gun all.stats.{GRENADE_FUSE}
data modify storage {ns}:temp grenade.{GRENADE_DURATION} set from storage {ns}:gun all.stats.{GRENADE_DURATION}
data modify storage {ns}:temp grenade.{GRENADE_EFFECT_RADIUS} set from storage {ns}:gun all.stats.{GRENADE_EFFECT_RADIUS}
data modify storage {ns}:temp grenade.{EXPLOSION_DAMAGE} set from storage {ns}:gun all.stats.{EXPLOSION_DAMAGE}
data modify storage {ns}:temp grenade.{EXPLOSION_DECAY} set from storage {ns}:gun all.stats.{EXPLOSION_DECAY}
data modify storage {ns}:temp grenade.{EXPLOSION_RADIUS} set from storage {ns}:gun all.stats.{EXPLOSION_RADIUS}
data modify storage {ns}:temp grenade.{PROJECTILE_GRAVITY} set from storage {ns}:gun all.stats.{PROJECTILE_GRAVITY}
data modify storage {ns}:temp grenade.{PROJECTILE_SPEED} set from storage {ns}:gun all.stats.{PROJECTILE_SPEED}
data modify storage {ns}:temp grenade.{PROJECTILE_MODEL} set from storage {ns}:gun all.stats.{PROJECTILE_MODEL}

# Summon loop (supports pellet_count for multiple grenades)
function {ns}:v{version}/grenade/summon_loop

# Consume one grenade from the stack (decrease count by 1) - skip if infinite ammo
execute unless score @s {ns}.special.infinite_ammo matches 1.. run item modify entity @p[tag={ns}.ticking] weapon.mainhand {ns}:v{version}/grenade/consume_one

# Set remaining_bullets to 2 so ammo/decrease (which runs after) reduces it to 1 for the next throw
scoreboard players set @s {ns}.{REMAINING_BULLETS} 2
""")

    ## Summon loop (supports pellet_count for multiple grenades)
    write_versioned_function("grenade/summon_loop",
f"""
# Summon a grenade
function {ns}:v{version}/grenade/summon

# Loop for remaining grenades
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/grenade/summon_loop
""")

    ## Summon a single grenade entity
    write_versioned_function("grenade/summon",
f"""
# Get accuracy value and apply spread
function {ns}:v{version}/raycast/accuracy/get_value

# Summon the grenade entity at the player's eye position
execute anchored eyes positioned ^ ^ ^0.5 summon item_display run function {ns}:v{version}/grenade/init

# Increment grenade counter
scoreboard players add #grenade_count {ns}.data 1
""")

    ## Initialize the newly summoned grenade entity
    write_versioned_function("grenade/init",
f"""
# Tag as grenade
tag @s add {ns}.grenade

# Store shooter UUID for damage attribution
data modify entity @s data.shooter set from entity @n[tag={ns}.ticking] UUID

# Copy grenade config from temp storage
data modify entity @s data.config set from storage {ns}:temp grenade

# Set the visual model on the item_display entity
function {ns}:v{version}/grenade/set_model with entity @s data.config

# Set fuse timer from config
execute store result score @s {ns}.data run data get entity @s data.config.{GRENADE_FUSE}

# Launch grace period: disable entity collision for 3 ticks to avoid sticking to the thrower
scoreboard players set @s {ns}.grenade_launch 3

# Calculate velocity from the player's look direction
# Step 1: Record current position
execute store result score #proj_ox {ns}.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy {ns}.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz {ns}.data run data get entity @s Pos[2] 1000

# Step 2: Apply accuracy spread to the grenade's rotation
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
execute store result storage {ns}:temp grenade_pos.x double 0.001 run scoreboard players get #proj_ox {ns}.data
execute store result storage {ns}:temp grenade_pos.y double 0.001 run scoreboard players get #proj_oy {ns}.data
execute store result storage {ns}:temp grenade_pos.z double 0.001 run scoreboard players get #proj_oz {ns}.data
function {ns}:v{version}/grenade/tp_back with storage {ns}:temp grenade_pos
""")

    # Set visual model on the item_display (macro function)
    write_versioned_function("grenade/set_model",
f"""
$data modify entity @s item set value {{id:"minecraft:paper", count:1, components:{{"minecraft:item_model":"{ns}:$({PROJECTILE_MODEL})"}}}}
data modify entity @s item_display set value "fixed"
data modify entity @s brightness set value {{sky: 15, block: 15}}
data modify entity @s teleport_duration set value 1
""")

    # Teleport back to original position (macro function)
    write_versioned_function("grenade/tp_back",
"""
$tp @s $(x) $(y) $(z)
""")

    ## Tick function for each grenade entity
    write_versioned_function("grenade/tick",
f"""
# Skip if grenade is stuck (semtex on a surface) or in smoke/flash effect phase
execute if entity @s[tag={ns}.grenade_stuck] run return run function {ns}:v{version}/grenade/tick_stuck
execute if entity @s[tag={ns}.grenade_active_effect] run return run function {ns}:v{version}/grenade/tick_effect

# Apply gravity (subtract from Y velocity)
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Move the grenade using Bookshelf's move module with collision detection
# Grenades use damped_bounce by default (frag/smoke/flash) or stick (semtex)
execute if data entity @s data.config{{{GRENADE_TYPE}:"semtex"}} run return run function {ns}:v{version}/grenade/move_semtex
function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:false,on_collision:"function {ns}:v{version}/grenade/on_bounce"}}}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Decrement fuse timer
scoreboard players remove @s {ns}.data 1

# If fuse expired, detonate
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

    ## Move semtex (uses stick collision instead of bounce)
    write_versioned_function("grenade/move_semtex",
f"""
# Apply gravity
execute store result score #proj_gravity {ns}.data run data get entity @s data.config.{PROJECTILE_GRAVITY}
scoreboard players operation @s bs.vel.y -= #proj_gravity {ns}.data

# Move with stick callback (semtex sticks to first surface or entity hit)
# During launch grace period, skip entity collision to avoid sticking to the thrower
scoreboard players remove @s {ns}.grenade_launch 1
execute if score @s {ns}.grenade_launch matches 0.. run function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:false,on_collision:"function {ns}:v{version}/grenade/on_stick"}}}}
execute unless score @s {ns}.grenade_launch matches 0.. run function #bs.move:apply_vel {{scale:0.001,with:{{blocks:true,entities:true,on_collision:"function {ns}:v{version}/grenade/on_stick"}}}}

# Trail particle (white_smoke avoids false-positive with shader marker detection)
particle white_smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1 force @a[distance=..64]

# Decrement fuse timer
scoreboard players remove @s {ns}.data 1

# If fuse expired, detonate
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

    ## Bounce collision callback (for frag/smoke/flash grenades)
    write_versioned_function("grenade/on_bounce",
"""
# Apply damped bounce (reduce velocity and reverse direction on collision axis)
function #bs.move:callback/damped_bounce

# Play bounce sound
playsound minecraft:entity.item.pickup player @a[distance=..32] ~ ~ ~ 0.5 0.5
""")

    ## Stick collision callback (for semtex)
    write_versioned_function("grenade/on_stick",
f"""
# Stop all velocity (stick to the surface)
function #bs.move:callback/stick

# Mark as stuck so tick skips movement
tag @s add {ns}.grenade_stuck

# If we hit an entity (hit_flag = -1 for entities), pair the grenade with the target
execute if score $move.hit_flag bs.lambda matches -1 run function {ns}:v{version}/grenade/stick_to_entity

# Play stick sound
playsound minecraft:block.honey_block.place player @a[distance=..32] ~ ~ ~ 1 1.2
""")

    ## Pair semtex grenade with target entity using unique scoreboard ID
    write_versioned_function("grenade/stick_to_entity",
f"""
# Increment the global semtex pairing counter to get a unique ID
scoreboard players add #semtex_id {ns}.data 1

# Assign the same unique ID to both the grenade and the nearest entity
scoreboard players operation @s {ns}.stuck_id = #semtex_id {ns}.data
execute positioned ~ ~-1 ~ run scoreboard players operation @e[type=!#{ns}:non_damageable,sort=nearest,limit=1,distance=..2,tag=!{ns}.grenade,tag=!{ns}.slow_bullet] {ns}.stuck_id = #semtex_id {ns}.data

# Mark that this grenade is stuck to an entity (not just a block)
tag @s add {ns}.stuck_to_entity
""")

    ## Tick for stuck grenades (just countdown)
    write_versioned_function("grenade/tick_stuck",
f"""
# If stuck to an entity, follow it
execute if entity @s[tag={ns}.stuck_to_entity] run function {ns}:v{version}/grenade/follow_entity

# Decrement fuse timer
scoreboard players remove @s {ns}.data 1

# Blinking particle to indicate it's about to explode
particle small_flame ~ ~0.3 ~ 0 0 0 0 1 force @a[distance=..32]

# If fuse expired, detonate
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/detonate
""")

    ## Follow the paired entity (teleport grenade to entity's position)
    write_versioned_function("grenade/follow_entity",
f"""
# Tag myself for the teleportation
tag @s add {ns}.tp_me

# Read my stuck ID
scoreboard players operation #my_stuck {ns}.data = @s {ns}.stuck_id

# Find the entity with matching stuck_id (not a grenade) and teleport me to it
execute as @e[scores={{{ns}.stuck_id=1..}}] if score @s {ns}.stuck_id = #my_stuck {ns}.data unless entity @s[tag={ns}.grenade] at @s run tp @e[tag={ns}.tp_me,limit=1] ~ ~ ~

# Remove temp tag
tag @s remove {ns}.tp_me
""")

    ## Detonation router - dispatch based on grenade type
    write_versioned_function("grenade/detonate",
f"""
# Route to the appropriate detonation effect based on grenade type
execute if data entity @s data.config{{{GRENADE_TYPE}:"frag"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"semtex"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"smoke"}} run return run function {ns}:v{version}/grenade/detonate_smoke
execute if data entity @s data.config{{{GRENADE_TYPE}:"flash"}} run return run function {ns}:v{version}/grenade/detonate_flash
""")

    ## Frag/Semtex detonation - explosion with area damage (reuses projectile explosion logic)
    write_versioned_function("grenade/detonate_frag",
f"""
# Explosion particles
particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 100 force @a[distance=..128]
particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound
playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if grenade_explosion_power > 0)
execute if score #grenade_explosion_power {ns}.config matches 1.. run function {ns}:v{version}/grenade/realistic_explosion

# Store explosion center position for damage calculation
execute store result storage {ns}:temp expl.center_x int 1 run data get entity @s Pos[0] 1000
execute store result storage {ns}:temp expl.center_y int 1 run data get entity @s Pos[1] 1000
execute store result storage {ns}:temp expl.center_z int 1 run data get entity @s Pos[2] 1000

# Copy explosion config from entity data to temp storage
data modify storage {ns}:temp expl.{EXPLOSION_DAMAGE} set from entity @s data.config.{EXPLOSION_DAMAGE}
data modify storage {ns}:temp expl.{EXPLOSION_DECAY} set from entity @s data.config.{EXPLOSION_DECAY}
data modify storage {ns}:temp expl.{EXPLOSION_RADIUS} set from entity @s data.config.{EXPLOSION_RADIUS}

# Resolve shooter: copy UUID to storage, then find matching player
data modify storage {ns}:temp expl.shooter_uuid set from entity @s data.shooter

# Tag the matching shooter for damage attribution
execute as @a run function {ns}:v{version}/projectile/match_shooter

# Apply area damage to nearby entities (macro for configurable radius)
execute store result storage {ns}:temp expl.radius_int int 1 run data get entity @s data.config.{EXPLOSION_RADIUS}
function {ns}:v{version}/projectile/damage_area with storage {ns}:temp expl

# Signal: on_explosion
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
data modify storage {ns}:signals on_explosion.grenade set value true
function #{ns}:signals/on_explosion

# Clean up shooter tag
tag @a remove {ns}.temp_shooter

# Delete the grenade
function {ns}:v{version}/grenade/delete
""")

    ## Realistic block destruction for grenades
    write_versioned_function("grenade/realistic_explosion",
f"""
# Set explosion power from config and call the library
scoreboard players operation #explosion_power realistic_explosion.data = #grenade_explosion_power {ns}.config
execute if score #grenade_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #grenade_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode
""")

    ## Smoke grenade detonation - start emitting smoke particles
    write_versioned_function("grenade/detonate_smoke",
f"""
# Activation sound
playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 1 0.8
playsound minecraft:entity.generic.extinguish_fire player @a[distance=..32] ~ ~ ~ 1 0.5

# Set duration timer (reuse the fuse score for duration countdown)
execute store result score @s {ns}.data run data get entity @s data.config.{GRENADE_DURATION}

# Mark as active effect (skip movement in tick)
tag @s add {ns}.grenade_active_effect

# Stop all velocity
scoreboard players set @s bs.vel.x 0
scoreboard players set @s bs.vel.y 0
scoreboard players set @s bs.vel.z 0

# Initial burst of smoke
particle campfire_signal_smoke ~ ~ ~ 2 1 2 0.02 30 force @a[distance=..128]
""")

    ## Flash grenade detonation - blind nearby players
    write_versioned_function("grenade/detonate_flash",
f"""
# Flash sound
playsound minecraft:entity.firework_rocket.blast player @a[distance=..32] ~ ~ ~ 2 2
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..16] ~ ~ ~ 0.3 2

# Flash particles
particle flash{{color:[1.0,1.0,1.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]
particle end_rod ~ ~ ~ 1 1 1 0.1 50 force @a[distance=..64]

# Tag this grenade as the flash source for visibility checks
tag @s add {ns}.flash_source

# Apply flash to nearby players (with direction and LOS checks)
function {ns}:v{version}/grenade/flash_apply

# Remove flash source tag
tag @s remove {ns}.flash_source

# Signal: on_explosion (flash type)
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
data modify storage {ns}:signals on_explosion.grenade set value true
function #{ns}:signals/on_explosion

# Delete the grenade
function {ns}:v{version}/grenade/delete
""")

    ## Apply flash effect to nearby players (macro for configurable radius)
    write_versioned_function("grenade/flash_apply",
f"""
# Apply blindness and darkness effects to all players within radius
execute store result storage {ns}:temp flash.radius_int int 1 run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
function {ns}:v{version}/grenade/flash_area with storage {ns}:temp flash
""")

    write_versioned_function("grenade/flash_area",
f"""
$execute as @a[distance=..$(radius_int)] at @s run function {ns}:v{version}/grenade/flash_check
""")

    # Check if this player should be flashed (close range OR looking at grenade with LOS)
    write_versioned_function("grenade/flash_check",
f"""
# @s = player, position = player's position (from at @s)
# Flash source grenade is tagged {ns}.flash_source

# Close range override: within 3 blocks, always flash (too close to avoid)
execute if entity @e[tag={ns}.flash_source,distance=..3] run return run function {ns}:v{version}/grenade/flash_player

# Direction check: is the grenade within the player's field of view? (110 degree cone)
execute at @e[tag={ns}.flash_source,limit=1] store result score #in_fov {ns}.data run function #bs.view:in_view_ata {{angle:110}}
execute unless score #in_fov {ns}.data matches 1 run return 0

# Line-of-sight check: can the player see the grenade? (no blocks between)
execute at @e[tag={ns}.flash_source,limit=1] store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute unless score #can_see {ns}.data matches 1 run return 0

# Both checks passed: flash the player
function {ns}:v{version}/grenade/flash_player
""")

    write_versioned_function("grenade/flash_player",
f"""
# Apply full blindness + darkness
effect give @s minecraft:blindness 5 0 true
effect give @s minecraft:darkness 3 0 true

# White screen flash using custom font (1x1 white pixel scaled to fill screen)
title @s times 5 40 20
title @s title {{"text":"F","font":"{ns}:flash"}}
""")

    ## Tick for active effect grenades (smoke particles)
    write_versioned_function("grenade/tick_effect",
f"""
# Decrement effect duration
scoreboard players remove @s {ns}.data 1

# Emit smoke cloud particles
execute store result score #effect_r {ns}.data run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
function {ns}:v{version}/grenade/smoke_particles

# Play ambient sound occasionally (every 20 ticks)
execute store result score #smoke_tick {ns}.data run scoreboard players get @s {ns}.data
scoreboard players operation #smoke_tick {ns}.data %= #20 {ns}.data
execute if score #smoke_tick {ns}.data matches 0 run playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 0.3 0.5

# If duration expired, delete
execute if score @s {ns}.data matches ..0 run function {ns}:v{version}/grenade/delete
""")

    ## Smoke particle emission
    write_versioned_function("grenade/smoke_particles",
"""
# Dense smoke cloud within effect radius
particle campfire_signal_smoke ~ ~0.5 ~ 3 2 3 0.01 20 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~1 ~ 2 1.5 2 0.02 10 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~0.3 ~ 2.5 0.5 2.5 0.005 5 force @a[distance=..128]
""")

    ## Delete grenade entity
    write_versioned_function("grenade/delete",
f"""
# If stuck to an entity, clean up the target's stuck_id
execute if entity @s[tag={ns}.stuck_to_entity] run function {ns}:v{version}/grenade/cleanup_stuck_entity

# Decrease grenade counter and kill entity
scoreboard players remove #grenade_count {ns}.data 1
kill @s
""")

    ## Clean up stuck_id from the paired entity
    write_versioned_function("grenade/cleanup_stuck_entity",
f"""
# Read my stuck ID
scoreboard players operation #my_stuck {ns}.data = @s {ns}.stuck_id

# Find the paired entity and reset its stuck_id
execute as @e[scores={{{ns}.stuck_id=1..}}] if score @s {ns}.stuck_id = #my_stuck {ns}.data unless entity @s[tag={ns}.grenade] run scoreboard players reset @s {ns}.stuck_id
""")

    ## Tick file entry for grenade movement
    write_tick_file(
f"""
# Tick function for active grenades
execute if score #grenade_count {ns}.data matches 1.. as @e[tag={ns}.grenade] at @s run function {ns}:v{version}/grenade/tick
""")
