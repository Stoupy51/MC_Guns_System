""" Hover feedback and the game tick / preload hooks. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_trap_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/traps/on_hover", f"""
execute store result score #trap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.price
execute store result score #trap_type {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.type
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚠ Trap","color":"red"}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#trap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}],priority:"conditional",freeze:5}}
execute if score #trap_type {ns}.data matches 0 run data modify storage smithed.actionbar:input message.json[0] set value {{"text":"🔥 Fire Trap","color":"red"}}
execute if score #trap_type {ns}.data matches 1 run data modify storage smithed.actionbar:input message.json[0] set value {{"text":"⚡ Electric Trap","color":"aqua"}}
execute if score #trap_type {ns}.data matches 2 run data modify storage smithed.actionbar:input message.json[0] set value {{"text":"🔫 Turret Trap","color":"gold"}}
function #smithed.actionbar:message
""")

	## Hook into game tick: process active traps and cooldowns
	write_versioned_function("zombies/game_tick", f"""
# Trap active tick (damage + timer)
execute as @e[type=minecraft:marker,tag={ns}.trap_center,scores={{{ns}.zb.trap.timer=1..}}] at @s run function {ns}:v{version}/zombies/traps/active_tick

# Trap cooldown tick (wall-clock via #tick_delta, same basis as the active timer)
execute as @e[type=minecraft:marker,tag={ns}.trap_center,scores={{{ns}.zb.trap.cd=1..}}] run function {ns}:v{version}/zombies/traps/cooldown_tick
""")

	## Hook into preload_complete: setup traps
	write_versioned_function("zombies/preload_complete", f"""
# Setup traps
execute if data storage {ns}:zombies game.map.traps[0] run function {ns}:v{version}/zombies/traps/setup
""")

