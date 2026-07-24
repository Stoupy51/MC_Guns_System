
# Imports
from stewbeet import Mem, write_function, write_load_file, write_tick_file, write_versioned_function

from ..config.stats import ACCURACY_BASE, COOLDOWN, GRENADE_TYPE, PELLET_COUNT, PROJECTILE_SPEED

# Main function


def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Scoreboards for mob AI
    write_load_file(f"""
# Armed mob counter (skip tick loop if 0)
scoreboard players add #armed_mob_count {ns}.data 0

# Mob AI phase timer, active time, and sleep time
scoreboard objectives add {ns}.mob.timer dummy
scoreboard objectives add {ns}.mob.active_time dummy
scoreboard objectives add {ns}.mob.sleep_time dummy
""")

    ## Mob tick function
    write_versioned_function("mob/tick", f"""
# Initialize mob if not yet initialized
execute unless entity @s[tag={ns}.mob_init] run function {ns}:v{version}/mob/init

# Phase timer management: decrement timer
execute if score @s {ns}.mob.timer matches 1.. run scoreboard players remove @s {ns}.mob.timer 1

# Phase transitions when timer reaches 0
execute if score @s {ns}.mob.timer matches 0 if entity @s[tag={ns}.mob_sleeping] run function {ns}:v{version}/mob/wake_up
execute if score @s {ns}.mob.timer matches 0 unless entity @s[tag={ns}.mob_sleeping] unless score @s {ns}.mob.sleep_time matches 0 run function {ns}:v{version}/mob/go_sleep

# If sleeping, skip everything
execute if entity @s[tag={ns}.mob_sleeping] run return 0

# Decrease weapon cooldown by 1
execute if score @s {ns}.cooldown matches 1.. run scoreboard players remove @s {ns}.cooldown 1

# If cooldown is active, skip shooting
execute if score @s {ns}.cooldown matches 1.. run return 0

# Pick target BEFORE paying the equipment-NBT gun copy: last attacker, otherwise nearest player.
# Scores (not @e[tag=] existence rescans) carry "did we find anyone" between the two paths.
scoreboard players set #mob_has_target {ns}.data 0
execute store success score #mob_has_target {ns}.data on attacker run tag @s add {ns}.target

# `on attacker` outlives the fight: a player who shot this mob and then died stays its attacker, so
# the mob kept firing at the corpse-camera. Drop a target that is no longer a live participant
# (spectator = dead and waiting to respawn, creative = admin) and fall through to the search below.
# The untag scan is gated on the rare bad case instead of running on every mob tick.
scoreboard players set #mob_dead_target {ns}.data 0
execute if score #mob_has_target {ns}.data matches 1 if entity @a[tag={ns}.target,gamemode=!adventure,gamemode=!survival] run scoreboard players set #mob_dead_target {ns}.data 1
execute if score #mob_dead_target {ns}.data matches 1 run scoreboard players set #mob_has_target {ns}.data 0
execute if score #mob_dead_target {ns}.data matches 1 run tag @a[tag={ns}.target] remove {ns}.target

# Fall back to the nearest player. Two rules this block has to respect, both of which silently
# broke mobs before:
#  - the result goes to a scratch score, because `execute store success` writes 0 whenever a guard
#    on the same chain filters the command out. Writing straight to #mob_has_target zeroed the
#    attacker hit above, so any mob that had ever been shot never fired again.
#  - "is a player in range" is asked separately from `tag ... add`, which reports failure when the
#    tag is merely already present — otherwise one leaked tag wedges the mob permanently.
scoreboard players set #mob_near_target {ns}.data 0
execute if score #mob_has_target {ns}.data matches 0 if entity @p[distance=..64,gamemode=!spectator,gamemode=!creative] run scoreboard players set #mob_near_target {ns}.data 1
execute if score #mob_near_target {ns}.data matches 1 run tag @p[distance=..64,gamemode=!spectator,gamemode=!creative] add {ns}.target
scoreboard players operation #mob_has_target {ns}.data > #mob_near_target {ns}.data

# No target in range, skip
execute if score #mob_has_target {ns}.data matches 0 run return 0

# Copy gun data from equipment mainhand to shared storage
function {ns}:v{version}/mob/copy_gun_data

# Check we have valid gun data (clean the target tag up on the way out)
execute unless data storage {ns}:gun all.stats run return run tag @e[tag={ns}.target,limit=1] remove {ns}.target

# Line-of-sight check: can the mob see the target? (limit=1 skips the @n distance sort — the
# tag is only ever on one entity)
scoreboard players set #can_see {ns}.data 0
execute positioned as @e[tag={ns}.target,limit=1] store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute unless score #can_see {ns}.data matches 1 run return run tag @e[tag={ns}.target,limit=1] remove {ns}.target

# Tag as ticking (for compatibility with existing damage/raycast system)
tag @s add {ns}.ticking

# Aim at target and fire
execute anchored eyes facing entity @e[tag={ns}.target,limit=1] feet run function {ns}:v{version}/mob/fire_weapon

# Remove tags
tag @e[tag={ns}.target,limit=1] remove {ns}.target
tag @s remove {ns}.ticking
""")

    ## Initialize a newly tagged armed mob
    write_versioned_function("mob/init", f"""
# Mark as initialized
tag @s add {ns}.mob_init

# Default active_time to 50 ticks if not set
execute unless score @s {ns}.mob.active_time matches 1.. run scoreboard players set @s {ns}.mob.active_time 50

# Default sleep_time to 100 ticks if not set
execute unless score @s {ns}.mob.sleep_time matches 0.. run scoreboard players set @s {ns}.mob.sleep_time 100

# Initialize cooldown to 1 second
scoreboard players set @s {ns}.cooldown 20

# Start in active phase
function {ns}:v{version}/mob/wake_up
""")

    ## Transition from sleeping to active phase
    write_versioned_function("mob/wake_up", f"""
# Remove sleeping tag and set timer to active duration
tag @s remove {ns}.mob_sleeping
scoreboard players operation @s {ns}.mob.timer = @s {ns}.mob.active_time
""")

    ## Transition from active to sleeping phase
    write_versioned_function("mob/go_sleep", f"""
# Add sleeping tag and set timer to sleep duration
tag @s add {ns}.mob_sleeping
scoreboard players operation @s {ns}.mob.timer = @s {ns}.mob.sleep_time
""")

    ## Copy gun data from mob's equipment mainhand to shared storage
    write_versioned_function("mob/copy_gun_data", f"""
# Copy gun data from equipment mainhand
data remove storage {ns}:gun all
data modify storage {ns}:gun all set from entity @s equipment.mainhand.components."minecraft:custom_data".{ns}
""")

    ## Apply random rotation offset for inaccuracy (non-level-5 mobs only)
    write_versioned_function("mob/apply_inaccuracy", f"""
# Random yaw offset: -20.0 to +20.0 degrees (stored as -200..200, applied with 0.1 scale)
execute store result storage {ns}:temp _rot.yaw double 0.1 run random value -200..200
execute store result storage {ns}:temp _rot.pitch double 0.1 run random value -200..200
function {ns}:v{version}/mob/apply_rotation_offset with storage {ns}:temp _rot
""")

    ## Apply rotation offset (macro)
    write_versioned_function("mob/apply_rotation_offset", """
$rotate @s ~$(yaw) ~$(pitch)
""")

    ## Fire weapon routing
    write_versioned_function("mob/fire_weapon", f"""
# Rotate to face the target eyes
rotate @s facing entity @n[tag={ns}.target] eyes

# Apply random inaccuracy (skip for level 5 mobs with perfect aim)
execute unless entity @s[tag={ns}.mob_lv5] run function {ns}:v{version}/mob/apply_inaccuracy

# Set cooldown from weapon stats
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{COOLDOWN}

# For weapons with pellet count, set bullets_to_fire appropriately
scoreboard players set #bullets_to_fire {ns}.data 1
execute if data storage {ns}:gun all.stats.{PELLET_COUNT} store result score #bullets_to_fire {ns}.data run data get storage {ns}:gun all.stats.{PELLET_COUNT}

# If weapon is a grenade, throw it instead
execute if data storage {ns}:gun all.stats.{GRENADE_TYPE} run return run function {ns}:v{version}/grenade/throw

# If weapon has projectile config, fire slow projectile(s) instead of instant raycast
execute if data storage {ns}:gun all.stats.{PROJECTILE_SPEED} run return run function {ns}:v{version}/projectile/summon_loop

# Shoot with hitscan raycast
function {ns}:v{version}/mob/shoot

# Play fire sound to nearby players
execute if data storage {ns}:gun all.sounds.fire run function {ns}:v{version}/mob/fire_sound with storage {ns}:gun all.sounds

# Signal: on_shoot (weapon data available in {ns}:signals)
data modify storage {ns}:signals on_shoot set value {{}}
data modify storage {ns}:signals on_shoot.weapon set from storage {ns}:gun all
function #{ns}:signals/on_shoot
""")

    ## Mob shoot function
    write_versioned_function("mob/shoot", f"""
# Set accuracy (mobs use base accuracy)
data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_BASE}

# Shoot with raycast
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove bs.raycast.omit

# Decrease bullets to fire & loop if needed
scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/mob/shoot
""")

    ## Fire sound for mobs
    write_versioned_function("mob/fire_sound", f"""
$playsound {ns}:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10
""")

    ## Tick file entry for armed mobs
    write_tick_file(
f"""
# Armed mob AI loop
execute if score #armed_mob_count {ns}.data matches 1.. as @e[tag={ns}.armed] at @s run function {ns}:v{version}/mob/tick

# Resync armed mob count every 5 seconds (mobs dying never decrement the counter)
scoreboard players operation #armed_mob_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #armed_mob_phase {ns}.data %= #100 {ns}.data
execute if score #armed_mob_count {ns}.data matches 1.. if score #armed_mob_phase {ns}.data matches 0 store result score #armed_mob_count {ns}.data if entity @e[tag={ns}.armed]
""")

    ## Simple default functions
    write_versioned_function("mob/default/on_new", f"""
# Tags, data, and attributes
tag @s add {ns}.armed
$data modify entity @s CustomName set value {{"text":"Armed $(entity) [Lv.$(level)]","color":"red"}}
data modify entity @s DeathLootTable set value "minecraft:empty"
data modify entity @s drop_chances set value {{mainhand:0.0f,offhand:0.0f}}
data modify entity @s PersistenceRequired set value true
attribute @s minecraft:waypoint_transmit_range base set 32

# Give a random weapon to the entity
function {ns}:v{version}/utils/random_weapon {{slot:"weapon.mainhand"}}

# Set mob active time and sleep time
$scoreboard players set @s {ns}.mob.active_time $(active_time)
$scoreboard players set @s {ns}.mob.sleep_time $(sleep_time)

# Increment armed mob count
scoreboard players add #armed_mob_count {ns}.data 1
""")
    # Level 5: perfect accuracy (always active, no sleep, tagged to skip inaccuracy)
    write_versioned_function("mob/default/on_new_lv5", f"""
# Tags, data, and attributes
$function {ns}:v{version}/mob/default/on_new {{entity:"$(entity)",level:5,active_time:72000,sleep_time:0}}
tag @s add {ns}.mob_lv5
""")

    # Version-independent entrypoints: map storage persists across version bumps, so saved enemy
    # functions must not embed the pack version (a map saved on v5.0.1 kept calling a dead path,
    # spawning 0 enemies and instantly completing the mission).
    for level, active, sleep in [(1, 50, 100), (2, 50, 50), (3, 60, 20), (4, 72000, 1)]:
        write_function(
            f"{ns}:mob/default/level_{level}",
            f"""$execute summon $(entity) run function {ns}:v{version}/mob/default/on_new {{entity:"$(entity)",level:{level},active_time:{active},sleep_time:{sleep}}}"""
        )
    write_function(
        f"{ns}:mob/default/level_5",
        f"""$execute summon $(entity) run function {ns}:v{version}/mob/default/on_new_lv5 {{entity:"$(entity)"}}"""
    )

