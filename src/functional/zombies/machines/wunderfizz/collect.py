""" Collecting the rolled perk, hover feedback and the game hooks. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ..perks.definitions import PERK_DEFINITIONS
from .shared import PERK_IDS


# Functions
def write_wunderfizz_collect() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Uncollected after the 10s window (@s = orb): despawn (no refund — the spin already happened)
	write_versioned_function("zombies/wunderfizz/orb_expire", """
particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.02 10 force @a[distance=..48]
kill @s
""")

	## Collect (@s = player, at machine): apply the orb's chosen perk, then despawn the orb
	collect_dispatch: str = "\n".join(
		f'execute if score #wf_pick {ns}.data matches {i} run data modify storage {ns}:temp _wf_grant.perk_id set value "{pid}"'
		for i, pid in enumerate(PERK_IDS)
	)
	write_versioned_function("zombies/wunderfizz/collect", f"""
scoreboard players operation #wf_pick {ns}.data = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.perk
data remove storage {ns}:temp _wf_grant.perk_id
{collect_dispatch}
execute if data storage {ns}:temp _wf_grant.perk_id run function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _wf_grant
execute if data storage {ns}:temp _wf_grant.perk_id run function #{ns}:zombies/on_new_perk
kill @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3]
{ZombiesFeedback.zb_sound('success')}
""")

	## Hover
	write_versioned_function("zombies/wunderfizz/on_hover", f"""
# If this player's perk is ready to collect here, prompt the pick-up (with the perk name) instead of the cost
execute at @n[tag=bs.interaction.target] if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3,scores={{{ns}.zb.wf.anim=..0}}] if score @s {ns}.zb.wf_pid = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.buyer run return run function {ns}:v{version}/zombies/wunderfizz/hover_result

execute store result score #wf_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wf.price
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎰 Der Wunderfizz","color":"gold"}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#wf_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points  (random perk)","color":"gray"}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	## Ready-orb hover: name the perk waiting to be collected, e.g.
	## "✋ Pick-up Juggernog" (@s = player, positioned at the machine so the nearby orb resolves)
	hover_result_dispatch: str = "\n".join(
		f'execute if score #wf_pick {ns}.data matches {i} run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎰 ","color":"gold"}},{{"text":"Pick-up ","color":"green"}},{{"text":"{PERK_DEFINITIONS[pid].display_name}","color":"{PERK_DEFINITIONS[pid].text_color}","bold":true}}],priority:"conditional",freeze:5}}'
		for i, pid in enumerate(PERK_IDS)
	)
	write_versioned_function("zombies/wunderfizz/hover_result", f"""
scoreboard players operation #wf_pick {ns}.data = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.perk
{hover_result_dispatch}
function #smithed.actionbar:message
""")

	## Hook: setup at preload_complete
	write_versioned_function("zombies/preload_complete", f"""
execute if data storage {ns}:zombies game.map.wunderfizz[0] run function {ns}:v{version}/zombies/wunderfizz/setup
""")

	## Hook: tick orbs + any active roam
	write_versioned_function("zombies/game_tick", f"""
execute as @e[type=item_display,tag={ns}.wunderfizz_orb] at @s run function {ns}:v{version}/zombies/wunderfizz/orb_tick
execute if score #wf_move_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/wunderfizz/move_tick
""")

	## Hook: clean up machines/orbs/bears on game start/stop
	write_versioned_function("zombies/start", f"""
kill @e[type=item_display,tag={ns}.wunderfizz_orb]
kill @e[tag={ns}.wf_display]
kill @e[tag={ns}.wf_bear]
scoreboard players set #wf_uses {ns}.data 0
scoreboard players set #wf_move_timer {ns}.data 0
""")
	write_versioned_function("zombies/stop", f"""
kill @e[type=item_display,tag={ns}.wunderfizz_orb]
kill @e[tag={ns}.wf_display]
kill @e[tag={ns}.wf_bear]
scoreboard players set #wf_uses {ns}.data 0
scoreboard players set #wf_move_timer {ns}.data 0
""")

