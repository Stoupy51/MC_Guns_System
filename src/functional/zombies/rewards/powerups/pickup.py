""" Collecting a power-up and dispatching to its activation. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....progression import Xp
from ...common import ZombiesCommon
from .types import POWERUP_TYPES, pu_activate_sound, pu_snd


# Functions
def write_powerup_pickup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	gun_cd: str = ZombiesCommon.gun_cd(ns)
	free_pap_type: int = POWERUP_TYPES["free_pap"].type_num

	# Pickup
	write_versioned_function("zombies/powerups/do_pickup", f"""
# Free PaP is the only power-up spent on a specific item, the gun held in hotbar 1-3, so it is the only
# one a player can be unable to use: downed players are spectators, and the knife (hotbar.0) and the
# grenade slots (hotbar.6-7) are not weapons it can upgrade. Leave the drop on the ground for a
# teammate who can take it rather than burning it on someone it would do nothing for.
scoreboard players set #pu_pap_ok {ns}.data 0
execute if score @s {ns}.zb.pu.type matches {free_pap_type} as @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5] run function {ns}:v{version}/zombies/powerups/check_pap_taker
execute if score @s {ns}.zb.pu.type matches {free_pap_type} if score #pu_pap_ok {ns}.data matches 0 run return fail

# Tag the nearest eligible player as the collector for this activation
tag @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] add {ns}.pu_collecting

# If no alive player collected, a downed player crawled their mannequin over it: credit them.
execute unless entity @a[tag={ns}.pu_collecting] if entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5] run function {ns}:v{version}/zombies/powerups/pickup_downed_collector

# Store power-up type before killing the entity
scoreboard players operation #pu_type_pickup {ns}.data = @s {ns}.zb.pu.type

# Kill the text display first (we still have a valid position)
kill @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3]

# Grab cue
{pu_snd(ns, "item/grab", 0.4)}

# Activate the power-up effect (collector tag is still active here)
function {ns}:v{version}/zombies/powerups/dispatch_activate

# Silent award: there are eleven power-up types with eleven different announces, so there is no single
# message to suffix. The bar moving is the feedback.
{Xp.give("zb", "powerup", f"@a[tag={ns}.pu_collecting]")}

# Kill this power-up item entity
kill @s
scoreboard players remove #pu_active {ns}.data 1

# Clean up the collector tag so other pickups can proceed
tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	# Can this player spend a Free PaP right now? (@s = nearest living player to the drop)
	# Same rule as the upgrade itself (see pap/upgrade_core): a gun in the selected hotbar slot 1-3.
	# When they cannot, the drop stays put and the actionbar says what they are missing.
	write_versioned_function("zombies/powerups/check_pap_taker", f"""
execute store result score #pu_pap_sel {ns}.data run data get entity @s SelectedItemSlot
execute if score #pu_pap_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players set #pu_pap_ok {ns}.data 1
execute if score #pu_pap_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players set #pu_pap_ok {ns}.data 1
execute if score #pu_pap_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players set #pu_pap_ok {ns}.data 1
execute if score #pu_pap_ok {ns}.data matches 0 run data modify storage smithed.actionbar:input message set value {{json:["✦ ",{{"text":"Free Pack-a-Punch","color":"aqua"}},{{"text":" - ","color":"gray"}},{{"text":"Hold a weapon to take it","color":"red"}}],priority:"conditional",freeze:5}}
execute if score #pu_pap_ok {ns}.data matches 0 run function #smithed.actionbar:message
""")

	# Tag the owner of the nearest downed mannequin (a downed spectator) as the collector, so a crawling downed player can grab power-ups.
	# @s = the power-up item entity.
	write_versioned_function("zombies/powerups/pickup_downed_collector", f"""
scoreboard players set #pu_downed_id {ns}.data -1
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5,sort=nearest,limit=1] run scoreboard players operation #pu_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.downed_id = #pu_downed_id {ns}.data run tag @s add {ns}.pu_collecting
""")

	dispatch_activate_lines: str = "\n".join(
		f"execute if score #pu_type_pickup {ns}.data matches {v.type_num} run function {ns}:v{version}/zombies/powerups/activate/{pu_id}"
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/dispatch_activate", dispatch_activate_lines)

	# Activation functions

	## 1. Max Ammo (no chat message — the sound is enough)
	write_versioned_function("zombies/powerups/activate/max_ammo", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/max_ammo
{pu_activate_sound(ns, POWERUP_TYPES["max_ammo"])}
""")

	## 2-4.

