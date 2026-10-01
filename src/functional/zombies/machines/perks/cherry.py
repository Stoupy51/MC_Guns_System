""" Electric Cherry: a reload discharges a shock scaled by how empty the magazine was. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import CAPACITY, REMAINING_BULLETS


# Functions
def write_electric_cherry() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# on_reload handler, run as the reloading player.
	write_versioned_function("zombies/perks/electric_cherry_on_reload", f"""
execute unless score @s {ns}.zb.in_game matches 1.. run return fail
execute unless score @s {ns}.special.electric_cherry matches 1 run return fail

# Bullets discharged = capacity - remaining.
execute store result score #ec_cap {ns}.data run data get storage {ns}:signals on_reload.weapon.stats.{CAPACITY}
execute store result score #ec_rem {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}
execute if score #ec_rem {ns}.data matches ..-1 run scoreboard players set #ec_rem {ns}.data 0
scoreboard players operation #ec_used {ns}.data = #ec_cap {ns}.data
scoreboard players operation #ec_used {ns}.data -= #ec_rem {ns}.data
execute if score #ec_used {ns}.data matches ..0 run return fail

# Allowed 10 s after the last discharge, or 5 s on a dry reload.
execute store result score #ec_now {ns}.data run time query gametime
scoreboard players operation #ec_since {ns}.data = #ec_now {ns}.data
scoreboard players operation #ec_since {ns}.data -= @s {ns}.zb.ec_last
scoreboard players set #ec_ok {ns}.data 0
execute if score #ec_since {ns}.data matches 200.. run scoreboard players set #ec_ok {ns}.data 1
execute if score #ec_since {ns}.data matches 100.. if score #ec_rem {ns}.data matches 0 run scoreboard players set #ec_ok {ns}.data 1
execute if score #ec_ok {ns}.data matches 0 run return fail

scoreboard players operation @s {ns}.zb.ec_last = #ec_now {ns}.data
execute at @s run function {ns}:v{version}/zombies/perks/electric_cherry_shock
""", tags=[f"{ns}:signals/on_reload"])

	# Run as the owner; #ec_used and #ec_cap come from the caller (on_down passes a full magazine).
	write_versioned_function("zombies/perks/electric_cherry_shock", f"""
particle minecraft:electric_spark ~ ~1 ~ 2 1 2 0.25 80 force @a[distance=..48]
particle minecraft:flash{{color:[1.0,1.0,1.0,1.0]}} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..48]
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..32] ~ ~ ~ 0.6 1.6
playsound minecraft:block.beacon.deactivate player @a[distance=..24] ~ ~ ~ 0.6 2

# Radius (blocks x1000) 2500 + 3500 x used / cap: 2.5 to 6.0 blocks.
scoreboard players operation #ec_r {ns}.data = #ec_used {ns}.data
scoreboard players operation #ec_r {ns}.data *= #3500 {ns}.data
scoreboard players operation #ec_r {ns}.data /= #ec_cap {ns}.data
scoreboard players add #ec_r {ns}.data 2500
execute store result storage {ns}:temp _ec.radius float 0.001 run scoreboard players get #ec_r {ns}.data

# Damage (max health x 0.01) 40 + 60 x used / cap: 40% to 100%.
scoreboard players operation #ec_frac {ns}.data = #ec_used {ns}.data
scoreboard players operation #ec_frac {ns}.data *= #60 {ns}.data
scoreboard players operation #ec_frac {ns}.data /= #ec_cap {ns}.data
scoreboard players add #ec_frac {ns}.data 40
execute store result storage {ns}:temp _ec.scale double 0.01 run scoreboard players get #ec_frac {ns}.data

function {ns}:v{version}/zombies/perks/electric_cherry_damage with storage {ns}:temp _ec
""")

	## Run as the owner.
	write_versioned_function("zombies/perks/electric_cherry_damage", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run function {ns}:v{version}/zombies/perks/electric_cherry_hit {{scale:"$(scale)"}}
""")

	## Run as a zombie: max health fraction from the macro, brief stun.
	write_versioned_function("zombies/perks/electric_cherry_hit", f"""
$execute store result storage {ns}:temp _ec_dmg.amount int 1 run attribute @s minecraft:max_health get $(scale)
data modify storage {ns}:temp _ec_dmg.type set value "minecraft:lightning_bolt"
particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.1 12
effect give @s minecraft:slowness 60 3 true
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _ec_dmg
""")

