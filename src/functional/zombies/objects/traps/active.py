""" An active trap: damaging zombies, its cooldown and the Timeslip discount. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_trap_activity() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Active trap tick: damage zombies, particles, decrement timer
	write_versioned_function("zombies/traps/active_tick", f"""
# @s = trap center marker, at @s position

# Apply damage based on trap type
data modify storage {ns}:temp _trap_tick set value {{rx:0,ry:0,rz:0,sx:0,sy:0,sz:0}}
execute store result storage {ns}:temp _trap_tick.rx int 1 run scoreboard players get @s {ns}.zb.trap.rx
execute store result storage {ns}:temp _trap_tick.ry int 1 run scoreboard players get @s {ns}.zb.trap.ry
execute store result storage {ns}:temp _trap_tick.rz int 1 run scoreboard players get @s {ns}.zb.trap.rz

scoreboard players operation #trap_sx {ns}.data = @s {ns}.zb.trap.rx
scoreboard players operation #trap_sy {ns}.data = @s {ns}.zb.trap.ry
scoreboard players operation #trap_sz {ns}.data = @s {ns}.zb.trap.rz
scoreboard players operation #trap_sx {ns}.data += #trap_sx {ns}.data
scoreboard players operation #trap_sy {ns}.data += #trap_sy {ns}.data
scoreboard players operation #trap_sz {ns}.data += #trap_sz {ns}.data
execute store result storage {ns}:temp _trap_tick.sx int 1 run scoreboard players get #trap_sx {ns}.data
execute store result storage {ns}:temp _trap_tick.sy int 1 run scoreboard players get #trap_sy {ns}.data
execute store result storage {ns}:temp _trap_tick.sz int 1 run scoreboard players get #trap_sz {ns}.data

execute if score @s {ns}.zb.trap.type matches 0 run function {ns}:v{version}/zombies/traps/damage_fire with storage {ns}:temp _trap_tick
execute if score @s {ns}.zb.trap.type matches 1 run function {ns}:v{version}/zombies/traps/damage_electric with storage {ns}:temp _trap_tick

# Turret: fire a shot every 5 ticks at the nearest zombie in range
scoreboard players operation #turret_mod {ns}.data = @s {ns}.zb.trap.timer
scoreboard players operation #turret_mod {ns}.data %= #5 {ns}.data
execute if score #turret_mod {ns}.data matches 0 if score @s {ns}.zb.trap.type matches 2 run function {ns}:v{version}/zombies/traps/turret_fire with storage {ns}:temp _trap_tick

# Particles based on type
execute if score @s {ns}.zb.trap.type matches 0 run particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.05 10
execute if score @s {ns}.zb.trap.type matches 1 run particle minecraft:electric_spark ~ ~1 ~ 1.5 0.5 1.5 0.1 15
execute if score @s {ns}.zb.trap.type matches 2 run particle minecraft:smoke ~ ~1 ~ 0.2 0.2 0.2 0.01 2

# Decrement timer (real-time via #tick_delta, clamped at 0 so the exact-0 checks below still hit)
scoreboard players operation @s {ns}.zb.trap.timer -= #tick_delta {ns}.data
execute unless score @s {ns}.zb.trap.timer matches 0.. run scoreboard players set @s {ns}.zb.trap.timer 0

# Check if deactivated: start the cooldown as a countdown. NOT an absolute #real_tick deadline —
# that clock is a stopwatch recreated on every datapack load, so a stored deadline outlived its
# clock and left the trap permanently unusable after any /reload.
execute if score @s {ns}.zb.trap.timer matches 0 run scoreboard players operation @s {ns}.zb.trap.cd = @s {ns}.zb.trap.cd_max

# Timeslip: the activator's trap cooldown is scaled to 75%
execute if score @s {ns}.zb.trap.timer matches 0 if score @s {ns}.zb.trap.timeslip matches 1 run function {ns}:v{version}/zombies/traps/apply_timeslip_cd
""")

	## Scale the just-set cooldown to 75% (Timeslip). @s = trap center marker.
	write_versioned_function("zombies/traps/apply_timeslip_cd", f"""
scoreboard players set #ts_num {ns}.data 3
scoreboard players set #ts_den {ns}.data 4
scoreboard players operation @s {ns}.zb.trap.cd *= #ts_num {ns}.data
scoreboard players operation @s {ns}.zb.trap.cd /= #ts_den {ns}.data
""")

	## Count a trap's cooldown down. @s = trap center marker.
	write_versioned_function("zombies/traps/cooldown_tick", f"""
# A countdown can never exceed its own maximum, so anything larger is a stale absolute deadline
# left by the old #real_tick scheme — clear it rather than make players wait out a dead timestamp.
execute if score @s {ns}.zb.trap.cd > @s {ns}.zb.trap.cd_max run scoreboard players set @s {ns}.zb.trap.cd 0

scoreboard players operation @s {ns}.zb.trap.cd -= #tick_delta {ns}.data
""")

	write_versioned_function("zombies/traps/damage_fire", f"""
# Zombies: lethal damage (1000% of each zombie's max health)
data modify storage {ns}:temp _trap_dmg.type set value "minecraft:on_fire"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function {ns}:v{version}/zombies/traps/kill_zombie

# Players inside the trap: 5 fire damage (PhD Flopper owners are immune)
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={{{ns}.zb.in_game=1,{ns}.special.phd_flopper=0}},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:on_fire
""")

	write_versioned_function("zombies/traps/damage_electric", f"""
# Zombies: lethal damage (1000% of each zombie's max health)
data modify storage {ns}:temp _trap_dmg.type set value "minecraft:lightning_bolt"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function {ns}:v{version}/zombies/traps/kill_zombie

# Players inside the trap: 5 electric damage (PhD Flopper owners are immune)
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={{{ns}.zb.in_game=1,{ns}.special.phd_flopper=0}},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:lightning_bolt
""")

	## Per-zombie lethal damage: 1000% of this zombie's max health (damage type set by caller in _trap_dmg.type)
	write_versioned_function("zombies/traps/kill_zombie", f"""
execute store result storage {ns}:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 10
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _trap_dmg
""")

	write_versioned_function("zombies/traps/apply_trap_damage", """
$damage @s $(amount) $(type)
""")

