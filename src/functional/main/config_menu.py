""" The /function mgs:config dialog tree: categories, value pickers and mode setup entries. """
# Imports
from collections.abc import Callable

from stewbeet import Mem, write_function

from ..helpers.dialogs import Dialogs, PickerOption
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
	def power_opts(score: str, name: str) -> list[PickerOption]:
		return [
			PickerOption(label=str(i), command=f"/scoreboard players set {score} {ns}.config {i}", color="green" if i == 0 else "yellow", hover=f"Set {name} to {i}" + (" (disabled)" if i == 0 else ""))
			for i in range(6)
		]

	def config_opt(label: str, score: str, value: int, color: str, hover: str) -> PickerOption:
		return PickerOption(label=label, command=f"/scoreboard players set {score} {ns}.config {value}", color=color, hover=hover)

	Dialogs.register_value_picker("config/rpg_power", "RPG Explosion Power", "Server-wide projectile explosion power", power_opts("#projectile_explosion_power", "Projectile Explosion Power"), back_dialog="config/global")
	Dialogs.register_value_picker("config/grenade_power", "Grenade Explosion Power", "Server-wide grenade explosion power", power_opts("#grenade_explosion_power", "Grenade Explosion Power"), back_dialog="config/global")
	Dialogs.register_value_picker("config/max_ammo", "Max Ammo Mode", "How the Max Ammo powerup refills weapons", [
		config_opt("OG", "#max_ammo_reload_weapons", 0, "yellow", "Only refill magazines in inventory (OG zombies)"),
		config_opt("Recent", "#max_ammo_reload_weapons", 1, "green", "Also reload current weapon (recent zombies)"),
	], back_dialog="config/global")
	Dialogs.register_value_picker("config/damage_debug", "Damage Debug", "Broadcast every hit's damage to chat", [
		config_opt("OFF", "#damage_debug", 0, "red", "Disable global damage debug"),
		config_opt("ON", "#damage_debug", 1, "green", "Enable global damage debug (tellraw @a every hit)"),
	], back_dialog="config/global")

	# --- Player Specials (self-only scores; commands run as the clicking player) ---
	durations: dict[str, tuple[int, str]] = {"OFF": (0, "red"), "10s": (200, "yellow"), "30s": (600, "yellow"), "60s": (1200, "yellow"), "∞": (72000, "light_purple")}
	percents: dict[str, tuple[int, str]] = {"0%": (0, "red"), "20%": (20, "yellow"), "50%": (50, "yellow"), "80%": (80, "green")}

	def special_opts(special: str, values: dict[str, tuple[int, str]], hover: Callable[[str, int], str]) -> list[PickerOption]:
		return [
			PickerOption(label=label, command=f"/scoreboard players set @s {ns}.special.{special} {value}", color=color, hover=hover(label, value))
			for label, (value, color) in values.items()
		]

	Dialogs.register_value_picker("config/instant_kill", "Instant Kill", "One-shot kills for a duration (self only)", special_opts(
		"instant_kill", durations, lambda label, v: f"Set instant kill {'off' if v == 0 else f'for {label}'}"), back_dialog="config/personal")
	Dialogs.register_value_picker("config/infinite_ammo", "Infinite Ammo", "No reloads needed for a duration (self only)", special_opts(
		"infinite_ammo", durations, lambda label, v: f"Set infinite ammo {'off' if v == 0 else f'for {label}'}"), back_dialog="config/personal")
	Dialogs.register_value_picker("config/quick_reload", "Quick Reload", "Reduce reload time (self only)", special_opts(
		"quick_reload", percents, lambda label, _: f"Set quick reload to {label}"), back_dialog="config/personal")
	Dialogs.register_value_picker("config/quick_swap", "Quick Swap", "Reduce weapon-swap time (self only)", special_opts(
		"quick_swap", percents, lambda label, _: f"Set quick swap to {label}"), back_dialog="config/personal")

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

	write_function(f"{ns}:config", f"dialog show @s {Dialogs.dialog_ref('config')}")

