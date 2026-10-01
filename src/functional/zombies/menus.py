""" Zombies setup, map selection and admin dialogs. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs, PickerOption
from .rewards.powerups.types import POWERUP_TYPES

# Constants
PU_ADMIN_EMOJI: dict[str, str] = {
	"max_ammo": "📦",
	"insta_kill": "💀",
	"double_points": "💰",
	"carpenter": "🔨",
	"nuke": "☢",
	"unlimited_ammo": "🔫",
	"random_perk": "🧪",
	"free_pap": "💠",
	"cash_drop": "💵",
	"fire_sale": "🏷",
	"bonfire_sale": "🔥",
}
""" Button emoji per power-up for the admin Force Power-Up menu (falls back to ⚡). """

# Functions
def generate_zombies_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Vanilla: classic CoD zombies; Zonweeb: passives, abilities and special zombies.
	variant_opts = [
		PickerOption(label="Vanilla", command=f'/data modify storage {ns}:zombies game.variant set value "vanilla"', color="yellow", hover="Classic CoD zombies: no passives, abilities, or special zombies"),
		PickerOption(label="Zonweeb", command=f'/data modify storage {ns}:zombies game.variant set value "zonweeb"', color="green", hover="Full experience: passives, abilities, and special zombies"),
	]
	Dialogs.register_value_picker("zombies/setup/variant", "Variant", "Choose the zombies experience", variant_opts, back_dialog="zombies/setup")

	setup_actions = [
		Dialogs.dialog_run_btn("🗺 Select Map", f"/function {ns}:v{version}/zombies/map_select", "Browse and select a zombies map", "dark_green"),
		Dialogs.dialog_show_btn(f"{ns}:zombies/setup/variant", "🧬 Variant", "Choose the zombies experience"),
		Dialogs.dialog_run_btn("▶ START", f"/function {ns}:v{version}/zombies/start", "Start the zombies game", "green"),
		Dialogs.dialog_run_btn("■ STOP", f"/function {ns}:v{version}/zombies/stop", "Stop the zombies game", "red"),
		Dialogs.dialog_run_btn("⟲ Fast Restart", f"/function {ns}:v{version}/zombies/restart", "Stop and immediately restart with the same map, variant and players", "gold"),
		Dialogs.dialog_run_btn("👥 Manage Players", f"/function {ns}:v{version}/players/list_zombies", "Add or remove players from the zombies game", "dark_aqua"),
		# The zombies equivalent of multiplayer's "Auto Team".
		Dialogs.dialog_run_btn("👥 All Players Join", f"/execute as @a run function {ns}:v{version}/players/zb_join", "Add every online player to the zombies game", "green"),
		Dialogs.dialog_run_btn("+ Join", f"/function {ns}:v{version}/zombies/join_game", "Join the ongoing zombies game as a late joiner", "yellow"),
		Dialogs.dialog_show_btn(f"{ns}:zombies/admin", "🛠 Admin / Debug", "Skip rounds, grant points and force power-ups (operators only)"),
	]
	Dialogs.register_dialog("zombies/setup", {
		"type": "minecraft:multi_action",
		"title": ["", "🧟 ", {"text": "Zombies Setup", "color": "dark_green", "bold": True}, " 🧟"],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Pick a map and variant, then Start", "color": "gray"}}],
		"actions": setup_actions,
		"columns": 2,
		"exit_action": Dialogs.dialog_back_action("config", tooltip="Return to the configuration menu"),
	})

	write_versioned_function("zombies/setup", f"dialog show @s {Dialogs.dialog_ref('zombies/setup')}")

	## Admin menu: every action reuses the normal game paths, so it cannot produce a state the round logic never does.
	## Each button is a /function, which vanilla restricts to permission level 2.
	generate_zombies_admin_menu(ns, version)

	write_versioned_function("zombies/map_select", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🗺 ",{{text:"Select Zombies Map",color:"dark_green",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Click a map to select it",color:"gray"}}}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{{label:["","◀ ",{{text:"Back",color:"gray"}}],tooltip:{{text:"Return to setup"}},action:{{type:"show_dialog",dialog:"{ns}:v{version}/zombies/setup"}}}}}}

data modify storage {ns}:temp _map_iter set from storage {ns}:maps zombies
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "zombies"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

# multi_action needs at least one action.
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No zombies maps",color:"red"}},tooltip:{{text:"Create one in the map editor first"}},action:{{type:"show_dialog",dialog:"{ns}:v{version}/zombies/setup"}}}}

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

def generate_zombies_admin_menu(ns: str, version: str) -> None:
	""" Register the operator-only zombies debug menu and the functions its buttons run. """
	## Reproduces what game_tick watches for (no zombie alive, none to spawn), so the normal round end runs once.
	write_versioned_function("zombies/admin/force_round_end", f"""
kill @e[tag={ns}.zombie_round]
scoreboard players set #zb_to_spawn {ns}.data 0
""")

	## start_round increments game.round, so the stored round is set to current + delta - 1.
	for delta in (1, 5, 10, 50):
		write_versioned_function(f"zombies/admin/round_skip_{delta}", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data {delta - 1}
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data
function {ns}:v{version}/zombies/admin/force_round_end
tellraw @a [{MGS_TAG},{{"text":"An operator skipped ahead {delta} round(s).","color":"yellow"}}]
""")

	## One toggle, so the dialog needs no per-state label.
	write_versioned_function("zombies/admin/freeze_toggle", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
execute if score #zb_freeze {ns}.data matches 1 run return run function {ns}:v{version}/zombies/freeze_off
function {ns}:v{version}/zombies/freeze_on
""")

	## To every player in the game, so scores stay comparable.
	for amount in (2500, 500000):
		write_versioned_function(f"zombies/admin/points_add_{amount}", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points {amount}
tellraw @a [{MGS_TAG},{{"text":"An operator granted {amount} points to everyone.","color":"green"}}]
""")

	write_versioned_function("zombies/admin/points_reset", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
scoreboard players set @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points 0
scoreboard players operation @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.xp_pts_prev = @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points
tellraw @a [{MGS_TAG},{{"text":"An operator reset everyone's points.","color":"red"}}]
""")

	## The real activation functions run, so everything behaves as a real pickup. Some act as the collector and need
	## {ns}.pu_collecting: the clicking operator when playing, otherwise any in-game player.
	write_versioned_function("zombies/admin/powerup", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
tag @s[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] add {ns}.pu_collecting
execute unless entity @a[tag={ns}.pu_collecting] run tag @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,limit=1] add {ns}.pu_collecting
execute unless entity @a[tag={ns}.pu_collecting] run return run tellraw @s [{MGS_TAG},{{"text":"No living player in the game to receive the power-up.","color":"red"}}]
$function {ns}:v{version}/zombies/powerups/activate/$(type)
tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	## A sub-dialog keeps the main admin dialog readable.
	Dialogs.register_dialog("zombies/admin/powerups", {
		"type": "minecraft:multi_action",
		"title": ["", "🛠 ", {"text": "Force Power-Up", "color": "dark_red", "bold": True}],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Triggers the real power-up, for everyone", "color": "gray"}}],
		"actions": [
			Dialogs.dialog_run_btn(f"{PU_ADMIN_EMOJI.get(pu_id, '⚡')} {v.display}", f'/function {ns}:v{version}/zombies/admin/powerup {{type:"{pu_id}"}}', f"Force {v.display} for everyone", v.color)
			for pu_id, v in POWERUP_TYPES.items()
		],
		"columns": 2,
		"exit_action": Dialogs.dialog_back_action("zombies/admin", tooltip="Return to the admin menu"),
	})

	Dialogs.register_dialog("zombies/admin", {
		"type": "minecraft:multi_action",
		"title": ["", "🛠 ", {"text": "Zombies Admin", "color": "dark_red", "bold": True}],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Debug tools (operators only)", "color": "gray"}}],
		"actions": [
			Dialogs.dialog_run_btn("⏭ Skip Round", f"/function {ns}:v{version}/zombies/admin/round_skip_1", "End this round and start the next one", "yellow"),
			Dialogs.dialog_run_btn("⏩ Skip 5 Rounds", f"/function {ns}:v{version}/zombies/admin/round_skip_5", "Jump forward 5 rounds", "gold"),
			Dialogs.dialog_run_btn("⏩ Skip 10 Rounds", f"/function {ns}:v{version}/zombies/admin/round_skip_10", "Jump forward 10 rounds", "gold"),
			Dialogs.dialog_run_btn("⏩ Skip 50 Rounds", f"/function {ns}:v{version}/zombies/admin/round_skip_50", "Jump forward 50 rounds", "gold"),
			Dialogs.dialog_show_btn(f"{ns}:zombies/admin/powerups", "⚡ Force Power-Up", "Trigger any power-up for everyone"),
			Dialogs.dialog_run_btn("⟲ Reset Points", f"/function {ns}:v{version}/zombies/admin/points_reset", "Set every player's points back to 0", "red"),
			Dialogs.dialog_run_btn("+2500 Points", f"/function {ns}:v{version}/zombies/admin/points_add_2500", "Give every player 2500 points", "green"),
			Dialogs.dialog_run_btn("+500000 Points", f"/function {ns}:v{version}/zombies/admin/points_add_500000", "Give every player 500000 points", "green"),
			Dialogs.dialog_run_btn("⏸ Freeze / Unfreeze", f"/function {ns}:v{version}/zombies/admin/freeze_toggle", "Pause the game: no mob moves, no player moves, every timer stops", "aqua"),
			Dialogs.dialog_run_btn("🔧 Unfreeze Round", f"/function {ns}:zombies/recover", "Rebuild a round that has stopped advancing (stuck at 0 zombies)", "aqua"),
		],
		"columns": 2,
		"exit_action": Dialogs.dialog_back_action("zombies/setup", tooltip="Return to the zombies setup menu"),
	})

