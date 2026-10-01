""" Advanced weapon audio: per-weapon fire sounds plus distance-based acoustics. """

# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import COOLDOWN, RELOAD_END, RELOAD_TIME


# Classes
@dataclass(frozen=True)
class HearingLevel:
	""" One `sound/hearing/<i>_<name>` function: the crack gets 0.05 quieter every 16 blocks, down to 0.05. """
	name: str
	loudest: int
	""" Volume at point blank, in hundredths, before the x1.5 gain. """
	first_band: int
	""" Distance where the first volume step happens. """


HEARING_LEVELS: tuple[HearingLevel, ...] = (
	HearingLevel(name="distant", loudest=60, first_band=32),
	HearingLevel(name="far", loudest=60, first_band=16),
	HearingLevel(name="midrange", loudest=55, first_band=16),
	HearingLevel(name="near", loudest=50, first_band=16),
	HearingLevel(name="closest", loudest=45, first_band=16),
	HearingLevel(name="water", loudest=15, first_band=16),
)


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("player/right_click", f"""
function {ns}:v{version}/sound/main
""")

	write_versioned_function("sound/compute_acoustics", f"""
scoreboard players set #acoustics {ns}.data 0

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

# Score to acoustics level.
scoreboard players set @s {ns}.acoustics_level 0
execute if score #acoustics {ns}.data matches 121..155 run scoreboard players set @s {ns}.acoustics_level 1
execute if score #acoustics {ns}.data matches 86..120 run scoreboard players set @s {ns}.acoustics_level 2
execute if score #acoustics {ns}.data matches 51..85 run scoreboard players set @s {ns}.acoustics_level 3
execute if score #acoustics {ns}.data matches ..50 run scoreboard players set @s {ns}.acoustics_level 4
execute anchored eyes positioned ^ ^ ^ if block ~ ~ ~ #{ns}:v{version}/sounds/water run scoreboard players set @s {ns}.acoustics_level 5
""")

	write_versioned_function("sound/main", f"""
## A Pack-a-Punched gun with a pap_fire sound plays it instead.
scoreboard players set #do_pap_sound {ns}.data 0
execute if data storage {ns}:gun all.stats.pap_level if data storage {ns}:gun all.sounds.pap_fire run scoreboard players set #do_pap_sound {ns}.data 1
execute if score #do_pap_sound {ns}.data matches 1 run function {ns}:v{version}/sound/fire_pap with storage {ns}:gun all.sounds

## TODO: a mode check to choose between fire and fire_alt.
execute if score #do_pap_sound {ns}.data matches 0 if data storage {ns}:gun all.sounds.fire_alt run function {ns}:v{version}/sound/fire_alt with storage {ns}:gun all.sounds
execute if score #do_pap_sound {ns}.data matches 0 unless data storage {ns}:gun all.sounds.fire_alt run function {ns}:v{version}/sound/fire_simple with storage {ns}:gun all.sounds

# Sniper rifles.
execute if data storage {ns}:gun all.sounds.cycle run function {ns}:v{version}/sound/cycle with storage {ns}:gun all.sounds

execute if data storage {ns}:gun all.sounds.crack run function {ns}:v{version}/sound/acoustics_main with storage {ns}:gun all.sounds
""")
	write_versioned_function("sound/fire_pap", f"""
$playsound {ns}:$(pap_fire) player @s ~ ~ ~ 0.10
$playsound {ns}:$(pap_fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10
""")
	write_versioned_function("sound/fire_simple", f"""
$playsound {ns}:$(fire) player @s ~ ~ ~ 0.10
$playsound {ns}:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10
""")
	write_versioned_function("sound/fire_alt", f"""
$playsound {ns}:$(fire_alt) player @s ~ ~ ~ 0.10
$playsound {ns}:$(fire_alt) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10
""")
	write_versioned_function("sound/cycle", f"""
$playsound {ns}:$(cycle) player @s ~ ~ ~ 0.5
$playsound {ns}:$(cycle) player @a[distance=0.01..48] ~ ~ ~ 1.0 1 0.5
""")
	write_versioned_function("sound/acoustics_main", f"""
$execute if score @s {ns}.acoustics_level matches 0 run playsound {ns}:common/$(crack)_crack_0_distant player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 1 run playsound {ns}:common/$(crack)_crack_1_far player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 2 run playsound {ns}:common/$(crack)_crack_2_midrange player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 3 run playsound {ns}:common/$(crack)_crack_3_near player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 4 run playsound {ns}:common/$(crack)_crack_4_closest player @s ~ ~ ~ 1.0
$execute if score @s {ns}.acoustics_level matches 5 run playsound {ns}:common/$(crack)_crack_5_water player @s ~ ~ ~ 1.0

# Each listener faces the source, so the sound is positioned right.
scoreboard players operation #origin_acoustics_level {ns}.data = @s {ns}.acoustics_level
execute as @a[distance=0.001..224] facing entity @s eyes run function {ns}:v{version}/sound/propagation
""")

	# Turret shot: the G3A3 sound (close report and 'large' crack), as for a player. Run as the turret centre marker, at the muzzle facing the target.
	write_versioned_function("sound/turret_fire", f"""
# The turret's acoustics, as for a firing player.
function {ns}:v{version}/sound/compute_acoustics
scoreboard players operation #origin_acoustics_level {ns}.data = @s {ns}.acoustics_level

# The fire_simple mix.
playsound {ns}:g3a3/fire player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10

# Each listener's own acoustics level.
data modify storage {ns}:temp _turret_snd set value {{crack:"large"}}
execute as @a[distance=0.001..224] facing entity @s eyes run function {ns}:v{version}/sound/turret_propagation
""")

	# Like sound/propagation, reading the crack from {ns}:temp _turret_snd instead of {ns}:gun.
	write_versioned_function("sound/turret_propagation", f"""
scoreboard players operation #processed_acoustics {ns}.data = #origin_acoustics_level {ns}.data
scoreboard players operation #attenuation_acoustics {ns}.data = #origin_acoustics_level {ns}.data
scoreboard players add #attenuation_acoustics {ns}.data 1

# Same blending as the player propagation.
execute if score #origin_acoustics_level {ns}.data matches 0..4 if score #origin_acoustics_level {ns}.data > @s {ns}.acoustics_level run scoreboard players remove #processed_acoustics {ns}.data 1
execute if score #origin_acoustics_level {ns}.data < @s {ns}.acoustics_level run scoreboard players add #processed_acoustics {ns}.data 1
execute if score #attenuation_acoustics {ns}.data < @s {ns}.acoustics_level run scoreboard players add #processed_acoustics {ns}.data 1
execute if score @s {ns}.acoustics_level matches 5 run scoreboard players set #processed_acoustics {ns}.data 5

# The shared hearing/* table.
execute if score #processed_acoustics {ns}.data matches 0 run function {ns}:v{version}/sound/hearing/0_distant with storage {ns}:temp _turret_snd
execute if score #processed_acoustics {ns}.data matches 1 run function {ns}:v{version}/sound/hearing/1_far with storage {ns}:temp _turret_snd
execute if score #processed_acoustics {ns}.data matches 2 run function {ns}:v{version}/sound/hearing/2_midrange with storage {ns}:temp _turret_snd
execute if score #processed_acoustics {ns}.data matches 3 run function {ns}:v{version}/sound/hearing/3_near with storage {ns}:temp _turret_snd
execute if score #processed_acoustics {ns}.data matches 4 run function {ns}:v{version}/sound/hearing/4_closest with storage {ns}:temp _turret_snd
execute if score #processed_acoustics {ns}.data matches 5 run function {ns}:v{version}/sound/hearing/5_water with storage {ns}:temp _turret_snd
""")

	write_versioned_function("sound/check/pump", f"""
scoreboard players set #divisor {ns}.data 2
execute store result score #half {ns}.data run data get storage {ns}:gun all.stats.{COOLDOWN}
scoreboard players operation #half {ns}.data /= #divisor {ns}.data

# Half the cooldown: the mid sound plays.
execute if score @s {ns}.cooldown = #half {ns}.data run function {ns}:v{version}/sound/pump with storage {ns}:gun all.sounds
""")

	write_versioned_function("sound/check/reload_mid", f"""
scoreboard players set #divisor {ns}.data 2
execute store result score #half {ns}.data run data get storage {ns}:gun all.stats.{RELOAD_TIME}
scoreboard players operation #half {ns}.data /= #divisor {ns}.data

# Half the cooldown: the mid sound plays.
execute if score @s {ns}.cooldown = #half {ns}.data run function {ns}:v{version}/sound/player_mid with storage {ns}:gun all.sounds
""")

	write_versioned_function("sound/check/reload_end", f"""
execute store result score #{RELOAD_END} {ns}.data run data get storage {ns}:gun all.stats.{RELOAD_END}
execute if score @s {ns}.cooldown = #{RELOAD_END} {ns}.data run function {ns}:v{version}/sound/player_end with storage {ns}:gun all.sounds
""")

	write_versioned_function("sound/propagation", f"""
scoreboard players operation #processed_acoustics {ns}.data = #origin_acoustics_level {ns}.data
scoreboard players operation #attenuation_acoustics {ns}.data = #origin_acoustics_level {ns}.data
scoreboard players add #attenuation_acoustics {ns}.data 1

# One level closer when the source (0-4) is above the listener's level: enclosed spaces make distant sounds seem near.
execute if score #origin_acoustics_level {ns}.data matches 0..4 if score #origin_acoustics_level {ns}.data > @s {ns}.acoustics_level run scoreboard players remove #processed_acoustics {ns}.data 1

# One level louder when the source is below: a more reflective spot sounds louder.
execute if score #origin_acoustics_level {ns}.data < @s {ns}.acoustics_level run scoreboard players add #processed_acoustics {ns}.data 1

# Again when source + 1 is still below, which smooths the transition between environments.
execute if score #attenuation_acoustics {ns}.data < @s {ns}.acoustics_level run scoreboard players add #processed_acoustics {ns}.data 1

# A listener in water (5) always hears the water level.
execute if score @s {ns}.acoustics_level matches 5 run scoreboard players set #processed_acoustics {ns}.data 5

execute if score #processed_acoustics {ns}.data matches 0 run function {ns}:v{version}/sound/hearing/0_distant with storage {ns}:gun all.sounds
execute if score #processed_acoustics {ns}.data matches 1 run function {ns}:v{version}/sound/hearing/1_far with storage {ns}:gun all.sounds
execute if score #processed_acoustics {ns}.data matches 2 run function {ns}:v{version}/sound/hearing/2_midrange with storage {ns}:gun all.sounds
execute if score #processed_acoustics {ns}.data matches 3 run function {ns}:v{version}/sound/hearing/3_near with storage {ns}:gun all.sounds
execute if score #processed_acoustics {ns}.data matches 4 run function {ns}:v{version}/sound/hearing/4_closest with storage {ns}:gun all.sounds
execute if score #processed_acoustics {ns}.data matches 5 run function {ns}:v{version}/sound/hearing/5_water with storage {ns}:gun all.sounds
""")
	for i, level in enumerate(HEARING_LEVELS):
		for band in range(level.loudest // 5):
			low: int = 0 if band == 0 else level.first_band + 16 * (band - 1)
			volume: float = (level.loudest - 5 * band) / 100
			write_versioned_function(
				f"sound/hearing/{i}_{level.name}",
				f"$execute if entity @s[distance={low}..{level.first_band + 16 * band}] positioned as @s run playsound {ns}:common/$(crack)_crack_{i}_{level.name} player @s ^ ^ ^-6 {round(volume * 1.5, 3)}"
			)

	write_versioned_function("sound/reload_start", f"""
$playsound {ns}:$(reload) player @s
""")
	write_versioned_function("sound/player_begin", f"""
$playsound {ns}:$(playerbegin) player @a[distance=0.01..16] ~ ~ ~ 0.3
""")
	write_versioned_function("sound/player_mid", f"""
$playsound {ns}:$(playermid) player @a[distance=0.01..16] ~ ~ ~ 0.3
""")
	write_versioned_function("sound/player_end", f"""
$playsound {ns}:$(playerend) player @a[distance=0.01..16] ~ ~ ~ 0.3
""")
	write_versioned_function("sound/pump", f"""
$playsound {ns}:$(pump) player @s
$playsound {ns}:$(pump) player @a[distance=0.01..16] ~ ~ ~ 0.3
""")

