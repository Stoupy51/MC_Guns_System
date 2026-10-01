""" Class selection menu and the perk effects applied when a loadout is equipped. """

# Imports
from stewbeet import (
	Dialog,
	DialogTag,
	Mem,
	set_json_encoder,
	write_load_file,
	write_versioned_function,
)

from ....config.catalogs import TRIG_EDITOR_START, TRIG_MARKETPLACE, TRIG_MY_LOADOUTS
from ....config.stats.items import ItemBuilder
from ...helpers import MGS_TAG
from ..classes import MultiplayerClasses


# Functions
def generate_class_selection() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# 1-10 standard class, negative custom loadout id, 0 none.
scoreboard objectives add {ns}.mp.class dummy

scoreboard objectives add {ns}.mp.death_count deathCount

scoreboard objectives add {ns}.class_menu minecraft.used:minecraft.warped_fungus_on_a_stick
""")

	write_versioned_function("player/tick", f"""
execute if score @s {ns}.class_menu matches 1.. if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{class_menu:true}}}}] run function {ns}:v{version}/multiplayer/select_class
scoreboard players set @s {ns}.class_menu 0
""")

	write_versioned_function("multiplayer/show_dialog", "$dialog show @s $(dialog)")

	## Appends one action per class, then recurses.
	write_versioned_function("multiplayer/build_class_btn", f"""
$data modify storage {ns}:temp _btn set value {{label:{{text:"$(name)",color:"green"}},tooltip:["",{{text:"$(lore)","color":"gray"}},{{"text":"\\n"}},{{"text":"Primary"}},": ",{{"text":"$(main_gun)","color":"green"}},{{"text":" x$(main_mag_count) mags","color":"dark_green"}},{{"text":"\\n"}},["",{{"text":"Secondary"}},": "],{{"text":"$(secondary_gun)","color":"yellow"}},{{"text":" x$(secondary_mag_count) mags","color":"gold"}},{{"text":"\\n"}},["",{{"text":"Grenades"}},": "],{{"text":"$(equip_display)","color":"aqua"}},{{"text":"\\n"}},["",{{"text":"Perks"}},": "],{{"text":"$(perks_display)","color":"light_purple"}},"\\n\\n",{{"text":"\u25b6 Click to select","color":"dark_gray","italic":true}}],action:{{type:"run_command",command:"/trigger {ns}.player.config set $(trigger_value)"}}}}

data modify storage {ns}:temp dialog.actions append from storage {ns}:temp _btn

data remove storage {ns}:temp class_iter[0]
execute if data storage {ns}:temp class_iter[0] run function {ns}:v{version}/multiplayer/build_class_btn with storage {ns}:temp class_iter[0]
""")

	## Built per player, so it is a dynamic dialog.
	write_versioned_function("multiplayer/select_class", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:{{text:"Select Your Class",color:"gold",bold:true}},body:{{type:"minecraft:item",item:{{id:"minecraft:crossbow"}},description:{{contents:{{text:"Choose a class for multiplayer",color:"gray"}}}},show_decoration:false,show_tooltip:true}},actions:[],columns:2,after_action:"close",exit_action:{{label:"Cancel"}}}}

data modify storage {ns}:temp class_iter set from storage {ns}:multiplayer classes_list

execute if data storage {ns}:temp class_iter[0] run function {ns}:v{version}/multiplayer/build_class_btn with storage {ns}:temp class_iter[0]

data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"✚ ",color:"aqua",bold:true}},{{text:"Create Loadout"}}],tooltip:{{text:"Build a custom loadout from scratch"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}
data modify storage {ns}:temp dialog.actions append value {{label:["","📦 ",{{text:"My Loadouts",color:"yellow",bold:true}}],tooltip:{{text:"Manage your custom loadouts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}
data modify storage {ns}:temp dialog.actions append value {{label:["","🌍 ",{{text:"Marketplace",color:"light_purple",bold:true}}],tooltip:{{text:"Browse public loadouts from other players"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE}"}}}}

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## Quick Action launcher (#minecraft:quick_actions), opened from the pause screen: the only dialog kept as a file, since dialog tags only reference registered dialogs.
	## It fires trigger 4 (select_class); external_title is the pack name, which Minecraft shows when several packs add a quick action.
	pack_name: str = Mem.ctx.project_name
	Mem.ctx.data[ns].dialogs["open_class_menu"] = set_json_encoder(Dialog({
		"type": "minecraft:multi_action",
		"external_title": pack_name,
		"title": {"text": pack_name, "color": "gold", "bold": True},
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Open the class & loadouts menu", "color": "gray"}}],
		"actions": [{
			"label": {"text": "Open Class Menu", "color": "green"},
			"action": {"type": "run_command", "command": f"/trigger {ns}.player.config set 4"},
		}],
		"columns": 1,
		"exit_action": {"label": {"translate": "gui.cancel"}},
	}))

	# Merged, so other packs' entries stay.
	dialog_ref: str = f"{ns}:open_class_menu"
	qa_values: list[str] = []
	if "quick_actions" in Mem.ctx.data["minecraft"].dialogs_tags:
		qa_values = list(Mem.ctx.data["minecraft"].dialogs_tags["quick_actions"].data.get("values", []))
	if dialog_ref not in qa_values:
		qa_values.append(dialog_ref)
	Mem.ctx.data["minecraft"].dialogs_tags["quick_actions"] = set_json_encoder(
		DialogTag({"replace": False, "values": qa_values})
	)

	## Run from the trigger dispatch (values 11-20 are classes 1-10).
	apply_now: str = f"""{{"text":" [✔]","color":"gold","hover_event":{{"action":"show_text","value":{{"text":"Click here to apply immediately (OP only)","color":"yellow"}}}},"click_event":{{"action":"run_command","command":"/function {ns}:v{version}/multiplayer/apply_class"}}}}"""
	write_versioned_function("multiplayer/set_class", f"""
$scoreboard players set @s {ns}.mp.class $(class_num)

# Applied at the next respawn.
$execute if data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{MGS_TAG},["",{{"text":"Class set to"}}," "],{{"text":"$(class_name)","color":"green","bold":true}},{{"text":" - will apply on respawn","color":"yellow"}},{apply_now}]

# Outside a game the choice is only saved.
$execute unless data storage {ns}:multiplayer game{{state:"active"}} run tellraw @s ["",{MGS_TAG},["",{{"text":"Class set to"}}," "],{{"text":"$(class_name)","color":"green","bold":true}},{apply_now}]
""")

	## classes_list is ordered, so the class at index class_num - 1 is copied to temp and applied.
	apply_commands: str = f"""
execute if score @s {ns}.mp.class matches ..-1 run return run function {ns}:v{version}/multiplayer/apply_custom_class

"""
	for class_num in MultiplayerClasses.CLASS_IDS.values():
		apply_commands += f"execute if score @s {ns}.mp.class matches {class_num} run data modify storage {ns}:temp current_class set from storage {ns}:multiplayer classes_list[{class_num - 1}]\n"

	apply_commands += f"""
function {ns}:v{version}/multiplayer/apply_class_dynamic
"""

	write_versioned_function("multiplayer/apply_class", apply_commands)

	write_versioned_function("multiplayer/apply_custom_class", f"""
# mp.class is minus the loadout id.
scoreboard players operation #loadout_id {ns}.data = @s {ns}.mp.class
scoreboard players operation #loadout_id {ns}.data *= #minus_one {ns}.data

data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts

execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/apply_custom_found
""")

	write_versioned_function("multiplayer/apply_custom_found", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run return run function {ns}:v{version}/multiplayer/apply_custom_match

data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/apply_custom_found
""")

	write_versioned_function("multiplayer/apply_custom_match", f"""
# Same layout as a standard class, so both go through apply_class_dynamic, which then applies current_class.perks.
data modify storage {ns}:temp current_class set value {{slots:[],perks:[]}}
data modify storage {ns}:temp current_class.slots set from storage {ns}:temp _find_iter[0].slots
data modify storage {ns}:temp current_class.perks set from storage {ns}:temp _find_iter[0].perks
# The knife camo lives outside slots[] (hotbar.0 is always given); loadouts saved before knife camos have none, and apply_class_dynamic defaults it.
execute if data storage {ns}:temp _find_iter[0].knife_camo run data modify storage {ns}:temp current_class.knife_camo set from storage {ns}:temp _find_iter[0].knife_camo

function {ns}:v{version}/multiplayer/apply_class_dynamic
""")

	## Scavenger and Quick Fix, run as the killer (signal listener).
	write_versioned_function("multiplayer/perks/on_kill", f"""
execute unless score @s {ns}.mp.in_game matches 1 run return fail

# Scavenger refills the spare magazines on every kill, not the loaded weapon.
execute if score @s {ns}.special.scavenger matches 1 run function {ns}:v{version}/multiplayer/perks/scavenger_refill

# Quick Fix starts health regen at once (last_hit threshold 100).
execute if score @s {ns}.special.quick_fix matches 1 run scoreboard players set @s {ns}.last_hit 100
execute if score @s {ns}.special.quick_fix matches 1 run effect give @s minecraft:regeneration 3 1 true
""", tags=[f"{ns}:signals/on_kill"])

	## Reuses the per-slot magazine refill; never the loaded weapon.
	scavenger_slot_checks: str = "".join(
		f'execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true}}}}] run function {ns}:v{version}/zombies/bonus/refill_magazine {{slot:"{slot}"}}\n'
		for slot in ItemBuilder.ALL_SLOTS
	)
	write_versioned_function("multiplayer/perks/scavenger_refill", f"""
{scavenger_slot_checks}
function {ns}:v{version}/ammo/compute_reserve
""")

	## Run from player tick on a real vanilla death (environmental only).
	write_versioned_function("multiplayer/on_respawn", f"""
scoreboard players set @s {ns}.mp.death_count 0

# Already spectating: this vanilla death was handled as a simulated death in the same tick.
execute if score @s {ns}.mp.spectate_timer matches 1.. run return 0
execute if entity @s[gamemode=spectator] run return 0

scoreboard players add @s {ns}.mp.deaths 1

# Vanilla damage kills land here, melee included (knives are an attack_damage attribute, not a raycast),
# so the kill is credited through signals/on_kill like a bullet kill.
tag @s add {ns}.temp_victim
execute on attacker run tag @s add {ns}.temp_killer

# Self-damage: no kill credit, and the fall-through prints a self-death message.
execute if entity @s[tag={ns}.temp_killer] run tag @s remove {ns}.temp_killer

execute if entity @a[tag={ns}.temp_killer] run function {ns}:v{version}/multiplayer/vanilla_kill_credit
execute unless entity @a[tag={ns}.temp_killer] run function {ns}:v{version}/multiplayer/random_death_message
tag @s remove {ns}.temp_victim

function {ns}:v{version}/multiplayer/enter_death_spectate
""")

	## Run as the victim, with {ns}.temp_killer on the attacker. Same credit as simulate_death_fire_kill: the gamemode's on_kill and the on-kill perks.
	write_versioned_function("multiplayer/vanilla_kill_credit", f"""
execute as @a[tag={ns}.temp_killer] run function #{ns}:signals/on_kill

# Melee, fall and fire never go through the raycast, so no headshot; cleared so a previous bullet kill cannot leak into it.
scoreboard players set #mp_kill_headshot {ns}.data 0
function {ns}:v{version}/multiplayer/random_kill_message
""")

	write_versioned_function("multiplayer/spectate_random_player", f"""
execute as @r[scores={{{ns}.mp.in_game=1}},gamemode=!spectator] run spectate @s @p[scores={{{ns}.mp.spectate_timer=1..}},sort=nearest]
""")

	write_versioned_function("multiplayer/actual_respawn", f"""
spectate @s

function {ns}:v{version}/multiplayer/respawn_tp

# The stamina system owns the hunger bar.
scoreboard players set @s {ns}.stam_seen 0

# Positive: standard class, negative: custom loadout.
execute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class

gamemode adventure @s

execute if data storage {ns}:multiplayer game.map.respawn_commands[0] at @s run function {ns}:v{version}/shared/run_respawn_commands {{mode:"multiplayer"}}

# Run as the respawning player.
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"respawn"}}
""")

	## Sets mp.class to minus mp.default, then applies it.
	write_versioned_function("multiplayer/auto_apply_default", f"""
scoreboard players operation @s {ns}.mp.class = @s {ns}.mp.default
scoreboard players operation @s {ns}.mp.class *= #minus_one {ns}.data

function {ns}:v{version}/multiplayer/apply_class
""")

	write_versioned_function("player/tick", f"""
# death_count comes from the deathCount criterion.
execute if data storage {ns}:multiplayer game{{state:"active"}} if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/multiplayer/on_respawn

execute if data storage {ns}:missions game{{state:"active"}} if score @s {ns}.mi.in_game matches 1.. if score @s {ns}.mp.death_count matches 1.. run function {ns}:v{version}/missions/on_respawn
""")

