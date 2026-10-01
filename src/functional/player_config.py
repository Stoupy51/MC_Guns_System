""" Per-player config menu and the trigger dispatch that applies its choices. """

# Imports
from stewbeet import Mem, write_versioned_function

from ..config.catalogs import (
	CAMO_VARIANTS,
	GRENADE_TYPES,
	PERKS,
	PRIMARY_WEAPONS,
	SECONDARY_WEAPONS,
	TRIG_DELETE_BASE,
	TRIG_EDIT_BASE,
	TRIG_EDITOR_START,
	TRIG_EQUIP1_CAMO_BASE,
	TRIG_EQUIP2_CAMO_BASE,
	TRIG_EQUIP_SLOT1_BASE,
	TRIG_EQUIP_SLOT2_BASE,
	TRIG_FAVORITE_BASE,
	TRIG_HUB,
	TRIG_HUB_EQUIP1,
	TRIG_HUB_EQUIP2,
	TRIG_HUB_KNIFE,
	TRIG_HUB_PERKS,
	TRIG_HUB_PRIMARY,
	TRIG_HUB_PRIMARY_MAGS,
	TRIG_HUB_SECONDARY,
	TRIG_HUB_SECONDARY_MAGS,
	TRIG_KNIFE_CAMO_BASE,
	TRIG_LIKE_BASE,
	TRIG_MANAGE_BASE,
	TRIG_MARKETPLACE,
	TRIG_MARKETPLACE_ALL,
	TRIG_MARKETPLACE_FAV_ONLY,
	TRIG_MARKETPLACE_LIKES,
	TRIG_MY_LOADOUTS,
	TRIG_MY_LOADOUTS_FAV_ONLY,
	TRIG_OVERKILL_SEC_BASE,
	TRIG_PERK_BASE,
	TRIG_PRIMARY_BASE,
	TRIG_PRIMARY_CAMO_BASE,
	TRIG_PRIMARY_MAGS_BASE,
	TRIG_PRIMARY_SCOPE_BASE,
	TRIG_REMOVE_PRIMARY,
	TRIG_REMOVE_SECONDARY,
	TRIG_SAVE_PRIVATE,
	TRIG_SAVE_PUBLIC,
	TRIG_SECONDARY_BASE,
	TRIG_SECONDARY_CAMO_BASE,
	TRIG_SECONDARY_MAGS_BASE,
	TRIG_SECONDARY_SCOPE_BASE,
	TRIG_SELECT_BASE,
	TRIG_SET_DEFAULT_BASE,
	TRIG_TOGGLE_VIS_BASE,
	TRIG_UNSET_DEFAULT,
)
from .helpers import MGS_TAG
from .multiplayer.classes import MultiplayerClasses


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Per-player config trigger (/trigger mgs.player.config set <value>) and toggles (0 off, 1 on).
	write_versioned_function("load/confirm_load", f"""
scoreboard objectives add {ns}.player.config trigger

# Off by default.
scoreboard objectives add {ns}.player.hitmarker dummy
scoreboard objectives add {ns}.player.damage_debug dummy
""", prepend=True)

	write_versioned_function("player/tick", f"""
# Bookshelf SUID.
execute unless score @s bs.id matches 0.. run function #bs.id:give_suid

scoreboard players enable @s {ns}.player.config
execute if score @s {ns}.player.config matches 1.. run function {ns}:v{version}/player/config/process

# Particles and actionbar.
execute if score @s {ns}.mp.map_edit matches 1 run function {ns}:v{version}/maps/editor/tick
""")

	## Trigger ranges count only the guns the editor lists (`if w.in_loadout`), or the ranges outgrow the buttons
	## and overlap the next block (the Overkill block once reached the knife-camo block, see TRIG_KNIFE_CAMO_BASE).
	primary_count = len([w for w in PRIMARY_WEAPONS if w.in_loadout])
	primary_max = TRIG_PRIMARY_BASE + primary_count - 1
	secondary_count = len([w for w in SECONDARY_WEAPONS if w.in_loadout])
	secondary_max = TRIG_SECONDARY_BASE + secondary_count - 1
	overkill_sec_max = TRIG_OVERKILL_SEC_BASE + primary_count - 1
	primary_mags_max = TRIG_PRIMARY_MAGS_BASE + 5
	secondary_mags_max = TRIG_SECONDARY_MAGS_BASE + 5
	perk_max = TRIG_PERK_BASE + len(PERKS) - 1
	equip1_max = TRIG_EQUIP_SLOT1_BASE + len(GRENADE_TYPES) - 1
	equip2_max = TRIG_EQUIP_SLOT2_BASE + len(GRENADE_TYPES) - 1
	primary_camo_max = TRIG_PRIMARY_CAMO_BASE + len(CAMO_VARIANTS) - 1
	secondary_camo_max = TRIG_SECONDARY_CAMO_BASE + len(CAMO_VARIANTS) - 1
	equip1_camo_max = TRIG_EQUIP1_CAMO_BASE + len(CAMO_VARIANTS) - 1
	equip2_camo_max = TRIG_EQUIP2_CAMO_BASE + len(CAMO_VARIANTS) - 1
	knife_camo_max = TRIG_KNIFE_CAMO_BASE + len(CAMO_VARIANTS) - 1
	edit_max = TRIG_EDIT_BASE + 9999
	manage_max = TRIG_MANAGE_BASE + 9999
	select_max = TRIG_SELECT_BASE + 9999  # 10000-wide range per loadout action
	favorite_max = TRIG_FAVORITE_BASE + 9999
	like_max = TRIG_LIKE_BASE + 9999
	delete_max = TRIG_DELETE_BASE + 9999
	toggle_vis_max = TRIG_TOGGLE_VIS_BASE + 9999
	set_default_max = TRIG_SET_DEFAULT_BASE + 9998  # 69999 is reserved for UNSET_DEFAULT

	write_versioned_function("player/config/process", f"""
# Isolates simultaneous editors.
execute store result storage {ns}:temp _pid int 1 run scoreboard players get @s bs.id
function {ns}:v{version}/multiplayer/editor/load_state with storage {ns}:temp

# 1 config menu, 2 hitmarker sound, 3 damage debug in chat, 4 class menu, 6-9 zombies passive and ability, 11-20 class 1-10.
execute if score @s {ns}.player.config matches 1 run function {ns}:v{version}/player/config/menu
execute if score @s {ns}.player.config matches 2 run function {ns}:v{version}/player/config/toggle_hitmarker
execute if score @s {ns}.player.config matches 3 run function {ns}:v{version}/player/config/toggle_damage_debug
execute if score @s {ns}.player.config matches 4 run function {ns}:v{version}/multiplayer/select_class
execute if score @s {ns}.player.config matches 5 run function {ns}:v{version}/zombies/passive_ability_menu
execute if score @s {ns}.player.config matches 6 run function {ns}:v{version}/zombies/perks/set_passive_1
execute if score @s {ns}.player.config matches 7 run function {ns}:v{version}/zombies/perks/set_passive_2
execute if score @s {ns}.player.config matches 8 run function {ns}:v{version}/zombies/perks/set_ability_1
execute if score @s {ns}.player.config matches 9 run function {ns}:v{version}/zombies/perks/set_ability_2
{"".join(f'execute if score @s {ns}.player.config matches {10 + class_num} run function {ns}:v{version}/multiplayer/set_class {{class_num:{class_num},class_name:"{MultiplayerClasses.CLASSES[class_id]["name"]}"}}{chr(10)}' for class_id, class_num in MultiplayerClasses.CLASS_IDS.items())}
# Custom loadout editor.
execute if score @s {ns}.player.config matches {TRIG_EDITOR_START} run function {ns}:v{version}/multiplayer/editor/start
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE} run function {ns}:v{version}/multiplayer/marketplace/browse
execute if score @s {ns}.player.config matches {TRIG_MY_LOADOUTS} run function {ns}:v{version}/multiplayer/my_loadouts/browse
# Also the no-op target of grayed-out rows.
execute if score @s {ns}.player.config matches {TRIG_HUB} run function {ns}:v{version}/multiplayer/editor/hub
execute if score @s {ns}.player.config matches {TRIG_HUB_PRIMARY} run function {ns}:v{version}/multiplayer/editor/show_primary_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_PRIMARY_MAGS} run function {ns}:v{version}/multiplayer/editor/show_primary_mags_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_SECONDARY} run function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_SECONDARY_MAGS} run function {ns}:v{version}/multiplayer/editor/show_secondary_mags_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_EQUIP1} run function {ns}:v{version}/multiplayer/editor/show_equip_slot1_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_EQUIP2} run function {ns}:v{version}/multiplayer/editor/show_equip_slot2_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_PERKS} run function {ns}:v{version}/multiplayer/editor/show_perks_dialog
execute if score @s {ns}.player.config matches {TRIG_HUB_KNIFE} run function {ns}:v{version}/multiplayer/editor/show_knife_camo_dialog
execute if score @s {ns}.player.config matches {TRIG_REMOVE_PRIMARY} run function {ns}:v{version}/multiplayer/editor/remove_primary
execute if score @s {ns}.player.config matches {TRIG_REMOVE_SECONDARY} run function {ns}:v{version}/multiplayer/editor/remove_secondary
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_BASE}..{primary_max} run function {ns}:v{version}/multiplayer/editor/pick_primary
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_SCOPE_BASE}..{TRIG_PRIMARY_SCOPE_BASE + 4} run function {ns}:v{version}/multiplayer/editor/pick_primary_scope
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_BASE}..{secondary_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary
execute if score @s {ns}.player.config matches {TRIG_OVERKILL_SEC_BASE}..{overkill_sec_max} run function {ns}:v{version}/multiplayer/editor/pick_overkill_secondary
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_SCOPE_BASE}..{TRIG_SECONDARY_SCOPE_BASE + 4} run function {ns}:v{version}/multiplayer/editor/pick_secondary_scope
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC}..{TRIG_SAVE_PRIVATE} run function {ns}:v{version}/multiplayer/editor/save
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_MAGS_BASE + 1}..{primary_mags_max} run function {ns}:v{version}/multiplayer/editor/pick_primary_mags
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_MAGS_BASE}..{secondary_mags_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary_mags
execute if score @s {ns}.player.config matches {TRIG_PERK_BASE}..{perk_max} run function {ns}:v{version}/multiplayer/editor/pick_perk
execute if score @s {ns}.player.config matches {TRIG_EQUIP_SLOT1_BASE}..{equip1_max} run function {ns}:v{version}/multiplayer/editor/pick_equip_slot1
execute if score @s {ns}.player.config matches {TRIG_EQUIP_SLOT2_BASE}..{equip2_max} run function {ns}:v{version}/multiplayer/editor/pick_equip_slot2
execute if score @s {ns}.player.config matches {TRIG_PRIMARY_CAMO_BASE}..{primary_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_primary_camo
execute if score @s {ns}.player.config matches {TRIG_SECONDARY_CAMO_BASE}..{secondary_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_secondary_camo
execute if score @s {ns}.player.config matches {TRIG_EQUIP1_CAMO_BASE}..{equip1_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_equip1_camo
execute if score @s {ns}.player.config matches {TRIG_EQUIP2_CAMO_BASE}..{equip2_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_equip2_camo
execute if score @s {ns}.player.config matches {TRIG_KNIFE_CAMO_BASE}..{knife_camo_max} run function {ns}:v{version}/multiplayer/editor/pick_knife_camo
# Custom loadout actions.
execute if score @s {ns}.player.config matches {TRIG_SELECT_BASE}..{select_max} run function {ns}:v{version}/multiplayer/custom/select
execute if score @s {ns}.player.config matches {TRIG_FAVORITE_BASE}..{favorite_max} run function {ns}:v{version}/multiplayer/custom/toggle_favorite
execute if score @s {ns}.player.config matches {TRIG_LIKE_BASE}..{like_max} run function {ns}:v{version}/multiplayer/custom/like
execute if score @s {ns}.player.config matches {TRIG_DELETE_BASE}..{delete_max} run function {ns}:v{version}/multiplayer/custom/delete
execute if score @s {ns}.player.config matches {TRIG_TOGGLE_VIS_BASE}..{toggle_vis_max} run function {ns}:v{version}/multiplayer/custom/toggle_visibility
execute if score @s {ns}.player.config matches {TRIG_SET_DEFAULT_BASE}..{set_default_max} run function {ns}:v{version}/multiplayer/custom/set_default
execute if score @s {ns}.player.config matches {TRIG_UNSET_DEFAULT} run function {ns}:v{version}/multiplayer/custom/unset_default
execute if score @s {ns}.player.config matches {TRIG_EDIT_BASE}..{edit_max} run function {ns}:v{version}/multiplayer/custom/edit
execute if score @s {ns}.player.config matches {TRIG_MANAGE_BASE}..{manage_max} run function {ns}:v{version}/multiplayer/my_loadouts/manage
# Marketplace and My Loadouts filters.
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_ALL} run function {ns}:v{version}/multiplayer/marketplace/browse
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_FAV_ONLY} run function {ns}:v{version}/multiplayer/marketplace/browse_fav_only
execute if score @s {ns}.player.config matches {TRIG_MARKETPLACE_LIKES} run function {ns}:v{version}/multiplayer/marketplace/browse_likes
execute if score @s {ns}.player.config matches {TRIG_MY_LOADOUTS_FAV_ONLY} run function {ns}:v{version}/multiplayer/my_loadouts/browse_fav_only

function {ns}:v{version}/multiplayer/editor/save_state with storage {ns}:temp

scoreboard players set @s {ns}.player.config 0
""")

	for score_name, display_name in [("hitmarker", "Hitmarker Sound"), ("damage_debug", "Damage Debug")]:
		write_versioned_function(f"player/config/toggle_{score_name}", f"""
# #toggle = 1 when it was off.
execute store success score #toggle {ns}.data unless score @s {ns}.player.{score_name} matches 1
execute if score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.{score_name} 1
execute unless score #toggle {ns}.data matches 1 run scoreboard players set @s {ns}.player.{score_name} 0
execute if score #toggle {ns}.data matches 1 run tellraw @s [{MGS_TAG},["",{{"text":"{display_name}"}},": "],{{"text":"ON","color":"green"}},{{"text":" ✔","color":"green"}}]
execute unless score #toggle {ns}.data matches 1 run tellraw @s [{MGS_TAG},["",{{"text":"{display_name}"}},": "],{{"text":"OFF","color":"red"}},{{"text":" ✘","color":"red"}}]

# Reopened, so the new state shows at once.
function {ns}:v{version}/player/config/menu
""")

	## Built per player, so toggle states show live; opened by /trigger set 1.
	write_versioned_function("player/config/menu", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🎮 ",{{text:"Player Settings",color:"gold",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Toggle your personal settings","color":"gray"}}}}],actions:[],columns:1,after_action:"close",exit_action:{{label:{{translate:"gui.done"}}}}}}

execute if score @s {ns}.player.hitmarker matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Hitmarker Sound: "}},{{text:"ON ✔",color:"green"}}],tooltip:{{text:"Toggle hitmarker sound on entity hit"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 2"}}}}
execute unless score @s {ns}.player.hitmarker matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Hitmarker Sound: "}},{{text:"OFF ✘",color:"red"}}],tooltip:{{text:"Toggle hitmarker sound on entity hit"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 2"}}}}

execute if score @s {ns}.player.damage_debug matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Damage Debug: "}},{{text:"ON ✔",color:"green"}}],tooltip:{{text:"Toggle damage numbers in chat"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 3"}}}}
execute unless score @s {ns}.player.damage_debug matches 1 run data modify storage {ns}:temp dialog.actions append value {{label:["",{{text:"Damage Debug: "}},{{text:"OFF ✘",color:"red"}}],tooltip:{{text:"Toggle damage numbers in chat"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 3"}}}}

data modify storage {ns}:temp dialog.actions append value {{label:["","⚔ ",{{text:"Multiplayer Class",color:"aqua",bold:true}}],tooltip:{{text:"Open multiplayer class selection menu"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("player/config/damage_debug", f"""
# Amount x10 as an int score, then split into whole and decimal parts.
$data modify storage {ns}:temp amount set value $(amount)
execute store result score #dmg_x10 {ns}.data run data get storage {ns}:temp amount 10
scoreboard players operation #dmg_whole {ns}.data = #dmg_x10 {ns}.data
scoreboard players operation #dmg_whole {ns}.data /= #10 {ns}.data
scoreboard players operation #dmg_dec {ns}.data = #dmg_x10 {ns}.data
scoreboard players operation #dmg_dec {ns}.data %= #10 {ns}.data

# The global config (tellraw @a) wins over the player's own (tellraw to the shooter).
$execute if score #damage_debug {ns}.config matches 1 run tellraw @a ["",[{{"text":"","color":"red"}},"[",{{"text":"DMG"}},"] "],[{{"score":{{"name":"#dmg_whole","objective":"{ns}.data"}},"color":"gold"}},".",{{"score":{{"name":"#dmg_dec","objective":"{ns}.data"}}}}]," ",{{"text":"HP to","color":"gray"}}," ",{{"selector":"$(target)"}}," ",{{"text":"by","color":"gray"}}," ",{{"selector":"$(attacker)"}}]
$execute unless score #damage_debug {ns}.config matches 1 as $(attacker) if entity @s[type=player] run tag @s add {ns}.temp_dmg_reader
tellraw @a[tag={ns}.temp_dmg_reader,scores={{{ns}.player.damage_debug=1}}] ["",[{{"text":"","color":"red"}},"[",{{"text":"DMG"}},"] "],[{{"score":{{"name":"#dmg_whole","objective":"{ns}.data"}},"color":"gold"}},".",{{"score":{{"name":"#dmg_dec","objective":"{ns}.data"}}}}]," ",{{"text":"HP to","color":"gray"}}," ",{{"selector":"@s"}}]
tag @a[tag={ns}.temp_dmg_reader] remove {ns}.temp_dmg_reader
""", tags=[f"{ns}:signals/damage"])

	## Hitscan shooters carry {ns}.ticking, explosion shooters {ns}.temp_shooter.
	write_versioned_function("player/config/hitmarker_sound", f"""
execute as @a[tag={ns}.ticking] if score @s {ns}.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 2.0
# Skipped when already played through ticking.
execute as @a[tag={ns}.temp_shooter,tag=!{ns}.ticking] if score @s {ns}.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 2.0
""", tags=[f"{ns}:signals/damage"])

