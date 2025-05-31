
# Imports
from python_datapack.utils.database_helper import write_versioned_function

from user.config.stats import BASE_WEAPON, RELOAD_END


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # TODO: Remove BASE_WEAPON and make all.sounds a dict containing all the sounds paths so it's customizable

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Advanced Playsound
function {ns}:v{version}/sound/main with storage {ns}:gun all.stats
""")

    # Main function
    write_versioned_function(config, "sound/main",
f"""
# TODO: Advanced playsound using cracks and stuff
$playsound {ns}:$({BASE_WEAPON})/fire player @s ~ ~ ~ 0.25
$playsound {ns}:$({BASE_WEAPON})/fire player @a[distance=0.01..48] 0.75 1 0.25
""")

    # Reload start function
    write_versioned_function(config, "sound/reload_start",
f"""
# Full reload sound for the player
$playsound {ns}:$({BASE_WEAPON})/reload player

# Play the begin reload sound for all nearby players
$playsound {ns}:$({BASE_WEAPON})/playerbegin player @a[distance=0.01..16] ~ ~ ~ 0.3
""")

    # Reload end functions
    write_versioned_function(config, "sound/check_reload_end",
f"""
# TODO:IF COOLDOWN = RELOAD_END, RUN:
execute store result score #{RELOAD_END} {ns}.data run data get storage {ns}:gun all.stats.{RELOAD_END}
execute if score @s {ns}.cooldown = #{RELOAD_END} {ns}.data run function {ns}:v{version}/sound/reload_end with storage {ns}:gun all.stats
""")
    write_versioned_function(config, "sound/reload_end",
f"""
# Play the end reload sound for all nearby players
$playsound {ns}:$({BASE_WEAPON})/playerend player @a[distance=0.01..16] ~ ~ ~ 0.3

# Update weapon lore
function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

# Remove reloading tag
tag @s remove {ns}.reloading
""")

