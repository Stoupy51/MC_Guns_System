""" The Zombies knife camo: unlocked by the Zombies level, picked from Player Settings, worn from the start and after a bleed-out. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ....config.catalogs import CAMO_VARIANTS, TRIG_ZB_KNIFE_CAMO_BASE, TRIG_ZB_KNIFE_MENU
from ...helpers import MGS_TAG


# Functions
def write_knife_camo() -> None:
	""" Write the picker, the pick, the unlock message and the model swap of the starting knife. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	by_level = sorted(enumerate(CAMO_VARIANTS), key=lambda pair: pair[1].zb_knife_level)

	write_load_file(f"scoreboard objectives add {ns}.zb.knife_camo dummy")

	rows: list[str] = []
	for index, camo in by_level:
		selected: str = f'{{label:["","✔ ",{{text:"{camo.display_name}",color:"green",bold:true}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_KNIFE_CAMO_BASE + index}"}}}}'
		unlocked: str = f'{{label:{{text:"{camo.display_name}",color:"yellow"}},tooltip:{{text:"Unlocked at Zombies level {camo.zb_knife_level}"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_KNIFE_CAMO_BASE + index}"}}}}'
		locked: str = f'{{label:["",{{text:"{camo.display_name}",color:"dark_gray"}},{{text:" (level {camo.zb_knife_level})",color:"dark_gray"}}],tooltip:{{text:"Reach Zombies level {camo.zb_knife_level} to unlock it"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_ZB_KNIFE_MENU}"}}}}'
		level: str = f"{ns}.zb.xp_level matches {camo.zb_knife_level}.."
		rows += [
			f"execute if score @s {ns}.zb.knife_camo matches {index} run data modify storage {ns}:temp dialog.actions append value {selected}",
			f"execute unless score @s {ns}.zb.knife_camo matches {index} if score @s {level} run data modify storage {ns}:temp dialog.actions append value {unlocked}",
			f"execute unless score @s {level} run data modify storage {ns}:temp dialog.actions append value {locked}",
		]
	write_versioned_function("zombies/knife_camo/menu", f"""
execute unless score @s {ns}.zb.knife_camo matches 0.. run scoreboard players set @s {ns}.zb.knife_camo 0
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🔪 ",{{text:"Zombies Knife Camo",color:"gold",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Camos unlock with your Zombies level","color":"gray"}}}}],actions:[],columns:1,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}
{chr(10).join(rows)}
data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Settings",color:"aqua"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 1"}}}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	picks: str = "\n".join(
		f"execute if score @s {ns}.player.config matches {TRIG_ZB_KNIFE_CAMO_BASE + index} if score @s {ns}.zb.xp_level matches {camo.zb_knife_level}.. "
		f"run scoreboard players set @s {ns}.zb.knife_camo {index}"
		for index, camo in enumerate(CAMO_VARIANTS)
	)
	write_versioned_function("zombies/knife_camo/pick", f"""
{picks}
function {ns}:v{version}/zombies/knife_camo/menu
""")

	## Run as the player who levelled; #xp_lvl_before holds the level before the award.
	unlocks: str = "\n".join(
		f'execute if score #xp_lvl_before {ns}.data matches ..{camo.zb_knife_level - 1} if score @s {ns}.zb.xp_level matches {camo.zb_knife_level}.. '
		f'run tellraw @s [{MGS_TAG},{{"text":"Zombies knife camo unlocked: ","color":"green"}},{{"text":"{camo.display_name}","color":"gold"}}]'
		for camo in CAMO_VARIANTS if camo.zb_knife_level > 1
	)
	write_versioned_function("zombies/knife_camo/on_level_up", f"""
execute unless data storage {ns}:signals on_level_up{{side:"zb"}} run return fail
{unlocks}
""", tags=[f"{ns}:progression/on_level_up"])

	swaps: str = "\n".join(
		f'execute if score @s {ns}.zb.knife_camo matches {index} run item modify entity @s hotbar.0 {{type:"minecraft:set_components",components:{{"minecraft:item_model":"{ns}:combat_knife{camo.suffix}"}}}}'
		for index, camo in enumerate(CAMO_VARIANTS) if camo.suffix
	)
	write_versioned_function("zombies/inventory/give_starting_loadout", swaps)

