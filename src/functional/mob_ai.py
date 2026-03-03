# Imports
from stewbeet import Mem, write_load_file, write_tick_file, write_versioned_function

from ..config.stats import ACCURACY_BASE, COOLDOWN, GRENADE_TYPE, PELLET_COUNT, PROJECTILE_SPEED


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Scoreboards for mob AI
    write_load_file(
f"""
# Armed mob counter (skip tick loop if 0)
scoreboard players add #armed_mob_count {ns}.data 0

# Mob AI phase timer, active time, and sleep time
scoreboard objectives add {ns}.mob.timer dummy
scoreboard objectives add {ns}.mob.active_time dummy
scoreboard objectives add {ns}.mob.sleep_time dummy
""")

    ## Mob tick function
    write_versioned_function("mob/tick",
f"""
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

# Copy gun data from equipment mainhand to shared storage
function {ns}:v{version}/mob/copy_gun_data

# Check if we have valid gun data
execute unless data storage {ns}:gun all.stats run return 0

# Pick target: last attacker if in range, otherwise nearest player
execute on attacker run tag @s add {ns}.target
execute unless entity @e[tag={ns}.target] run tag @p[distance=..64,gamemode=!spectator,gamemode=!creative] add {ns}.target

# No target in range, skip
execute unless entity @e[tag={ns}.target] run return 0

# Line-of-sight check: can the mob see the target?
execute positioned as @n[tag={ns}.target] store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute unless score #can_see {ns}.data matches 1 run return run tag @e[tag={ns}.target] remove {ns}.target

# Tag as ticking (for compatibility with existing damage/raycast system)
tag @s add {ns}.ticking

# Aim at target and fire
execute anchored eyes facing entity @n[tag={ns}.target] feet run function {ns}:v{version}/mob/fire_weapon

# Remove tags
tag @e[tag={ns}.target] remove {ns}.target
tag @s remove {ns}.ticking
""")

    ## Initialize a newly tagged armed mob
    write_versioned_function("mob/init",
f"""
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
    write_versioned_function("mob/wake_up",
f"""
# Remove sleeping tag and set timer to active duration
tag @s remove {ns}.mob_sleeping
scoreboard players operation @s {ns}.mob.timer = @s {ns}.mob.active_time
""")

    ## Transition from active to sleeping phase
    write_versioned_function("mob/go_sleep",
f"""
# Add sleeping tag and set timer to sleep duration
tag @s add {ns}.mob_sleeping
scoreboard players operation @s {ns}.mob.timer = @s {ns}.mob.sleep_time
""")

    ## Copy gun data from mob's equipment mainhand to shared storage
    write_versioned_function("mob/copy_gun_data",
f"""
# Copy gun data from equipment mainhand
data remove storage {ns}:gun all
data modify storage {ns}:gun all set from entity @s equipment.mainhand.components."minecraft:custom_data".{ns}
""")

    ## Fire weapon routing
    write_versioned_function("mob/fire_weapon",
f"""
# Rotate to face the target eyes
rotate @s facing entity @n[tag={ns}.target] eyes

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
    write_versioned_function("mob/shoot",
f"""
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
    write_versioned_function("mob/fire_sound",
f"""
$playsound {ns}:$(fire) player @a[distance=..48] ~ ~ ~ 0.75
""")

    ## Tick file entry for armed mobs
    write_tick_file(
f"""
# Armed mob AI loop
execute if score #armed_mob_count {ns}.data matches 1.. as @e[tag={ns}.armed] at @s run function {ns}:v{version}/mob/tick
""")

    ## Simple example functions
    for level, active, sleep in [(1, 50, 100), (2, 50, 50), (3, 60, 20), (4, 72000, 1)]:
        write_versioned_function(f"mob/example/level_{level}",
f"""
# Summon entity with armed tag and custom name
$summon $(entity) ~ ~ ~ {{"Tags":["{ns}.armed","{ns}.new"],"CustomName":{{"text":"Armed $(entity) [Lv.{level}]","color":"red"}}}}

# Give a random weapon to the entity
execute as @n[tag={ns}.new] run function {ns}:v{version}/utils/random_weapon {{slot:"weapon.mainhand"}}

# Set mob active time and sleep time
scoreboard players set @n[tag={ns}.new] {ns}.mob.active_time {active}
scoreboard players set @n[tag={ns}.new] {ns}.mob.sleep_time {sleep}

# Increment armed mob count & Clean up new tag
scoreboard players add #armed_mob_count {ns}.data 1
tag @n[tag={ns}.new] remove {ns}.new
""")

