""" Collecting the upgraded weapon back off the machine. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ...common import ZombiesCommon


# Functions
def write_pap_collect() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_not_your_weapon: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This upgraded weapon belongs to another player.","color":"red"}')

	# Run from on_right_click while the machine is in the collectible range (1..205).
	write_versioned_function("zombies/pap/anim/collect", f"""
# Machine-context functions target the player through this tag.
tag @s add {ns}.pap_owner
execute store result score #pap_mid {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id

# Ownership is read into a flag first: collect_give resets zb.pap_mid, so testing it afterwards would trip the deny branch.
scoreboard players set #pap_owns {ns}.data 0
execute if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run scoreboard players set #pap_owns {ns}.data 1

execute if score #pap_owns {ns}.data matches 1 as @n[tag=bs.interaction.target] at @s run function {ns}:v{version}/zombies/pap/anim/collect_at_machine
execute if score #pap_owns {ns}.data matches 0 run {deny_not_your_weapon}
tag @s remove {ns}.pap_owner
""")

	# Run as the machine.
	write_versioned_function("zombies/pap/anim/collect_at_machine", f"""
execute store result storage {ns}:temp _pap_c.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/anim/collect_lookup with storage {ns}:temp _pap_c
""")

	write_versioned_function("zombies/pap/anim/collect_lookup", f"""
$data modify storage {ns}:temp _pap_cg.slot set from storage {ns}:zombies pap_anim_slot."$(id)"
$data modify storage {ns}:temp _pap_cg.id set value $(id)
function {ns}:v{version}/zombies/pap/anim/collect_give with storage {ns}:temp _pap_cg
""")

	write_versioned_function("zombies/pap/anim/collect_give", f"""
$item replace entity @p[tag={ns}.pap_owner] $(slot) from entity @n[tag={ns}.pap_weapon_display,distance=..2] contents

execute as @p[tag={ns}.pap_owner] run function {ns}:v{version}/ammo/compute_reserve

scoreboard players set @s {ns}.pap_anim -1

# The item was already given back.
kill @e[tag={ns}.pap_weapon_display,distance=..2]

execute store result score #pap_mid {ns}.data run scoreboard players get @s {ns}.zb.pap.id
execute as @a[scores={{{ns}.zb.pap_s=1..}}] if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run scoreboard players set @s {ns}.zb.pap_s 0
execute as @a[scores={{{ns}.zb.pap_mid=1..}}] if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run scoreboard players set @s {ns}.zb.pap_mid 0

$data remove storage {ns}:zombies pap_anim_slot."$(id)"

execute as @p[tag={ns}.pap_owner] run {ZombiesFeedback.zb_sound('success')}
""")

	# Timeslip: two extra steps per tick, so the upgrade advances 3 ticks per tick while every exact-tick trigger still runs.
	# Only while pap_anim >= 206 (sliding in, inside, sliding out): the collectible retreat (1..205) stays at 1x for everyone.
	write_versioned_function("zombies/pap/anim/step_timeslip", f"""
execute if score @s {ns}.pap_anim matches 206.. run function {ns}:v{version}/zombies/pap/anim/step
execute if score @s {ns}.pap_anim matches 206.. run function {ns}:v{version}/zombies/pap/anim/step
""")

