""" Buying a trap: the power, cooldown and points guards. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon


# Functions
def write_trap_interaction() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_requires_power: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This trap requires power.","color":"red"}')
	deny_not_ready: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Trap is on cooldown and not ready yet.","color":"yellow"}')
	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#trap_price")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/traps/on_right_click", f"""
# Guard: game must be active
{ZombiesCommon.game_active_guard_cmd(ns)}

# Check power requirement
execute store result score #trap_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.power
execute if score #trap_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run {deny_requires_power}

# Get trap ID
execute store result score #trap_id {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.id

# Check if trap is ready (not active, not on cooldown)
scoreboard players set #trap_ready {ns}.data 0
execute as @e[type=minecraft:marker,tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data if score @s {ns}.zb.trap.timer matches 0 if score @s {ns}.zb.trap.cd matches ..0 run scoreboard players set #trap_ready {ns}.data 1
execute unless score #trap_ready {ns}.data matches 1 run return run {deny_not_ready}

# Check price
execute store result score #trap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.price
execute unless score @s {ns}.zb.points >= #trap_price {ns}.data run return run {deny_not_enough_points}

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #trap_price {ns}.data

# Activate trap (set timer = duration on the marker)
execute as @e[type=minecraft:marker,tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data run scoreboard players operation @s {ns}.zb.trap.timer = @s {ns}.zb.trap.dur

# Timeslip: remember whether this activator earns the reduced cooldown (checked at deactivation)
execute unless score @s {ns}.special.timeslip matches 1.. as @e[type=minecraft:marker,tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data run scoreboard players set @s {ns}.zb.trap.timeslip 0
execute if score @s {ns}.special.timeslip matches 1.. as @e[type=minecraft:marker,tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data run scoreboard players set @s {ns}.zb.trap.timeslip 1

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Trap activated for ","color":"gold"}},{{"score":{{"name":"#trap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"gold"}}]
{ZombiesFeedback.zb_sound('announce')}
""")

