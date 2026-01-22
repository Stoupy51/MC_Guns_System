
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.stats import CAPACITY, END_HEX, FIRE_MODE, REMAINING_BULLETS, START_HEX


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Main actionbar display function
    write_versioned_function("actionbar/show",
f"""
# Initialize actionbar with fire mode indicator
function {ns}:v{version}/actionbar/build_fire_mode_indicator

# Get capacity and remaining bullets
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute store result score #remaining {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}

# Add separator between fire mode and ammo
data modify storage {ns}:temp actionbar.list append value {{"text":" "}}

# Check if capacity > 15 (use numeric display) or <= 15 (use icons)
execute if score #capacity {ns}.data matches 16.. run function {ns}:v{version}/actionbar/add_numeric_ammo
execute if score #capacity {ns}.data matches ..15 run function {ns}:v{version}/actionbar/add_icon_ammo

# Display actionbar
function {ns}:v{version}/actionbar/display with storage {ns}:temp actionbar
""")

    # Build fire mode indicator: [S | B | A]
    write_versioned_function("actionbar/build_fire_mode_indicator",
f"""
# Initialize actionbar list
data modify storage {ns}:temp actionbar set value {{list:[]}}

# Add opening bracket
data modify storage {ns}:temp actionbar.list append value {{"text":"","color":"#{START_HEX}"}}
data modify storage {ns}:temp actionbar.list append value {{"text":"[ ","color":"#{END_HEX}"}}

# Check weapon capabilities
execute store result score #has_auto {ns}.data if data storage {ns}:gun all.stats.can_auto
execute store result score #has_burst {ns}.data if data storage {ns}:gun all.stats.can_burst

# Show appropriate fire mode selector based on capabilities
# Weapons with auto and burst: [S | B | A]
# Weapons with auto only: [S | A]
# Weapons with burst only: [S | B]
# Weapons with neither: [S]

# S = Semi-auto (always available)
execute if data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"S","color":"yellow","bold":true}}
execute unless data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"S"}}

# Show separator and burst only if weapon has burst capability
execute if score #has_burst {ns}.data matches 1 run data modify storage {ns}:temp actionbar.list append value {{"text":" | "}}

# B = Burst (only show if CAN_BURST)
execute if score #has_burst {ns}.data matches 1 if data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"B","color":"yellow"}}
execute if score #has_burst {ns}.data matches 1 unless data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"B"}}

# Show separator and auto only if weapon has auto capability
execute if score #has_auto {ns}.data matches 1 run data modify storage {ns}:temp actionbar.list append value {{"text":" | "}}

# A = Auto (only show if CAN_AUTO)
execute if score #has_auto {ns}.data matches 1 if data storage {ns}:gun all.stats{{{FIRE_MODE}:"auto"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"A","color":"yellow","bold":true}}
execute if score #has_auto {ns}.data matches 1 unless data storage {ns}:gun all.stats{{{FIRE_MODE}:"auto"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"A"}}

# Add closing bracket
data modify storage {ns}:temp actionbar.list append value {{"text":" ]    ","color":"#{END_HEX}"}}
""")  # noqa: E501

    # Add numeric ammo display (for capacity > 15)
    write_versioned_function("actionbar/add_numeric_ammo",
f"""
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#remaining","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value {{"text":"x "}}
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0],"color":"white"}}
data modify storage {ns}:temp actionbar.list append value {{"text":" / ","color":"#{END_HEX}"}}
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#capacity","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value {{"text":"x "}}
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0],"color":"white"}}
""")

    # Add icon ammo display (for capacity <= 15)
    write_versioned_function("actionbar/add_icon_ammo",
f"""
# Build icons recursively
scoreboard players set #i {ns}.data 0
execute if score #i {ns}.data < #capacity {ns}.data run function {ns}:v{version}/actionbar/build_icon_loop
""")

    # Build actionbar icons recursively
    write_versioned_function("actionbar/build_icon_loop",
f"""
# Append bullet icon (full by default)
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0]}}

# For empty bullets, use outline
execute if score #i {ns}.data >= #remaining {ns}.data run data modify storage {ns}:temp actionbar.list[-1] set value {{"text":"B","font":"{ns}:icons","color":"gray","shadow_color":[0,0,0,0]}}

# Increment counter
scoreboard players add #i {ns}.data 1

# Recurse if not done
execute if score #i {ns}.data < #capacity {ns}.data run function {ns}:v{version}/actionbar/build_icon_loop
""")

    # Display actionbar using macro
    write_versioned_function("actionbar/display", r"$title @s actionbar $(list)")

