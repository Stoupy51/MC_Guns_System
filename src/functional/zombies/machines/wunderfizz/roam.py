""" Roaming to another spot when a pull turns up the teddy bear. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from .shared import WF_MOVE_BEAR_POOF, WF_MOVE_RELOCATE, WF_MOVE_TICKS


# Functions
def write_wunderfizz_roam() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Run as the orb, at the active machine.
	write_versioned_function("zombies/wunderfizz/land_bear", f"""
# The machine roams instead of granting a perk (Black Ops teddy bear rule).
scoreboard players operation #wf_b {ns}.data = @s {ns}.zb.wf.buyer
scoreboard players operation #wf_refund {ns}.data = @s {ns}.zb.wf.paid
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.wf_pid = #wf_b {ns}.data run scoreboard players operation @s {ns}.zb.points += #wf_refund {ns}.data

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Der Wunderfizz is moving!","color":"yellow","bold":true}}]
{ZombiesFeedback.zb_sound('box_bye_bye')}

execute as @n[tag={ns}.wf_active] at @s run function {ns}:v{version}/zombies/wunderfizz/move_start
kill @s
""")

	## Run as the active interaction entity: a rising teddy bear and the move timer.
	write_versioned_function("zombies/wunderfizz/move_start", f"""
execute positioned ~ ~-1.5 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.wf_bear","{ns}.gm_entity","{ns}.wf_bear_new"],item_display:"fixed",billboard:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}}}
loot replace entity @n[tag={ns}.wf_bear_new] contents loot {ns}:zombies/roaming_bear
data merge entity @n[tag={ns}.wf_bear_new] {{teleport_duration:2}}
tag @e[tag={ns}.wf_bear_new] remove {ns}.wf_bear_new
scoreboard players set #wf_move_timer {ns}.data {WF_MOVE_TICKS}
""")

	## Runs from game_tick while #wf_move_timer > 0.
	write_versioned_function("zombies/wunderfizz/move_tick", f"""
scoreboard players remove #wf_move_timer {ns}.data 1

execute if score #wf_move_timer {ns}.data matches {WF_MOVE_RELOCATE + 1}.. as @e[tag={ns}.wf_bear] at @s run tp @s ~ ~0.06 ~

# Midpoint: model swap and interaction visibility.
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_RELOCATE} run function {ns}:v{version}/zombies/wunderfizz/do_relocate

execute if score #wf_move_timer {ns}.data matches {WF_MOVE_BEAR_POOF} as @e[tag={ns}.wf_bear] at @s run particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.02 15 force @a[distance=..48]
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_BEAR_POOF} run kill @e[tag={ns}.wf_bear]

execute if score #wf_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/wunderfizz/move_land
""")

	## The old cabinet grays out, the new one lights up.
	write_versioned_function("zombies/wunderfizz/do_relocate", f"""
tag @e[tag={ns}.wf_active] add {ns}.wf_prev_active
tag @e[tag={ns}.wf_active] remove {ns}.wf_active
execute as @n[tag={ns}.wunderfizz_machine,tag=!{ns}.wf_prev_active,sort=random] run tag @s add {ns}.wf_active
tag @e[tag={ns}.wf_prev_active] remove {ns}.wf_prev_active

function {ns}:v{version}/zombies/wunderfizz/sync_displays
function {ns}:v{version}/zombies/wunderfizz/sync_visibility

execute as @n[tag={ns}.wf_active] at @s run particle minecraft:end_rod ~ ~-1 ~ 0.3 1.5 0.3 0.05 25 force @a[distance=..64]
execute as @n[tag={ns}.wf_active] at @s run playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.6 1.6
""")

	write_versioned_function("zombies/wunderfizz/move_land", f"""
scoreboard players set #wf_move_timer {ns}.data 0
kill @e[tag={ns}.wf_bear]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Der Wunderfizz has arrived at a new location!","color":"yellow"}}]
execute as @n[tag={ns}.wf_active] at @s run {ZombiesFeedback.zb_sound('announce')}
""")

