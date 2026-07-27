""" The /function mgs:config dialog tree: categories, value pickers and mode setup entries. """
# Imports
from stewbeet import Mem, write_function

from ..helpers.dialogs import Dialogs
from ..helpers.text import Text


# Functions
def write_config_menu() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Config menu (/function mgs:config), a dialog-based settings menu.
	# The main dialog lists every setting as a button opening its own sub-dialog of value buttons.
	# Picking a value runs the scoreboard command directly.
	# Each value button is independent with no submit step, so opening the menu never resets untouched settings.
	# --- Global Settings (server-wide fake-player scores) ---
	rpg_opts = [
		(str(i), f"/scoreboard players set #projectile_explosion_power {ns}.config {i}",
         "green" if i == 0 else "yellow",
         f"Set Projectile Explosion Power to {i}" + (" (disabled)" if i == 0 else ""))
		for i in range(6)
	]
	gren_opts = [
		(str(i), f"/scoreboard players set #grenade_explosion_power {ns}.config {i}",
         "green" if i == 0 else "yellow",
         f"Set Grenade Explosion Power to {i}" + (" (disabled)" if i == 0 else ""))
		for i in range(6)
	]
	ma_opts = [
		("OG", f"/scoreboard players set #max_ammo_reload_weapons {ns}.config 0", "yellow", "Only refill magazines in inventory (OG zombies)"),
		("Recent", f"/scoreboard players set #max_ammo_reload_weapons {ns}.config 1", "green", "Also reload current weapon (recent zombies)"),
	]
	dd_opts = [
		("OFF", f"/scoreboard players set #damage_debug {ns}.config 0", "red", "Disable global damage debug"),
		("ON", f"/scoreboard players set #damage_debug {ns}.config 1", "green", "Enable global damage debug (tellraw @a every hit)"),
	]

	# --- Player Specials (self-only scores; commands run as the clicking player) ---
	duration_opts = [("OFF", 0, "red"), ("10s", 200, "yellow"), ("30s", 600, "yellow"), ("60s", 1200, "yellow"), ("∞", 72000, "light_purple")]
	percent_opts = [("0%", 0, "red"), ("20%", 20, "yellow"), ("50%", 50, "yellow"), ("80%", 80, "green")]
	ik_opts = [(label, f"/scoreboard players set @s {ns}.special.instant_kill {v}", color,
				f"Set instant kill {'off' if v == 0 else f'for {label}'}") for label, v, color in duration_opts]
	ia_opts = [(label, f"/scoreboard players set @s {ns}.special.infinite_ammo {v}", color,
				f"Set infinite ammo {'off' if v == 0 else f'for {label}'}") for label, v, color in duration_opts]
	qr_opts = [(label, f"/scoreboard players set @s {ns}.special.quick_reload {v}", color,
				f"Set quick reload to {label}") for label, v, color in percent_opts]
	qs_opts = [(label, f"/scoreboard players set @s {ns}.special.quick_swap {v}", color,
				f"Set quick swap to {label}") for label, v, color in percent_opts]

	# Register every value sub-dialog: (sub_id, title, description, options)
	value_dialogs = [
		("config/rpg_power", "RPG Explosion Power", "Server-wide projectile explosion power", rpg_opts),
		("config/grenade_power", "Grenade Explosion Power", "Server-wide grenade explosion power", gren_opts),
		("config/max_ammo", "Max Ammo Mode", "How the Max Ammo powerup refills weapons", ma_opts),
		("config/damage_debug", "Damage Debug", "Broadcast every hit's damage to chat", dd_opts),
		("config/instant_kill", "Instant Kill", "One-shot kills for a duration (self only)", ik_opts),
		("config/infinite_ammo", "Infinite Ammo", "No reloads needed for a duration (self only)", ia_opts),
		("config/quick_reload", "Quick Reload", "Reduce reload time (self only)", qr_opts),
		("config/quick_swap", "Quick Swap", "Reduce weapon-swap time (self only)", qs_opts),
	]
	# Each value picker's Back button returns to its parent category (global / personal).
	picker_back = {
		"config/rpg_power": "config/global", "config/grenade_power": "config/global",
		"config/max_ammo": "config/global", "config/damage_debug": "config/global",
		"config/instant_kill": "config/personal", "config/infinite_ammo": "config/personal",
		"config/quick_reload": "config/personal", "config/quick_swap": "config/personal",
	}
	for sub_id, title_text, desc, options in value_dialogs:
		Dialogs.register_value_picker(sub_id, title_text, desc, options, back_dialog=picker_back[sub_id])

	# --- Configuration dialog, organized into categories (by scope) ---
	# The top-level menu is a short list of categories; each opens its own sub-dialog whose Back button returns to the top-level config.
	# Leaf value pickers Back to their category (above).
	def register_category(sub_id: str, title: str, actions: list[dict[str, str]]) -> None:
		Dialogs.register_dialog(sub_id, {
			"type": "minecraft:multi_action",
			"title": Text.split_emoji(title, color="gold", bold=True),
			"actions": actions,
			# Each category lists items of a single kind (settings / mode links) → one column.
			"columns": 1,
			"exit_action": Dialogs.dialog_back_action("config", tooltip="Return to configuration"),
		})

	register_category("config/global", "⚙ Global Settings", [
		Dialogs.dialog_show_btn(f"{ns}:config/rpg_power", "RPG Explosion Power", "Server-wide projectile explosion power", "red"),
		Dialogs.dialog_show_btn(f"{ns}:config/grenade_power", "Grenade Explosion Power", "Server-wide grenade explosion power", "gold"),
		Dialogs.dialog_show_btn(f"{ns}:config/max_ammo", "Max Ammo Mode", "How the Max Ammo powerup refills weapons", "aqua"),
		Dialogs.dialog_show_btn(f"{ns}:config/damage_debug", "Damage Debug", "Broadcast every hit's damage to chat", "yellow"),
	])
	register_category("config/personal", "⚡ Personal Cheats", [
		Dialogs.dialog_show_btn(f"{ns}:config/instant_kill", "Instant Kill", "One-shot kills for a duration (self only)", "red"),
		Dialogs.dialog_show_btn(f"{ns}:config/infinite_ammo", "Infinite Ammo", "No reloads needed for a duration (self only)", "gold"),
		Dialogs.dialog_show_btn(f"{ns}:config/quick_reload", "Quick Reload", "Reduce reload time (self only)", "green"),
		Dialogs.dialog_show_btn(f"{ns}:config/quick_swap", "Quick Swap", "Reduce weapon-swap time (self only)", "aqua"),
	])
	# The three game-mode setups sit directly on the first page instead of behind a "Game Modes" category — opening a mode used to cost two clicks for no benefit.
	# There is no "Players & Teams" category either: team assignment only makes sense in the context of one mode, and every mode's setup dialog already carries its own "Manage Players" button.
	config_actions = [
		# Row 1: the game modes, side by side (see columns=3 below)
		Dialogs.dialog_show_btn(f"{ns}:multiplayer/setup", "⚔ Multiplayer", "Open the multiplayer game setup menu", "red"),
		Dialogs.dialog_show_btn(f"{ns}:zombies/setup", "🧟 Zombies", "Open the zombies setup menu", "green"),
		Dialogs.dialog_show_btn(f"{ns}:missions/setup", "🎯 Missions", "Open the mission setup menu", "gold"),
		# Row 2: settings and tools
		Dialogs.dialog_show_btn(f"{ns}:config/global", "⚙ Global Settings", "Server-wide gameplay settings", "gold"),
		Dialogs.dialog_show_btn(f"{ns}:config/personal", "⚡ Personal Cheats", "Self-only powerups", "light_purple"),
		Dialogs.dialog_run_btn("🗺 Map Editor", f"/function {ns}:v{version}/maps/editor/menu", "Open the map editor", "yellow"),
	]
	Dialogs.register_dialog("config", {
		"type": "minecraft:multi_action",
		"title": Text.split_emoji("☣ MGS Configuration ☣", color="gold", bold=True),
		"body": [{"type": "minecraft:plain_message", "contents": {"text": "Pick a game mode, or a settings category", "color": "gray"}}],
		"actions": config_actions,
		# 3 columns lays the actions out as two rows: the game modes, then settings + tools.
		"columns": 3,
		"exit_action": {"label": {"translate": "gui.done"}},
	})

	# /function mgs:config now opens the (inline) dialog
	write_function(f"{ns}:config", f"function {Dialogs.dialog_function('config')}")

