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

	write_versioned_function("zombies/powerups/do_pickup", f"""
# Free PaP upgrades the gun in hotbar 1-3, so a player without one cannot use it: the drop stays for a teammate.
scoreboard players set #pu_pap_ok {ns}.data 0
execute if score @s {ns}.zb.pu.type matches {free_pap_type} as @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5] run function {ns}:v{version}/zombies/powerups/check_pap_taker
execute if score @s {ns}.zb.pu.type matches {free_pap_type} if score #pu_pap_ok {ns}.data matches 0 run return fail

# The nearest eligible player collects.
tag @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] add {ns}.pu_collecting

# Nobody alive took it: a downed player crawled their mannequin over it.
execute unless entity @a[tag={ns}.pu_collecting] if entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5] run function {ns}:v{version}/zombies/powerups/pickup_downed_collector

scoreboard players operation #pu_type_pickup {ns}.data = @s {ns}.zb.pu.type

# First, while the position is still valid.
kill @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3]

{pu_snd(ns, "item/grab", 0.4)}

# The collector tag is still set here.
function {ns}:v{version}/zombies/powerups/dispatch_activate

# Silent award: eleven types with eleven announces, so no single message to suffix.
{Xp.give("zb", "powerup", f"@a[tag={ns}.pu_collecting]")}

kill @s
scoreboard players remove #pu_active {ns}.data 1

tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	# Run as the nearest living player: the upgrade_core rule (a gun in hotbar 1-3); otherwise the actionbar says why.
	write_versioned_function("zombies/powerups/check_pap_taker", f"""
execute store result score #pu_pap_sel {ns}.data run data get entity @s SelectedItemSlot
execute if score #pu_pap_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players set #pu_pap_ok {ns}.data 1
execute if score #pu_pap_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players set #pu_pap_ok {ns}.data 1
execute if score #pu_pap_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players set #pu_pap_ok {ns}.data 1
execute if score #pu_pap_ok {ns}.data matches 0 run data modify storage smithed.actionbar:input message set value {{json:["✦ ",{{"text":"Free Pack-a-Punch","color":"aqua"}},{{"text":" - ","color":"gray"}},{{"text":"Hold a weapon to take it","color":"red"}}],priority:"conditional",freeze:5}}
execute if score #pu_pap_ok {ns}.data matches 0 run function #smithed.actionbar:message
""")

	# Run as the power-up item: the owner of the nearest downed mannequin collects.
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

	## 1. Max Ammo (the sound is the message)
	write_versioned_function("zombies/powerups/activate/max_ammo", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:zombies/bonus/max_ammo
{pu_activate_sound(ns, POWERUP_TYPES["max_ammo"])}
""")

	## 2-4.

