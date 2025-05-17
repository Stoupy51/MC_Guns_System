
# Imports

from python_datapack.utils.database_helper import write_versioned_function


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle zoom functionality
    write_versioned_function(config, "zoom/main",
f"""
# If no gun data, stop here
execute unless data storage {ns}:gun stats run return run function {ns}:v{version}/zoom/check_slowness

# If already zoom and not sneaking, unzoom
execute if data storage {ns}:gun stats.is_zoom unless predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/remove

# If not zooming but sneaking, zoom
execute unless data storage {ns}:gun stats.is_zoom if predicate {ns}:v{version}/is_sneaking run return run function {ns}:v{version}/zoom/set
""")

    # Function to remove zoom state
    write_versioned_function(config, "zoom/remove",
f"""
# Remove zoom state from gun stats
data remove storage {ns}:gun stats.is_zoom

# Prepare input storage for model update
data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun stats.models.normal

# Update weapon model and stats
function {ns}:v{version}/utils/update_model with storage {ns}:input with
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats

# Reset zoom state and remove slowness effect
scoreboard players reset @s {ns}.zoom
effect clear @s slowness
""")

    # Function to set zoom state
    write_versioned_function(config, "zoom/set",
f"""
# Set zoom state in gun stats
data modify storage {ns}:gun stats.is_zoom set value 1b

# Prepare input storage for model update
data modify storage {ns}:input with set value {{"item_model":""}}
data modify storage {ns}:input with.item_model set from storage {ns}:gun stats.models.zoom

# Update weapon model and stats
function {ns}:v{version}/utils/update_model with storage {ns}:input with
item modify entity @s weapon.mainhand {ns}:v{version}/update_stats

# Apply zoom effects
effect give @s slowness infinite 2 true
scoreboard players set @s {ns}.zoom 1
""")

    # Function to check and handle slowness effect
    write_versioned_function(config, "zoom/check_slowness",
f"""
# If player was zooming and switched slot so no longer holding a gun, remove slowness effect
execute unless score @s {ns}.zoom matches 1 run return fail
scoreboard players reset @s {ns}.zoom
effect clear @s slowness

# TODO optionnal: Find the weapon in inventory and turn it back to non-zoom model
""")

