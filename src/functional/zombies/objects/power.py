""" Power switch system.

A one-time activatable wall switch (custom breaker-box model) that enables power for the map.
Elements with power:true (perk machines, traps) require power to be active.
The switch renders as an item_display using the {ns}:power_switch model (database/items.py).
Activating it swaps to {ns}:power_switch_on, recoloring the handle and indicator light green.
"""
# Imports
from stewbeet import Mem, write_versioned_function

from ...core.feedback import ZombiesFeedback
from ...helpers import MGS_TAG
from ...progression import Xp
from ..common import ZombiesCommon


# Functions
def generate_power_switch() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	deny_already_on: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Power is already on.","color":"yellow"}')

	write_versioned_function("zombies/power/setup", f"""
data modify storage {ns}:temp _pw_iter set from storage {ns}:zombies game.map.power_switch
execute if data storage {ns}:temp _pw_iter[0] run function {ns}:v{version}/zombies/power/setup_iter
""")

	write_versioned_function("zombies/power/setup_iter", f"""
execute store result score #pwx {ns}.data run data get storage {ns}:temp _pw_iter[0].pos[0]
execute store result score #pwy {ns}.data run data get storage {ns}:temp _pw_iter[0].pos[1]
execute store result score #pwz {ns}.data run data get storage {ns}:temp _pw_iter[0].pos[2]
scoreboard players operation #pwx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #pwy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #pwz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _pw.x int 1 run scoreboard players get #pwx {ns}.data
execute store result storage {ns}:temp _pw.y int 1 run scoreboard players get #pwy {ns}.data
execute store result storage {ns}:temp _pw.z int 1 run scoreboard players get #pwz {ns}.data

# Stored yaw is player yaw + 180 so the switch faces the placer, like the machines. This model faces the other way,
# so its display rotation is 0 instead of -180 (see database/models/power_switch.json).
data modify storage {ns}:temp _pw.yaw set value 0.0f
execute if data storage {ns}:temp _pw_iter[0].rotation[0] run data modify storage {ns}:temp _pw.yaw set from storage {ns}:temp _pw_iter[0].rotation[0]

function {ns}:v{version}/zombies/power/place_at with storage {ns}:temp _pw

data remove storage {ns}:temp _pw_iter[0]
execute if data storage {ns}:temp _pw_iter[0] run function {ns}:v{version}/zombies/power/setup_iter
""")

	write_versioned_function("zombies/power/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:0.9f,height:0.9f,response:true,Tags:["{ns}.power_switch","{ns}.gm_entity","bs.entity.interaction","_pw_new"]}}

$execute positioned $(x) $(y) $(z) align xyz positioned ~.5 ~.5 ~.5 run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw)f,0f],Tags:["{ns}.power_switch_disp","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:lever",count:1,components:{{"minecraft:item_model":"{ns}:power_switch"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}}}

execute as @e[tag=_pw_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/power/on_activate",executor:"source"}}
execute as @e[tag=_pw_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/power/on_hover",executor:"source"}}
tag @e[tag=_pw_new] remove _pw_new
""")

	## Run as the clicking player.
	write_versioned_function("zombies/power/on_activate", f"""
{ZombiesCommon.game_active_guard_cmd(ns)}

execute if score #zb_power {ns}.data matches 1 run return run {deny_already_on}

scoreboard players set #zb_power {ns}.data 1

execute as @e[tag={ns}.power_switch] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag={ns}.power_switch] at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a ~ ~ ~ 2 1

# Displays switch to the lit model.
execute as @e[tag={ns}.power_switch_disp] run data modify entity @s item.components."minecraft:item_model" set value "{ns}:power_switch_on"

# One-time use: the interactions go, the displays stay.
kill @e[tag={ns}.power_switch]

# The whole roster earns it, so no earner split.
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Power is ON!","color":"green","bold":true}},{Xp.suffix("zb", "power")}]
{Xp.give("zb", "power", f"@a[scores={{{ns}.zb.in_game=1}}]")}
{ZombiesFeedback.zb_sound('power_on')}

function {ns}:v{version}/shared/maps/call_script_at_base {{script:"power"}}
""")

	## Run as the player looking at the switch.
	write_versioned_function("zombies/power/on_hover", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"text":"Power Switch","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/start", f"""
scoreboard players set #zb_power {ns}.data 0
""")

	write_versioned_function("zombies/preload_complete", f"""
execute if data storage {ns}:zombies game.map.power_switch[0] run function {ns}:v{version}/zombies/power/setup
""")

