""" Command blocks every mode's start, prep and late-join flows are assembled from. """
# Imports
from stewbeet import Mem

from . import MGS_TAG
from .text import Text


# Classes
class GameLifecycle:
	""" Command blocks every mode's start, prep and late-join flows are assembled from. """

	# Functions
	@staticmethod
	def game_active_guard(ns: str, storage: str) -> str:
		""" Return the standard guard command for active games. """
		return f'execute unless data storage {ns}:{storage} game{{state:"active"}} run return fail'

	@staticmethod
	def game_start_guards(ns: str, storage: str, mode_name: str) -> str:
		""" Return the 2-line guard for game start functions (active + preparing). """
		return f"""
execute if data storage {ns}:{storage} game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"{mode_name} already in progress!","color":"red"}}]
execute if data storage {ns}:{storage} game{{state:"preparing"}} run return run tellraw @s [{MGS_TAG},{{"text":"{mode_name} already preparing!","color":"red"}}]
""".strip()

	@staticmethod
	def normalize_map_command_lines(ns: str, storage: str) -> str:
		""" Return the legacy respawn/start command normalization block for a map. """
		return f"""
execute unless data storage {ns}:{storage} game.map.respawn_commands if data storage {ns}:{storage} game.map.respawn_command[0] run data modify storage {ns}:{storage} game.map.respawn_commands set from storage {ns}:{storage} game.map.respawn_command
execute unless data storage {ns}:{storage} game.map.respawn_commands if data storage {ns}:{storage} game.map.respawn_command.command run data modify storage {ns}:{storage} game.map.respawn_commands set value []
execute unless data storage {ns}:{storage} game.map.respawn_commands[0] if data storage {ns}:{storage} game.map.respawn_command.command run data modify storage {ns}:{storage} game.map.respawn_commands append from storage {ns}:{storage} game.map.respawn_command
execute unless data storage {ns}:{storage} game.map.respawn_commands run data modify storage {ns}:{storage} game.map.respawn_commands set value []
execute unless data storage {ns}:{storage} game.map.start_commands run data modify storage {ns}:{storage} game.map.start_commands set value []
""".strip()  # noqa: E501

	@staticmethod
	def schedule_preload_complete_line(ns: str, mode: str) -> str:
		""" Return the preload-complete schedule command for a mode. """
		version: str = Mem.ctx.project_version
		return f'schedule function {ns}:v{version}/{mode}/preload_complete 20t'

	@staticmethod
	def prep_freeze_lines(ns: str, score_prefix: str, prepend: str = "", append: str = "") -> str:
		""" Return shared prep freeze/effects lines for a mode's in-game players. """
		selector: str = f'@a[scores={{{ns}.{score_prefix}.in_game=1}}]'
		parts: list[str] = [
			f'effect give {selector} darkness 25 255 true',
			f'effect give {selector} blindness 25 255 true',
			f'effect give {selector} night_vision 25 255 true',
		]
		if prepend:
			parts.append(prepend.strip())
		parts.extend([
			f'execute as {selector} run attribute @s minecraft:movement_speed base set 0',
			f'execute as {selector} run attribute @s minecraft:jump_strength base set 0',
		])
		if append:
			parts.append(append.strip())
		return "\n".join(parts)

	@staticmethod
	def end_prep_transition_lines(ns: str, storage: str, score_prefix: str) -> str:
		"""Return shared end-prep transition lines (guard, active state, restore, clear effects)."""
		selector: str = f'@a[scores={{{ns}.{score_prefix}.in_game=1}}]'
		parts: list[str] = [
			f'execute unless data storage {ns}:{storage} game{{state:"preparing"}} run return fail',
			f'data modify storage {ns}:{storage} game.state set value "active"',
			f'execute as {selector} run attribute @s minecraft:movement_speed base reset',
			f'execute as {selector} run attribute @s minecraft:jump_strength base reset',
			f'effect clear {selector} darkness',
			f'effect clear {selector} blindness',
			f'effect clear {selector} night_vision',
		]
		return "\n".join(parts)

	@staticmethod
	def late_join_flow_lines(
		ns: str,
		storage: str,
		in_game_objective: str,
		no_active_text: str,
		already_in_text: str,
		init_lines: str,
		respawn_function: str,
		announce_text: str,
		announce_color: str,
		*,
		allow_preparing: bool = False,
		setup_extra_lines: str = "",
		post_class_lines: str = "",
		class_menu_lines: str = "",
		xp_side: str = "mp",
	) -> str:
		""" Return a mode late-join flow with hook points for mode-specific setup.

		class_menu_lines: replaces the default multiplayer class/loadout selection block. Modes
		without loadouts (zombies gives a fixed knife + starting pistol) pass their own giving
		logic here so a late-joiner isn't prompted to pick a multiplayer class. """
		version: str = Mem.ctx.project_version
		preparing_guard: str = f' unless data storage {ns}:{storage} game{{state:"preparing"}}' if allow_preparing else ""
		guard_line: str = (
			f'execute unless data storage {ns}:{storage} game{{state:"active"}}{preparing_guard} '
			f'run return run tellraw @s [{MGS_TAG},{{"text":"{no_active_text}","color":"red"}}]'
		)
		double_join_guard: str = (
			f'execute if score @s {in_game_objective} matches 1 '
			f'run return run tellraw @s [{MGS_TAG},{{"text":"{already_in_text}","color":"red"}}]'
		)
		parts: list[str] = [
			f'# Require an active game\n{guard_line}',
			f'# Prevent double-joining\n{double_join_guard}',
			f'# Tag as in-game and reset stats\n{init_lines.strip()}',
			'# Setup player\ngamemode adventure @s',
		]
		if setup_extra_lines.strip():
			parts.append(setup_extra_lines.strip())
		parts.append(f'# Reset stamina so the stamina system re-inits this player at full (it owns the hunger bar)\nscoreboard players set @s {ns}.stam_seen 0')
		if class_menu_lines.strip():
			# Mode-specific loadout (e.g. zombies gives a fixed knife + pistol, no class prompt)
			parts.append(class_menu_lines.strip())
		else:
			parts.extend([
				f'# Enable class menu and show class selection\ntag @s add {ns}.give_class_menu\nfunction {ns}:v{version}/multiplayer/select_class',
				f'# Apply class if already chosen\nexecute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class',
			])
		if post_class_lines.strip():
			parts.append(post_class_lines.strip())
		parts.extend([
			f'# Teleport to spawn\nfunction {respawn_function}',
			f'# Call map join script (executed as the joining player)\nfunction {ns}:v{version}/shared/maps/call_script_at_base {{script:"join"}}',
			f'# Announce\ntellraw @a ["",{Text.player(ns, "@s", side=xp_side, color=announce_color)},{{"text":" {announce_text}","color":"{announce_color}"}}]',
		])
		return "\n\n".join(parts)

	@staticmethod
	def mode_start_map_bootstrap_lines(ns: str, mode: str, normalize_legacy: bool = False) -> str:
		""" Return the shared start bootstrap: selection check, load, copy, and preparing state. """
		parts: list[str] = []
		parts.append(f"""
# Check that a map is selected
execute if data storage {ns}:{mode} game{{map_id:""}} run return run tellraw @s [{MGS_TAG},{{"text":"No map selected! Use the setup menu to select a map.","color":"red"}}]

# Load the selected map
function {ns}:v{Mem.ctx.project_version}/{mode}/load_map_from_storage with storage {ns}:{mode} game
execute unless score #map_load_found {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"Map not found! Select a valid map.","color":"red"}}]

# Copy loaded map data into game state
data modify storage {ns}:{mode} game.map set from storage {ns}:temp map_load.result
""".strip())
		if normalize_legacy:
			parts.append(GameLifecycle.normalize_map_command_lines(ns, mode))
		parts.append(f'# Set state to preparing\ndata modify storage {ns}:{mode} game.state set value "preparing"')
		return "\n\n".join(parts)

	@staticmethod
	def regen_enable_lines(ns: str) -> str:
		""" Lines to add at game start: disable natural regen, activate custom regen system. """
		return f"""
# Disable natural regeneration, enable custom regen system
gamerule natural_health_regeneration false
scoreboard players set #any_game_active {ns}.data 1

# Reset per-player regen state (hp_prev seeded from the auto-updated health criterion; a player
# whose criterion score is still unset just misses this seed and syncs on their first health change)
scoreboard players set @a {ns}.last_hit 0
scoreboard players set @a {ns}.hp_prev 0
execute as @a run scoreboard players operation @s {ns}.hp_prev = @s {ns}.health

# Reset stamina state so every player re-inits to full on their next stamina tick (also covers late-joiners)
scoreboard players set @a {ns}.stam_seen 0
""".strip()

	@staticmethod
	def regen_disable_lines(ns: str) -> str:
		""" Lines to add at game stop: re-enable natural regen, deactivate custom regen system. """
		return f"""
# Re-enable natural regeneration, disable custom regen system
gamerule natural_health_regeneration true
scoreboard players set #any_game_active {ns}.data 0

# Tear down stamina state: stop any hunger drain and refill the bar so nobody is left winded
effect clear @a minecraft:hunger
effect give @a minecraft:saturation 5 20 true
scoreboard players set @a {ns}.stam_out 0
scoreboard players set @a {ns}.stam_seen 0
""".strip()

