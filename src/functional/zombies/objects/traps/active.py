""" An active trap: damaging zombies, its cooldown and the Timeslip discount. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_trap_activity() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Damage zombies, particles, timer.
	write_versioned_function("zombies/traps/active_tick", f"""
# Run as the trap centre marker, at it.

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

# Turret: a shot every 5 ticks.
scoreboard players operation #turret_mod {ns}.data = @s {ns}.zb.trap.timer
scoreboard players operation #turret_mod {ns}.data %= #5 {ns}.data
execute if score #turret_mod {ns}.data matches 0 if score @s {ns}.zb.trap.type matches 2 run function {ns}:v{version}/zombies/traps/turret_fire with storage {ns}:temp _trap_tick

execute if score @s {ns}.zb.trap.type matches 0 run particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.05 10
execute if score @s {ns}.zb.trap.type matches 1 run particle minecraft:electric_spark ~ ~1 ~ 1.5 0.5 1.5 0.1 15
execute if score @s {ns}.zb.trap.type matches 2 run particle minecraft:smoke ~ ~1 ~ 0.2 0.2 0.2 0.01 2

# Clamped at 0 so the exact-0 checks below still hit.
scoreboard players operation @s {ns}.zb.trap.timer -= #tick_delta {ns}.data
execute unless score @s {ns}.zb.trap.timer matches 0.. run scoreboard players set @s {ns}.zb.trap.timer 0

# The cooldown is a countdown, not a #real_tick deadline: that stopwatch is recreated on every load.
execute if score @s {ns}.zb.trap.timer matches 0 run scoreboard players operation @s {ns}.zb.trap.cd = @s {ns}.zb.trap.cd_max

# Timeslip: the activator's cooldown at 75%.
execute if score @s {ns}.zb.trap.timer matches 0 if score @s {ns}.zb.trap.timeslip matches 1 run function {ns}:v{version}/zombies/traps/apply_timeslip_cd
""")

	## Run as the trap centre marker.
	write_versioned_function("zombies/traps/apply_timeslip_cd", f"""
scoreboard players set #ts_num {ns}.data 3
scoreboard players set #ts_den {ns}.data 4
scoreboard players operation @s {ns}.zb.trap.cd *= #ts_num {ns}.data
scoreboard players operation @s {ns}.zb.trap.cd /= #ts_den {ns}.data
""")

	## Run as the trap centre marker.
	write_versioned_function("zombies/traps/cooldown_tick", f"""
# A cooldown above its max is a stale absolute deadline from older versions: clear it.
execute if score @s {ns}.zb.trap.cd > @s {ns}.zb.trap.cd_max run scoreboard players set @s {ns}.zb.trap.cd 0

scoreboard players operation @s {ns}.zb.trap.cd -= #tick_delta {ns}.data
""")

	write_versioned_function("zombies/traps/damage_fire", f"""
# 1000% of each zombie's max health.
data modify storage {ns}:temp _trap_dmg.type set value "minecraft:on_fire"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function {ns}:v{version}/zombies/traps/kill_zombie

# Players inside take 5 fire damage, unless they own PhD Flopper.
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={{{ns}.zb.in_game=1,{ns}.special.phd_flopper=0}},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:on_fire
""")

	write_versioned_function("zombies/traps/damage_electric", f"""
# 1000% of each zombie's max health.
data modify storage {ns}:temp _trap_dmg.type set value "minecraft:lightning_bolt"
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @e[tag={ns}.zombie_round,dx=$(sx),dy=$(sy),dz=$(sz)] run function {ns}:v{version}/zombies/traps/kill_zombie

# Players inside take 5 electric damage, unless they own PhD Flopper.
$execute positioned ~-$(rx) ~-$(ry) ~-$(rz) as @a[scores={{{ns}.zb.in_game=1,{ns}.special.phd_flopper=0}},gamemode=!creative,gamemode=!spectator,dx=$(sx),dy=$(sy),dz=$(sz)] run damage @s 5 minecraft:lightning_bolt
""")

	## The caller sets _trap_dmg.type.
	write_versioned_function("zombies/traps/kill_zombie", f"""
execute store result storage {ns}:temp _trap_dmg.amount int 1 run attribute @s minecraft:max_health get 10
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _trap_dmg
""")

	write_versioned_function("zombies/traps/apply_trap_damage", """
$damage @s $(amount) $(type)
""")

