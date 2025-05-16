
# Imports
import stouputils as stp
from python_datapack.utils.database_helper import write_predicate, write_versioned_function

from user.config.stats import ACCURACY_BASE, ACCURACY_JUMP, ACCURACY_SNEAK, ACCURACY_SPRINT, ACCURACY_WALK, DAMAGE, DECAY


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Check which type of movement the player is doing
function {ns}:v{version}/raycast/accuracy/get_value

# Shoot with raycast
tag @s add {ns}.attacker
tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove {ns}.attacker
""")

    # Handle pending clicks
    write_versioned_function(config, "raycast/main",
f"""
# Handle accuracy
tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Prepare arguments
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value true
data modify storage {ns}:input with.entities set value true
data modify storage {ns}:input with.piercing set value 10
data modify storage {ns}:input with.max_distance set value 128
data modify storage {ns}:input with.hitbox_shape set value "interaction"
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/air"
data modify storage {ns}:input with.on_hit_point set value "function {ns}:v{version}/raycast/on_hit_point"
data modify storage {ns}:input with.on_targeted_block set value "function {ns}:v{version}/raycast/on_targeted_block"
data modify storage {ns}:input with.on_targeted_entity set value "function {ns}:v{version}/raycast/on_targeted_entity"

# Launch raycast with callbacks (https://docs.mcbookshelf.dev/en/latest/modules/raycast.html#run-the-raycast)
execute at @s run function #bs.raycast:run with storage {ns}:input
""")

    # On hit point
    write_versioned_function(config, "raycast/on_hit_point",
f"""
# If targeted entity, return to prevent showing particles
execute if data storage bs:lambda raycast.targeted_entity run return fail

# Get current block (https://docs.mcbookshelf.dev/en/latest/modules/block.html#get)
data modify storage {ns}:temp Pos set from entity @s Pos
data modify entity @s Pos set from storage bs:lambda raycast.targeted_block
execute at @s run function #bs.block:get_block
data modify entity @s Pos set from storage {ns}:temp Pos

# Make block particles
data modify storage {ns}:input with set value {{x:0,y:0,z:0,block:"minecraft:air"}}
data modify storage {ns}:input with.block set from storage bs:out block.type
data modify storage {ns}:input with.x set from storage bs:lambda raycast.hit_point[0]
data modify storage {ns}:input with.y set from storage bs:lambda raycast.hit_point[1]
data modify storage {ns}:input with.z set from storage bs:lambda raycast.hit_point[2]
execute unless data storage {ns}:input with{{block:"minecraft:air"}} run return run function {ns}:v{version}/raycast/block_particles with storage {ns}:input with
""")

    # On targeted block
    write_versioned_function(config, "raycast/on_targeted_block",
f"""
# Allow bullets to pierce 2 blocks at most
execute if score $raycast.piercing bs.lambda matches 1..3 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 3

# Divide damage per 2
execute store result storage {ns}:gun stats.{DAMAGE} float 0.5 run data get storage {ns}:gun stats.{DAMAGE}

execute if block ~ ~ ~ #{ns}:v{version}/sounds/glass run playsound minecraft:block.glass.break block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/water run playsound minecraft:ambient.underwater.exit block @a ~ ~ ~ 0.25 1.5
execute if block ~ ~ ~ #{ns}:v{version}/sounds/cloth run playsound {ns}:common.cloth_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/dirt run playsound {ns}:common.dirt_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/mud run playsound {ns}:common.mud_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/wood run playsound {ns}:common.wood_bullet_impact block @a ~ ~ ~ 1
""")
    write_versioned_function(config, "raycast/block_particles", """$particle block{block_state:"$(block)"} $(x) $(y) $(z) 0.1 0.1 0.1 1 10 force @a[distance=..128]""")

    # On targeted entity
    write_versioned_function(config, "raycast/on_targeted_entity",
f"""
# Blood particles
particle block{{block_state:"redstone_wire"}} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Get base damage with 3 digits of precision
data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@p[tag={ns}.attacker]"}}
execute store result score #damage {ns}.data run data get storage {ns}:gun stats.{DAMAGE} 10

# Apply decay using `damage *= pow(decay, distance)` (https://docs.mcbookshelf.dev/en/latest/modules/math.html#power)
data modify storage bs:in math.pow.x set from storage {ns}:gun stats.{DECAY}
data modify storage bs:in math.pow.y set from storage bs:lambda raycast.distance
function #bs.math:pow
execute store result score #pow_decay_distance {ns}.data run data get storage bs:out math.pow 1000000
scoreboard players operation #damage {ns}.data *= #pow_decay_distance {ns}.data

# Divide by 1000000 because we're multiplying two scaled integers with each other (10*1000000 = 10000000)
scoreboard players operation #damage {ns}.data /= #1000000 {ns}.data

# Divide damage by 2 if not headshot
scoreboard players set #is_headshot {ns}.data 0
execute store result score #entity_y {ns}.data run data get entity @s Pos[1] 1000
execute store result score #hit_y {ns}.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff {ns}.data = #hit_y {ns}.data
scoreboard players operation #y_diff {ns}.data -= #entity_y {ns}.data
execute if score #y_diff {ns}.data matches 1200.. run scoreboard players set #is_headshot {ns}.data 1
execute unless score #is_headshot {ns}.data matches 1 run scoreboard players operation #damage {ns}.data /= #2 {ns}.data

# Damage entity
execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #damage {ns}.data
function {ns}:v{version}/utils/damage with storage {ns}:input with
""")


    ## Accuracy
    # Prepare predicates for accuracy checks
    write_predicate(config, f"{ns}:v{version}/is_on_ground", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_on_ground":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_sprinting", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sprinting":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_sneaking", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sneaking":True}}}))
    write_predicate(config, f"{ns}:v{version}/is_moving", stp.super_json_dump({"condition":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"horizontal_speed":{"min":0.1}}}}))

    # Get values
    write_versioned_function(config, "raycast/accuracy/get_value",
f"""
## Order is important: Jump > Sprint > Sneak > Walk > Base
data remove storage {ns}:gun accuracy

# If not on ground, return jump accuracy
execute unless predicate {ns}:v{version}/is_on_ground run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun stats.{ACCURACY_JUMP}

# If sprinting, return sprint accuracy
execute if predicate {ns}:v{version}/is_sprinting run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun stats.{ACCURACY_SPRINT}

# If sneaking, return sneak accuracy
execute if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun stats.{ACCURACY_SNEAK}

# If moving horizontally, return walk accuracy
execute if predicate {ns}:v{version}/is_moving run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun stats.{ACCURACY_WALK}

# Else, return base accuracy
data modify storage {ns}:gun accuracy set from storage {ns}:gun stats.{ACCURACY_BASE}
""")

    # Apply random rotation spread
    write_versioned_function(config, "raycast/accuracy/apply_spread",
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

