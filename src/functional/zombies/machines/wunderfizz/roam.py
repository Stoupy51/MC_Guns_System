""" Roaming to another spot when a pull turns up the teddy bear. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from .shared import WF_MOVE_BEAR_POOF, WF_MOVE_RELOCATE, WF_MOVE_TICKS


# Functions
def write_wunderfizz_roam() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Roam landing (@s = orb, positioned at the active machine): refund the buyer, then start the move.
	write_versioned_function("zombies/wunderfizz/land_bear", f"""
# Refund the buyer (the machine roams away instead of granting a perk — Black Ops teddy-bear rule)
scoreboard players operation #wf_b {ns}.data = @s {ns}.zb.wf.buyer
scoreboard players operation #wf_refund {ns}.data = @s {ns}.zb.wf.paid
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.wf_pid = #wf_b {ns}.data run scoreboard players operation @s {ns}.zb.points += #wf_refund {ns}.data

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Der Wunderfizz is moving!","color":"yellow","bold":true}}]
{ZombiesFeedback.zb_sound('box_bye_bye')}

# Spawn the teddy bear at the active machine and start the roam timer, then remove the orb
execute as @n[tag={ns}.wf_active] at @s run function {ns}:v{version}/zombies/wunderfizz/move_start
kill @s
""")

	## Begin the roam (@s = active interaction entity, at @s).
	## Spawn a rising teddy bear near the cabinet and start the move timer.
	write_versioned_function("zombies/wunderfizz/move_start", f"""
execute positioned ~ ~-1.5 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.wf_bear","{ns}.gm_entity","{ns}.wf_bear_new"],item_display:"fixed",billboard:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}}}
loot replace entity @n[tag={ns}.wf_bear_new] contents loot {ns}:zombies/roaming_bear
data merge entity @n[tag={ns}.wf_bear_new] {{teleport_duration:2}}
tag @e[tag={ns}.wf_bear_new] remove {ns}.wf_bear_new
scoreboard players set #wf_move_timer {ns}.data {WF_MOVE_TICKS}
""")

	## Roam tick (hooked into game_tick while #wf_move_timer > 0)
	write_versioned_function("zombies/wunderfizz/move_tick", f"""
scoreboard players remove #wf_move_timer {ns}.data 1

# Bear rises before the swap
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_RELOCATE + 1}.. as @e[tag={ns}.wf_bear] at @s run tp @s ~ ~0.06 ~

# Midpoint: relocate the active spot (model swap + interaction visibility)
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_RELOCATE} run function {ns}:v{version}/zombies/wunderfizz/do_relocate

# Bear poofs shortly after
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_BEAR_POOF} as @e[tag={ns}.wf_bear] at @s run particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.02 15 force @a[distance=..48]
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_BEAR_POOF} run kill @e[tag={ns}.wf_bear]

# Arrival
execute if score #wf_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/wunderfizz/move_land
""")

	## Swap the active spot to a new random position (@s not required).
	## Old cabinet grays out, new one lights up, interaction reachability follows.
	write_versioned_function("zombies/wunderfizz/do_relocate", f"""
tag @e[tag={ns}.wf_active] add {ns}.wf_prev_active
tag @e[tag={ns}.wf_active] remove {ns}.wf_active
execute as @n[tag={ns}.wunderfizz_machine,tag=!{ns}.wf_prev_active,sort=random] run tag @s add {ns}.wf_active
tag @e[tag={ns}.wf_prev_active] remove {ns}.wf_prev_active

function {ns}:v{version}/zombies/wunderfizz/sync_displays
function {ns}:v{version}/zombies/wunderfizz/sync_visibility

# Arrival particles/sound at the new active cabinet
execute as @n[tag={ns}.wf_active] at @s run particle minecraft:end_rod ~ ~-1 ~ 0.3 1.5 0.3 0.05 25 force @a[distance=..64]
execute as @n[tag={ns}.wf_active] at @s run playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.6 1.6
""")

	write_versioned_function("zombies/wunderfizz/move_land", f"""
scoreboard players set #wf_move_timer {ns}.data 0
kill @e[tag={ns}.wf_bear]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Der Wunderfizz has arrived at a new location!","color":"yellow"}}]
execute as @n[tag={ns}.wf_active] at @s run {ZombiesFeedback.zb_sound('announce')}
""")

