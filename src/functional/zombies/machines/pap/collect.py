""" Collecting the upgraded weapon back off the machine. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ...common import ZombiesCommon


# Functions
def write_pap_collect() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_not_your_weapon: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This upgraded weapon belongs to another player.","color":"red"}')

	# Called from on_right_click when machine pap_anim is in collectible range (1..150).
	write_versioned_function("zombies/pap/anim/collect", f"""
# Tag the clicking player so machine-context functions can target them precisely
tag @s add {ns}.pap_owner
execute store result score #pap_mid {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id

# Resolve ownership into a flag BEFORE acting: a successful collect (collect_give) resets the
# player's zb.pap_mid to 0, so re-testing the comparison afterwards would spuriously trip the
# deny branch ("belongs to another player") right after the weapon was returned.
scoreboard players set #pap_owns {ns}.data 0
execute if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run scoreboard players set #pap_owns {ns}.data 1

execute if score #pap_owns {ns}.data matches 1 as @n[tag=bs.interaction.target] at @s run function {ns}:v{version}/zombies/pap/anim/collect_at_machine
execute if score #pap_owns {ns}.data matches 0 run {deny_not_your_weapon}
tag @s remove {ns}.pap_owner
""")

	# Resolve machine ID and call lookup (runs as machine).
	write_versioned_function("zombies/pap/anim/collect_at_machine", f"""
execute store result storage {ns}:temp _pap_c.id int 1 run scoreboard players get @s {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/anim/collect_lookup with storage {ns}:temp _pap_c
""")

	# Macro $(id): fetch stored slot string and pass id, then call give.
	write_versioned_function("zombies/pap/anim/collect_lookup", f"""
$data modify storage {ns}:temp _pap_cg.slot set from storage {ns}:zombies pap_anim_slot."$(id)"
$data modify storage {ns}:temp _pap_cg.id set value $(id)
function {ns}:v{version}/zombies/pap/anim/collect_give with storage {ns}:temp _pap_cg
""")

	# Macro $(slot): give weapon back from display entity's contents slot, cleanup, restore display, notify.
	write_versioned_function("zombies/pap/anim/collect_give", f"""
# Return upgraded weapon directly from the display entity's contents slot
$item replace entity @p[tag={ns}.pap_owner] $(slot) from entity @n[tag={ns}.pap_weapon_display,distance=..2] contents

# Refresh ammo HUD
execute as @p[tag={ns}.pap_owner] run function {ns}:v{version}/ammo/compute_reserve

# Reset animation timer to idle
scoreboard players set @s {ns}.pap_anim -1

# Remove weapon display (item already given back, safe to kill)
kill @e[tag={ns}.pap_weapon_display,distance=..2]

# Clear PAP slot tracking for the original owner
execute store result score #pap_mid {ns}.data run scoreboard players get @s {ns}.zb.pap.id
execute as @a[scores={{{ns}.zb.pap_s=1..}}] if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run scoreboard players set @s {ns}.zb.pap_s 0
execute as @a[scores={{{ns}.zb.pap_mid=1..}}] if score @s {ns}.zb.pap_mid = #pap_mid {ns}.data run scoreboard players set @s {ns}.zb.pap_mid 0

# Clean stored slot data
$data remove storage {ns}:zombies pap_anim_slot."$(id)"

# Notify the player
execute as @p[tag={ns}.pap_owner] run {ZombiesFeedback.zb_sound('success')}
""")

	# Timeslip: run two EXTRA anim steps this tick for a Timeslip-owned machine, so the UPGRADE advances 3 ticks per real tick.
	# Stepping (rather than decrementing by 3) preserves every exact-tick phase trigger — each intermediate timer value is still processed.
	# Gated on pap_anim>=206 (the going-in/inside/coming-out upgrade phase, timer 300→206): Timeslip only speeds up the UPGRADE, never the retreat/collectible phase (1..205).
	# Once the weapon has emerged and is collectible it retreats at the normal 1x rate, so the collect window is the full ~10s for Timeslip owners too (this also stops the extras running into the retreat or past the animation end at -1).
	# The base step still runs it once from game_tick regardless.
	write_versioned_function("zombies/pap/anim/step_timeslip", f"""
execute if score @s {ns}.pap_anim matches 206.. run function {ns}:v{version}/zombies/pap/anim/step
execute if score @s {ns}.pap_anim matches 206.. run function {ns}:v{version}/zombies/pap/anim/step
""")

