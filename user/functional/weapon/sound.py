
# ruff: noqa: E501
# Imports
from python_datapack.utils.database_helper import write_versioned_function

from user.config.stats import BASE_WEAPON, CRACK_TYPE, RELOAD_END


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

    # Compute acoustics function
    write_versioned_function(config, "sound/compute_acoustics",
f"""
# Initialize acoustics score
scoreboard players set #acoustics {ns}.data 0

# Compute it
execute if block ~ ~1 ~ #{ns}:v{version}/outside if block ~ ~2 ~ #{ns}:v{version}/outside if block ~ ~3 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 8
execute if block ~ ~4 ~ #{ns}:v{version}/outside if block ~ ~5 ~ #{ns}:v{version}/outside if block ~ ~6 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 8
execute if block ~1 ~1 ~ #{ns}:v{version}/outside if block ~2 ~1 ~ #{ns}:v{version}/outside if block ~3 ~1 ~ #{ns}:v{version}/outside if block ~1 ~2 ~ #{ns}:v{version}/outside if block ~2 ~2 ~ #{ns}:v{version}/outside if block ~3 ~2 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-1 ~1 ~ #{ns}:v{version}/outside if block ~-2 ~1 ~ #{ns}:v{version}/outside if block ~-3 ~1 ~ #{ns}:v{version}/outside if block ~-1 ~2 ~ #{ns}:v{version}/outside if block ~-2 ~2 ~ #{ns}:v{version}/outside if block ~-3 ~2 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~ ~1 ~1 #{ns}:v{version}/outside if block ~ ~1 ~2 #{ns}:v{version}/outside if block ~ ~1 ~3 #{ns}:v{version}/outside if block ~ ~2 ~1 #{ns}:v{version}/outside if block ~ ~2 ~2 #{ns}:v{version}/outside if block ~ ~2 ~3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~ ~1 ~-1 #{ns}:v{version}/outside if block ~ ~1 ~-2 #{ns}:v{version}/outside if block ~ ~1 ~-3 #{ns}:v{version}/outside if block ~ ~2 ~-1 #{ns}:v{version}/outside if block ~ ~2 ~-2 #{ns}:v{version}/outside if block ~ ~2 ~-3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~1 ~1 #{ns}:v{version}/outside if block ~2 ~1 ~2 #{ns}:v{version}/outside if block ~3 ~1 ~3 #{ns}:v{version}/outside if block ~1 ~2 ~1 #{ns}:v{version}/outside if block ~2 ~2 ~2 #{ns}:v{version}/outside if block ~3 ~2 ~3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-1 ~1 ~1 #{ns}:v{version}/outside if block ~-2 ~1 ~2 #{ns}:v{version}/outside if block ~-3 ~1 ~3 #{ns}:v{version}/outside if block ~-1 ~2 ~1 #{ns}:v{version}/outside if block ~-2 ~2 ~2 #{ns}:v{version}/outside if block ~-3 ~2 ~3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~1 ~-1 #{ns}:v{version}/outside if block ~2 ~1 ~-2 #{ns}:v{version}/outside if block ~3 ~1 ~-3 #{ns}:v{version}/outside if block ~1 ~2 ~-1 #{ns}:v{version}/outside if block ~2 ~2 ~-2 #{ns}:v{version}/outside if block ~3 ~2 ~-3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-1 ~1 ~-1 #{ns}:v{version}/outside if block ~-2 ~1 ~-2 #{ns}:v{version}/outside if block ~-3 ~1 ~-3 #{ns}:v{version}/outside if block ~-1 ~2 ~-1 #{ns}:v{version}/outside if block ~-2 ~2 ~-2 #{ns}:v{version}/outside if block ~-3 ~2 ~-3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~3 ~ #{ns}:v{version}/outside if block ~2 ~3 ~ #{ns}:v{version}/outside if block ~3 ~3 ~ #{ns}:v{version}/outside if block ~1 ~4 ~ #{ns}:v{version}/outside if block ~2 ~4 ~ #{ns}:v{version}/outside if block ~3 ~4 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-1 ~3 ~ #{ns}:v{version}/outside if block ~-2 ~3 ~ #{ns}:v{version}/outside if block ~-3 ~3 ~ #{ns}:v{version}/outside if block ~-1 ~4 ~ #{ns}:v{version}/outside if block ~-2 ~4 ~ #{ns}:v{version}/outside if block ~-3 ~4 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~ ~3 ~1 #{ns}:v{version}/outside if block ~ ~3 ~2 #{ns}:v{version}/outside if block ~ ~3 ~3 #{ns}:v{version}/outside if block ~ ~4 ~1 #{ns}:v{version}/outside if block ~ ~4 ~2 #{ns}:v{version}/outside if block ~ ~4 ~3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~ ~3 ~-1 #{ns}:v{version}/outside if block ~ ~3 ~-2 #{ns}:v{version}/outside if block ~ ~3 ~-3 #{ns}:v{version}/outside if block ~ ~4 ~-1 #{ns}:v{version}/outside if block ~ ~4 ~-2 #{ns}:v{version}/outside if block ~ ~4 ~-3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~3 ~1 #{ns}:v{version}/outside if block ~2 ~3 ~2 #{ns}:v{version}/outside if block ~3 ~3 ~3 #{ns}:v{version}/outside if block ~1 ~4 ~1 #{ns}:v{version}/outside if block ~2 ~4 ~2 #{ns}:v{version}/outside if block ~3 ~4 ~3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-1 ~3 ~1 #{ns}:v{version}/outside if block ~-2 ~3 ~2 #{ns}:v{version}/outside if block ~-3 ~3 ~3 #{ns}:v{version}/outside if block ~-1 ~4 ~1 #{ns}:v{version}/outside if block ~-2 ~4 ~2 #{ns}:v{version}/outside if block ~-3 ~4 ~3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~3 ~-1 #{ns}:v{version}/outside if block ~2 ~3 ~-2 #{ns}:v{version}/outside if block ~3 ~3 ~-3 #{ns}:v{version}/outside if block ~1 ~4 ~-1 #{ns}:v{version}/outside if block ~2 ~4 ~-2 #{ns}:v{version}/outside if block ~3 ~4 ~-3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-1 ~3 ~-1 #{ns}:v{version}/outside if block ~-2 ~3 ~-2 #{ns}:v{version}/outside if block ~-3 ~3 ~-3 #{ns}:v{version}/outside if block ~-1 ~4 ~-1 #{ns}:v{version}/outside if block ~-2 ~4 ~-2 #{ns}:v{version}/outside if block ~-3 ~4 ~-3 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~5 ~ #{ns}:v{version}/outside if block ~2 ~5 ~ #{ns}:v{version}/outside if block ~1 ~6 ~ #{ns}:v{version}/outside if block ~2 ~6 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~-1 ~5 ~ #{ns}:v{version}/outside if block ~-2 ~5 ~ #{ns}:v{version}/outside if block ~-1 ~6 ~ #{ns}:v{version}/outside if block ~-2 ~6 ~ #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~ ~5 ~1 #{ns}:v{version}/outside if block ~ ~5 ~2 #{ns}:v{version}/outside if block ~ ~6 ~1 #{ns}:v{version}/outside if block ~ ~6 ~2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~ ~5 ~-1 #{ns}:v{version}/outside if block ~ ~5 ~-2 #{ns}:v{version}/outside if block ~ ~6 ~-1 #{ns}:v{version}/outside if block ~ ~6 ~-2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~1 ~5 ~1 #{ns}:v{version}/outside if block ~2 ~5 ~2 #{ns}:v{version}/outside if block ~1 ~6 ~1 #{ns}:v{version}/outside if block ~2 ~6 ~2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~-1 ~5 ~1 #{ns}:v{version}/outside if block ~-2 ~5 ~2 #{ns}:v{version}/outside if block ~-1 ~6 ~1 #{ns}:v{version}/outside if block ~-2 ~6 ~2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~1 ~5 ~-1 #{ns}:v{version}/outside if block ~2 ~5 ~-2 #{ns}:v{version}/outside if block ~1 ~6 ~-1 #{ns}:v{version}/outside if block ~2 ~6 ~-2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~-1 ~5 ~-1 #{ns}:v{version}/outside if block ~-2 ~5 ~-2 #{ns}:v{version}/outside if block ~-1 ~6 ~-1 #{ns}:v{version}/outside if block ~-2 ~6 ~-2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~2 ~1 ~1 #{ns}:v{version}/outside if block ~2 ~2 ~1 #{ns}:v{version}/outside if block ~2 ~1 ~-1 #{ns}:v{version}/outside if block ~2 ~2 ~-1 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~-2 ~1 ~1 #{ns}:v{version}/outside if block ~-2 ~2 ~1 #{ns}:v{version}/outside if block ~-2 ~1 ~-1 #{ns}:v{version}/outside if block ~-2 ~2 ~-1 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~1 ~2 #{ns}:v{version}/outside if block ~1 ~2 ~2 #{ns}:v{version}/outside if block ~-1 ~1 ~2 #{ns}:v{version}/outside if block ~-1 ~2 ~2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~1 ~1 ~-2 #{ns}:v{version}/outside if block ~1 ~2 ~-2 #{ns}:v{version}/outside if block ~-1 ~1 ~-2 #{ns}:v{version}/outside if block ~-1 ~2 ~-2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 4
execute if block ~2 ~3 ~1 #{ns}:v{version}/outside if block ~2 ~4 ~1 #{ns}:v{version}/outside if block ~2 ~3 ~-1 #{ns}:v{version}/outside if block ~2 ~4 ~-1 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~-2 ~3 ~1 #{ns}:v{version}/outside if block ~-2 ~4 ~1 #{ns}:v{version}/outside if block ~-2 ~3 ~-1 #{ns}:v{version}/outside if block ~-2 ~4 ~-1 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~1 ~3 ~2 #{ns}:v{version}/outside if block ~1 ~4 ~2 #{ns}:v{version}/outside if block ~-1 ~3 ~2 #{ns}:v{version}/outside if block ~-1 ~4 ~2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~1 ~3 ~-2 #{ns}:v{version}/outside if block ~1 ~4 ~-2 #{ns}:v{version}/outside if block ~-1 ~3 ~-2 #{ns}:v{version}/outside if block ~-1 ~4 ~-2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 6
execute if block ~2 ~5 ~1 #{ns}:v{version}/outside if block ~2 ~6 ~1 #{ns}:v{version}/outside if block ~2 ~5 ~-1 #{ns}:v{version}/outside if block ~2 ~6 ~-1 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 8
execute if block ~-2 ~5 ~1 #{ns}:v{version}/outside if block ~-2 ~6 ~1 #{ns}:v{version}/outside if block ~-2 ~5 ~-1 #{ns}:v{version}/outside if block ~-2 ~6 ~-1 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 8
execute if block ~1 ~5 ~2 #{ns}:v{version}/outside if block ~1 ~6 ~2 #{ns}:v{version}/outside if block ~-1 ~5 ~2 #{ns}:v{version}/outside if block ~-1 ~6 ~2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 8
execute if block ~1 ~5 ~-2 #{ns}:v{version}/outside if block ~1 ~6 ~-2 #{ns}:v{version}/outside if block ~-1 ~5 ~-2 #{ns}:v{version}/outside if block ~-1 ~6 ~-2 #{ns}:v{version}/outside run scoreboard players add #acoustics {ns}.data 8

# Turn score into acoustics level
scoreboard players set @s {ns}.acoustics_level 0
execute if score #acoustics {ns}.data matches 121..155 run scoreboard players set @s {ns}.acoustics_level 1
execute if score #acoustics {ns}.data matches 86..120 run scoreboard players set @s {ns}.acoustics_level 2
execute if score #acoustics {ns}.data matches 51..85 run scoreboard players set @s {ns}.acoustics_level 3
execute if score #acoustics {ns}.data matches ..50 run scoreboard players set @s {ns}.acoustics_level 4
execute anchored eyes positioned ^ ^ ^ if block ~ ~ ~ #{ns}:v{version}/sounds/water run scoreboard players set @s {ns}.acoustics_level 5
""")

    # Main function
    write_versioned_function(config, "sound/main",
f"""
# Simple weapon fire sound
$playsound {ns}:$({BASE_WEAPON})/fire player @s ~ ~ ~ 0.25
$playsound {ns}:$({BASE_WEAPON})/fire player @a[distance=0.01..48] 0.75 1 0.25

# Playsound depending on acoustics level
$execute if score @s {ns}.acoustics_level matches 0 run playsound {ns}:common/$({CRACK_TYPE})_crack_0_distant player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 1 run playsound {ns}:common/$({CRACK_TYPE})_crack_1_far player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 2 run playsound {ns}:common/$({CRACK_TYPE})_crack_2_midrange player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 3 run playsound {ns}:common/$({CRACK_TYPE})_crack_3_near player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 4 run playsound {ns}:common/$({CRACK_TYPE})_crack_4_closest player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 5 run playsound {ns}:common/$({CRACK_TYPE})_crack_5_water player @s ~ ~ ~ 1.0

# Directs sound propagation to nearby players by aligning their view with the sound source for accurate positional audio
scoreboard players operation #origin_acoustics_level {ns}.data = @s {ns}.acoustics_level
execute as @a[distance=0.001..224] facing entity @s eyes run function {ns}:v{version}/sound/propagation
""")

    write_versioned_function(config, "sound/propagation",
f"""
# Make copies of the original acoustics level to work on
scoreboard players operation #processed_acoustics {ns}.data = #origin_acoustics_level {ns}.data
scoreboard players operation #attenuation_acoustics {ns}.data = #origin_acoustics_level {ns}.data
scoreboard players add #attenuation_acoustics {ns}.data 1

# Reduce the sound level by 1 when the original sound level (0-4) is greater than the listener's acoustics level
# When in an enclosed space, distant sounds are perceived as closer due to acoustic properties
execute if score #origin_acoustics_level {ns}.data matches 0..4 if score #origin_acoustics_level {ns}.data > @s {ns}.acoustics_level run scoreboard players remove #processed_acoustics {ns}.data 1

# Increase the sound level by 1 when the original sound level is less than the listener's acoustics level
# This makes sounds appear louder when the listener is in a more acoustically reflective environment
execute if score #origin_acoustics_level {ns}.data < @s {ns}.acoustics_level run scoreboard players add #processed_acoustics {ns}.data 1

# If (original sound level + 1) is less than listener's acoustics level, increase the sound level by 1
# This creates a smoother sound transition between different acoustic environments
execute if score #attenuation_acoustics {ns}.data < @s {ns}.acoustics_level run scoreboard players add #processed_acoustics {ns}.data 1

# If listener's acoustics level is 5 (water), force the sound level to water regardless of other conditions
execute if score @s {ns}.acoustics_level matches 5 run scoreboard players set #processed_acoustics {ns}.data 5

# Play the appropriate sound effect based on the calculated sound level
execute if score #processed_acoustics {ns}.data matches 0 run function {ns}:v{version}/sound/hearing/0_distant with storage {ns}:gun all.stats
execute if score #processed_acoustics {ns}.data matches 1 run function {ns}:v{version}/sound/hearing/1_far with storage {ns}:gun all.stats
execute if score #processed_acoustics {ns}.data matches 2 run function {ns}:v{version}/sound/hearing/2_midrange with storage {ns}:gun all.stats
execute if score #processed_acoustics {ns}.data matches 3 run function {ns}:v{version}/sound/hearing/3_near with storage {ns}:gun all.stats
execute if score #processed_acoustics {ns}.data matches 4 run function {ns}:v{version}/sound/hearing/4_closest with storage {ns}:gun all.stats
execute if score #processed_acoustics {ns}.data matches 5 run function {ns}:v{version}/sound/hearing/5_water with storage {ns}:gun all.stats
""")
    sound_levels: list[tuple[str, list[tuple[int, int, float]]]] = [
        ("distant",  [(0, 32, 0.6), (32, 48, 0.55), (48, 64, 0.5), (64, 80, 0.45), (80, 96, 0.4), (96, 112, 0.35), (112, 128, 0.3), (128, 144, 0.25), (144, 160, 0.2), (160, 176, 0.15), (176, 192, 0.1), (192, 208, 0.05)]),
        ("far",      [(0, 16, 0.6), (16, 32, 0.55), (32, 48, 0.5), (48, 64, 0.45), (64, 80, 0.4), (80, 96, 0.35), (96, 112, 0.3), (112, 128, 0.25), (128, 144, 0.2), (144, 160, 0.15), (160, 176, 0.1), (176, 192, 0.05)]),
        ("midrange", [(0, 16, 0.55), (16, 32, 0.5), (32, 48, 0.45), (48, 64, 0.4), (64, 80, 0.35), (80, 96, 0.3), (96, 112, 0.25), (112, 128, 0.2), (128, 144, 0.15), (144, 160, 0.1), (160, 176, 0.05)]),
        ("near",     [(0, 16, 0.5), (16, 32, 0.45), (32, 48, 0.4), (48, 64, 0.35), (64, 80, 0.3), (80, 96, 0.25), (96, 112, 0.2), (112, 128, 0.15), (128, 144, 0.1), (144, 160, 0.05)]),
        ("closest",  [(0, 16, 0.45), (16, 32, 0.4), (32, 48, 0.35), (48, 64, 0.3), (64, 80, 0.25), (80, 96, 0.2), (96, 112, 0.15), (112, 128, 0.1), (128, 144, 0.05)]),
        ("water",    [(0, 16, 0.15), (16, 32, 0.1), (32, 48, 0.05)])
    ]
    for i, (level, pairs) in enumerate(sound_levels):
        for mini, maxi, volume in pairs:
            write_versioned_function(
                config, f"sound/hearing/{i}_{level}",
                f"$execute if entity @s[distance={mini}..{maxi}] positioned as @s run playsound {ns}:common/$({CRACK_TYPE})_crack_{i}_{level} player @s ^ ^ ^-6 {round(volume * 1.5, 3)}\n"
            )

    # Main function
    write_versioned_function(config, "sound/main",
f"""
# Simple weapon fire sound
$playsound {ns}:$({BASE_WEAPON})/fire player @s ~ ~ ~ 0.25
$playsound {ns}:$({BASE_WEAPON})/fire player @a[distance=0.01..48] 0.75 1 0.25

# Playsound depending on acoustics level
execute if score @s {ns}.acoustics_level matches 0 run return run function {ns}:v{version}/acoustics_0 {{}}
execute if score @s {ns}.acoustics_level matches 1 run return run function {ns}:v{version}/acoustics_1
execute if score @s {ns}.acoustics_level matches 2 run return run function {ns}:v{version}/acoustics_2
execute if score @s {ns}.acoustics_level matches 3 run return run function {ns}:v{version}/acoustics_3
execute if score @s {ns}.acoustics_level matches 4 run return run function {ns}:v{version}/acoustics_4
execute if score @s {ns}.acoustics_level matches 5 run return run function {ns}:v{version}/acoustics_water
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
# If cooldown is reload end, and player was reloading, playsound
execute store result score #{RELOAD_END} {ns}.data run data get storage {ns}:gun all.stats.{RELOAD_END}
execute if score @s {ns}.cooldown = #{RELOAD_END} {ns}.data run function {ns}:v{version}/sound/reload_end with storage {ns}:gun all.stats
""")
    write_versioned_function(config, "sound/reload_end",
f"""
# Play the end reload sound for all nearby players
$playsound {ns}:$({BASE_WEAPON})/playerend player @a[distance=0.01..16] ~ ~ ~ 0.3
""")

