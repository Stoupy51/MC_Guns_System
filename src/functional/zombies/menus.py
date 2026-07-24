
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG, dialog_back_action, dialog_function, dialog_run_btn, dialog_show_btn, register_dialog, register_value_picker
from .powerups import POWERUP_TYPES

# Button emoji per power-up for the admin Force Power-Up menu (falls back to ⚡).
_PU_ADMIN_EMOJI: dict[str, str] = {
	"max_ammo": "📦", "insta_kill": "💀", "double_points": "💰", "carpenter": "🔨",
	"nuke": "☢", "unlimited_ammo": "🔫", "random_perk": "🧪", "free_pap": "💠",
	"cash_drop": "💵", "fire_sale": "🏷", "bonfire_sale": "🔥",
}


def generate_zombies_menus() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Variant picker (Vanilla = classic CoD zombies, Zonweeb = passives/abilities/special zombies)
	variant_opts = [
		("Vanilla", f'/data modify storage {ns}:zombies game.variant set value "vanilla"', "yellow", "Classic CoD zombies: no passives, abilities, or special zombies"),
		("Zonweeb", f'/data modify storage {ns}:zombies game.variant set value "zonweeb"', "green", "Full experience: passives, abilities, and special zombies"),
	]
	register_value_picker("zombies/setup/variant", "Variant", "Choose the zombies experience", variant_opts, back_dialog="zombies/setup")

	## Main zombies setup dialog
	setup_actions = [
		dialog_run_btn("🗺 Select Map", f"/function {ns}:v{version}/zombies/map_select", "Browse and select a zombies map", "dark_green"),
		dialog_show_btn(f"{ns}:zombies/setup/variant", "🧬 Variant", "Choose the zombies experience"),
		dialog_run_btn("▶ START", f"/function {ns}:v{version}/zombies/start", "Start the zombies game", "green"),
		dialog_run_btn("■ STOP", f"/function {ns}:v{version}/zombies/stop", "Stop the zombies game", "red"),
		dialog_run_btn("⟲ Fast Restart", f"/function {ns}:v{version}/zombies/restart", "Stop and immediately restart with the same map, variant and players", "gold"),
		dialog_run_btn("👥 Manage Players", f"/function {ns}:v{version}/players/list_zombies", "Add or remove players from the zombies game", "dark_aqua"),
		# Multiplayer has "Auto Team" to seat everyone at once; this is the zombies equivalent.
		dialog_run_btn("👥 All Players Join", f"/execute as @a run function {ns}:v{version}/players/zb_join", "Add every online player to the zombies game", "green"),
		dialog_run_btn("+ Join", f"/function {ns}:v{version}/zombies/join_game", "Join the ongoing zombies game as a late joiner", "yellow"),
		dialog_show_btn(f"{ns}:zombies/admin", "🛠 Admin / Debug", "Skip rounds, grant points and force power-ups (operators only)"),
	]
	register_dialog("zombies/setup", {
		"type": "minecraft:multi_action",
		"title": ["", "🧟 ", {"text": "Zombies Setup", "color": "dark_green", "bold": True}, " 🧟"],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Pick a map and variant, then Start", "color": "gray"}}],
		"actions": setup_actions,
		"columns": 2,
		"exit_action": dialog_back_action("config", tooltip="Return to the configuration menu"),
	})

	# /function .../zombies/setup now opens the dialog
	write_versioned_function("zombies/setup", f"function {dialog_function('zombies/setup')}")

	## Admin / debug menu ────────────────────────────────────────
	## Everything here reuses the normal game paths rather than poking state directly, so a debug
	## action can't leave a game in a shape the round logic never produces. Reachable only by
	## operators: every button is a /function, which vanilla already restricts to permission level 2.
	generate_zombies_admin_menu(ns, version)

	## Map selection menu: build a dialog listing all available zombies maps
	write_versioned_function("zombies/map_select", f"""
# Build the base map-select dialog (empty actions), then append one button per map
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:["","🗺 ",{{text:"Select Zombies Map",color:"dark_green",bold:true}}],body:[{{type:"minecraft:plain_message",contents:{{text:"Click a map to select it",color:"gray"}}}}],actions:[],columns:1,pause:false,after_action:"none",exit_action:{{label:["","◀ ",{{text:"Back",color:"gray"}}],tooltip:{{text:"Return to setup"}},action:{{type:"show_dialog",dialog:"{ns}:v{version}/zombies/setup"}}}}}}

# Copy maps list and iterate (select_entry appends one button per map)
data modify storage {ns}:temp _map_iter set from storage {ns}:maps zombies
scoreboard players set #map_idx {ns}.data 0
data modify storage {ns}:temp _map_select_mode set value "zombies"
execute if data storage {ns}:temp _map_iter[0] run function {ns}:v{version}/shared/maps/select_iter

# Empty fallback: multi_action requires a non-empty actions list
execute unless data storage {ns}:temp dialog.actions[0] run data modify storage {ns}:temp dialog.actions append value {{label:{{text:"No zombies maps",color:"red"}},tooltip:{{text:"Create one in the map editor first"}},action:{{type:"show_dialog",dialog:"{ns}:v{version}/zombies/setup"}}}}

# Show the completed dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")


def generate_zombies_admin_menu(ns: str, version: str) -> None:
	""" Register the operator-only zombies debug menu and the functions its buttons run.

	Args:
		ns      (str): The project namespace.
		version (str): The project version, used to build function paths.
	"""
	## Force the current round to end. Rather than calling round_complete directly, this reproduces
	## the condition game_tick already watches for (no zombies alive, none left to spawn), so the
	## normal round-end path runs exactly once with all its announcements and respawns intact.
	write_versioned_function("zombies/admin/force_round_end", f"""
kill @e[tag={ns}.zombie_round]
scoreboard players set #zb_to_spawn {ns}.data 0
""")

	## Round jumps. start_round increments game.round itself, so to land on "current + delta" the
	## stored round is set to "current + delta - 1" before the round is forced to end.
	for delta in (1, 5, 10, 50):
		write_versioned_function(f"zombies/admin/round_skip_{delta}", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data {delta - 1}
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data
function {ns}:v{version}/zombies/admin/force_round_end
tellraw @a [{MGS_TAG},{{"text":"An operator skipped ahead {delta} round(s).","color":"yellow"}}]
""")

	## Point grants, applied to every player in the game so scores stay comparable
	for amount in (2500, 500000):
		write_versioned_function(f"zombies/admin/points_add_{amount}", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
scoreboard players add @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points {amount}
tellraw @a [{MGS_TAG},{{"text":"An operator granted {amount} points to everyone.","color":"green"}}]
""")

	write_versioned_function("zombies/admin/points_reset", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
scoreboard players set @a[scores={{{ns}.zb.in_game=1}}] {ns}.zb.points 0
tellraw @a [{MGS_TAG},{{"text":"An operator reset everyone's points.","color":"red"}}]
""")

	## Power-ups reuse the real activation functions, so bossbars, sounds and timers all behave
	## exactly as if the power-up had been picked up off the floor.
	# Generated from POWERUP_TYPES so EVERY power-up is always present (no drift when new ones are added).
	admin_powerups: list[tuple[str, str, str, str]] = [
		(pu_id, f'{_PU_ADMIN_EMOJI.get(pu_id, "⚡")} {v["display"]}', v["color"], f'Force {v["display"]} for everyone')
		for pu_id, v in POWERUP_TYPES.items()
	]
	## Some power-ups (Nuke, Free PaP, Cash Drop, Random Perk) act "as the player who picked it up"
	## and do nothing at all without the {ns}.pu_collecting tag a real pickup sets — the Nuke's kill
	## loop in particular never starts, so the fire and sounds play while every zombie survives.
	## Nominate a collector here: the clicking operator when they are actually playing, otherwise any
	## in-game player, so the button still works from spectator.
	write_versioned_function("zombies/admin/powerup", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]
tag @s[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] add {ns}.pu_collecting
execute unless entity @a[tag={ns}.pu_collecting] run tag @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,limit=1] add {ns}.pu_collecting
execute unless entity @a[tag={ns}.pu_collecting] run return run tellraw @s [{MGS_TAG},{{"text":"No living player in the game to receive the power-up.","color":"red"}}]
$function {ns}:v{version}/zombies/powerups/activate/$(type)
tag @a[tag={ns}.pu_collecting] remove {ns}.pu_collecting
""")

	## Power-up sub-dialog (kept separate so the main admin dialog stays readable)
	register_dialog("zombies/admin/powerups", {
		"type": "minecraft:multi_action",
		"title": ["", "🛠 ", {"text": "Force Power-Up", "color": "dark_red", "bold": True}],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Triggers the real power-up, for everyone", "color": "gray"}}],
		"actions": [
			dialog_run_btn(label, f'/function {ns}:v{version}/zombies/admin/powerup {{type:"{pu_id}"}}', hover, color)
			for pu_id, label, color, hover in admin_powerups
		],
		"columns": 2,
		"exit_action": dialog_back_action("zombies/admin", tooltip="Return to the admin menu"),
	})

	## Main admin dialog
	register_dialog("zombies/admin", {
		"type": "minecraft:multi_action",
		"title": ["", "🛠 ", {"text": "Zombies Admin", "color": "dark_red", "bold": True}],
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Debug tools — operators only", "color": "gray"}}],
		"actions": [
			dialog_run_btn("⏭ Skip Round", f"/function {ns}:v{version}/zombies/admin/round_skip_1", "End this round and start the next one", "yellow"),
			dialog_run_btn("⏩ Skip 5 Rounds", f"/function {ns}:v{version}/zombies/admin/round_skip_5", "Jump forward 5 rounds", "gold"),
			dialog_run_btn("⏩ Skip 10 Rounds", f"/function {ns}:v{version}/zombies/admin/round_skip_10", "Jump forward 10 rounds", "gold"),
			dialog_run_btn("⏩ Skip 50 Rounds", f"/function {ns}:v{version}/zombies/admin/round_skip_50", "Jump forward 50 rounds", "gold"),
			dialog_show_btn(f"{ns}:zombies/admin/powerups", "⚡ Force Power-Up", "Trigger any power-up for everyone"),
			dialog_run_btn("⟲ Reset Points", f"/function {ns}:v{version}/zombies/admin/points_reset", "Set every player's points back to 0", "red"),
			dialog_run_btn("+2500 Points", f"/function {ns}:v{version}/zombies/admin/points_add_2500", "Give every player 2500 points", "green"),
			dialog_run_btn("+500000 Points", f"/function {ns}:v{version}/zombies/admin/points_add_500000", "Give every player 500000 points", "green"),
			dialog_run_btn("🔧 Unfreeze Round", f"/function {ns}:zombies/recover", "Rebuild a round that has stopped advancing (stuck at 0 zombies)", "aqua"),
		],
		"columns": 2,
		"exit_action": dialog_back_action("zombies/setup", tooltip="Return to the zombies setup menu"),
	})

