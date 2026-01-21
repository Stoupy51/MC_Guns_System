
# Imports
from typing import Any

from stewbeet import ItemModifier, Mem, set_json_encoder, write_versioned_function

from ...config.stats import CAN_AUTO, CAN_BURST, FIRE_MODE, SWITCH, WEAPON_ID


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Weapon switching main function
    write_versioned_function("switch/main",
f"""
# Set weapon id if not done yet
execute if data storage {ns}:gun all.gun unless data storage {ns}:gun all.stats.{WEAPON_ID} run function {ns}:v{version}/switch/set_weapon_id

# If last_selected is different from this one, set cooldown
scoreboard players set #current_id {ns}.data 0
execute store result score #current_id {ns}.data run data get storage {ns}:gun all.stats.{WEAPON_ID}
execute unless score @s {ns}.last_selected = #current_id {ns}.data run function {ns}:v{version}/switch/on_weapon_switch

# Update last selected
scoreboard players operation @s {ns}.last_selected = #current_id {ns}.data
""")

    # Set weapon id function and item modifier
    write_versioned_function("switch/set_weapon_id",
f"""
execute store result storage {ns}:gun all.stats.{WEAPON_ID} int 1 run scoreboard players add #next_id {ns}.data 1

# Initialize fire mode to 'auto' if weapon supports it, otherwise 'semi'
execute unless data storage {ns}:gun all.stats.{FIRE_MODE} if data storage {ns}:gun all.stats.{CAN_AUTO} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "auto"
execute unless data storage {ns}:gun all.stats.{FIRE_MODE} unless data storage {ns}:gun all.stats.{CAN_AUTO} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "semi"

item modify entity @s weapon.mainhand {ns}:v{version}/set_weapon_id
""")

    # On weapon switch function
    write_versioned_function("switch/on_weapon_switch",
f"""
# Apply weapon switch cooldown only if it exceeds the current cooldown value
execute store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{SWITCH}
execute if score #cooldown {ns}.data > @s {ns}.cooldown run scoreboard players operation @s {ns}.cooldown = #cooldown {ns}.data

# Force weapon switch animation
function {ns}:v{version}/switch/force_switch_animation
""")

    # Swap weapon function
    write_versioned_function("switch/force_switch_animation",
f"""
# Stop if no weapon in hand
execute unless data storage {ns}:gun all.gun run return fail

# Modify attack_speed attribute modifier to sync with current cooldown
function {ns}:v{version}/switch/sync_attack_speed_with_cooldown

# Swap weapon in hand if same as previously selected (26 chars long = "minecraft:poisonous_potato")
execute store result score #current_length {ns}.data run data get storage {ns}:gun SelectedItem.id
execute if score #current_length {ns}.data = @s {ns}.previous_selected if score @s {ns}.previous_selected matches 26 run item modify entity @s weapon.mainhand {{"function": "minecraft:set_item","item": "minecraft:firework_star"}}
execute if score #current_length {ns}.data = @s {ns}.previous_selected unless score @s {ns}.previous_selected matches 26 run item modify entity @s weapon.mainhand {{"function": "minecraft:set_item","item": "minecraft:poisonous_potato"}}
""")  # noqa: E501

    # Sync attack speed with cooldown function
    write_versioned_function("switch/sync_attack_speed_with_cooldown",
f"""
## Formula: [attack_speed = (20.0 / cooldown) - 4.0] <- where 4.0 is default attack speed
# Compute attack speed based of @s {ns}.cooldown (with 3 digits precision)
scoreboard players set #attack_speed {ns}.data 20000
scoreboard players operation #attack_speed {ns}.data /= @s {ns}.cooldown
scoreboard players remove #attack_speed {ns}.data 4000

# Summon a temporary entity that will be used to modify the attack speed attribute modifier from the player's mainhand slot
tag @s add {ns}.to_modify
execute summon item_display run function {ns}:v{version}/switch/modify_attack_speed
tag @s remove {ns}.to_modify
""")

    # Modify attack speed function
    write_versioned_function("switch/modify_attack_speed",
f"""
# Copy weapon from player's mainhand slot to item_display entity
item replace entity @s contents from entity @p[tag={ns}.to_modify] weapon.mainhand

# Modify attack speed attribute modifier
execute unless data entity @s item.components."minecraft:attribute_modifiers" run data modify entity @s item.components."minecraft:attribute_modifiers" set value []
execute unless data entity @s item.components."minecraft:attribute_modifiers"[{{"type":"minecraft:attack_speed"}}] run data modify entity @s item.components."minecraft:attribute_modifiers" append value {{"type":"attack_speed","amount":0.0d,"operation":"add_value","slot":"mainhand","id":"minecraft:base_attack_speed"}}
execute store result entity @s item.components."minecraft:attribute_modifiers"[{{"type":"minecraft:attack_speed"}}].amount double 0.001 run scoreboard players get #attack_speed {ns}.data

# Modify tooltip display
data modify entity @s item.components."minecraft:tooltip_display" set value {{"hide_tooltip":false,"hidden_components":["minecraft:attribute_modifiers"]}}

# Copy back weapon to player's mainhand slot
item replace entity @p[tag={ns}.to_modify] weapon.mainhand from entity @s contents

# Kill item_display entity
kill @s
""")  # noqa: E501



    # Check for fire mode toggle (weapon drop)
    write_versioned_function("switch/check_fire_mode_toggle",
f"""
# Check if player dropped a weapon
execute if score @s {ns}.dropped matches 1.. run function {ns}:v{version}/switch/toggle_fire_mode
scoreboard players reset @s {ns}.dropped
""")

    # Toggle fire mode function
    write_versioned_function("switch/toggle_fire_mode",
f"""
# Find nearest dropped gun item and execute as it (only if mainhand is empty)
execute unless items entity @s weapon.mainhand * as @n[type=item,distance=..3,nbt={{Item:{{components:{{"minecraft:custom_data":{{{ns}:{{gun:true}}}}}}}}}}] run function {ns}:v{version}/switch/do_toggle

# Force weapon switch animation
function {ns}:v{version}/switch/force_switch_animation
""")  # noqa: E501

    # Do the actual toggle
    write_versioned_function("switch/do_toggle",
f"""
# Get current fire mode
data modify storage {ns}:temp fire_mode set from entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE}

# Check weapon capabilities
execute store result score #has_auto {ns}.data if data entity @s Item.components."minecraft:custom_data".{ns}.stats.{CAN_AUTO}
execute store result score #has_burst {ns}.data if data entity @s Item.components."minecraft:custom_data".{ns}.stats.{CAN_BURST}

# 3-way toggle for weapons with auto and burst: auto -> semi -> burst -> auto
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"auto"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "semi"
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"semi"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "burst"
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"burst"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "auto"

# 2-way toggle for weapons with auto but no burst: auto -> semi -> auto
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 0 if data storage {ns}:temp {{fire_mode:"auto"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "semi"
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 0 if data storage {ns}:temp {{fire_mode:"semi"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "auto"

# 2-way toggle for weapons with burst but no auto: semi -> burst -> semi
execute if score #has_auto {ns}.data matches 0 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"semi"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "burst"
execute if score #has_auto {ns}.data matches 0 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"burst"}} run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "semi"

# Weapons with neither auto nor burst stay on semi (should not happen)
# Default to auto if missing and weapon supports it, otherwise semi
execute unless data storage {ns}:temp fire_mode if score #has_auto {ns}.data matches 1 run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "auto"
execute unless data storage {ns}:temp fire_mode if score #has_auto {ns}.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".{ns}.stats.{FIRE_MODE} set value "semi"

# Give item back to player's mainhand and kill the item entity
item replace entity @p weapon.mainhand from entity @s contents
kill @s

# Play feedback sound
playsound minecraft:block.note_block.hat ambient @p
""")  # noqa: E501

    modifier: dict[str, Any] = {
        "function": "minecraft:copy_custom_data",
        "source": {
            "type": "minecraft:storage",
            "source": f"{ns}:gun"
        },
        "ops": [
            {
                "source": f"all.stats.{WEAPON_ID}",
                "target": f"{ns}.stats.{WEAPON_ID}",
                "op": "replace"
            },
            {
                "source": f"all.stats.{FIRE_MODE}",
                "target": f"{ns}.stats.{FIRE_MODE}",
                "op": "replace"
            }
        ]
    }
    Mem.ctx.data[ns].item_modifiers[f"v{version}/set_weapon_id"] = set_json_encoder(ItemModifier(modifier), max_level=-1)
