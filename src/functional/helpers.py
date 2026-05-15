
# Shared utility functions for functional modules
import json
import re

from stewbeet import Mem, TextComponent, write_versioned_function

# [MGS] prefix as a nested list component (gold colored, lang-safe).
# Use in tellraw arrays: tellraw @s ["",{MGS_TAG},...]
# The brackets/space are raw strings (not matched by lang plugin).
# {"text":"MGS"} will be translated to {"translate":"mgs"} → value "MGS".
MGS_TAG: str = r'[{"text":"","color":"gold"},"[",{"text":"MGS"},"] "]'


def game_active_guard(ns: str, storage: str) -> str:
	""" Return the standard guard command for active games. """
	return f'execute unless data storage {ns}:{storage} game{{state:"active"}} run return fail'


def game_start_guards(ns: str, storage: str, mode_name: str) -> str:
	""" Return the 2-line guard for game start functions (active + preparing). """
	return f"""
execute if data storage {ns}:{storage} game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"{mode_name} already in progress!","color":"red"}}]
execute if data storage {ns}:{storage} game{{state:"preparing"}} run return run tellraw @s [{MGS_TAG},{{"text":"{mode_name} already preparing!","color":"red"}}]
""".strip()


def normalize_map_command_lines(ns: str, storage: str) -> str:
    """ Return the legacy respawn/start command normalization block for a map. """
    return f"""
execute unless data storage {ns}:{storage} game.map.respawn_commands if data storage {ns}:{storage} game.map.respawn_command[0] run data modify storage {ns}:{storage} game.map.respawn_commands set from storage {ns}:{storage} game.map.respawn_command
execute unless data storage {ns}:{storage} game.map.respawn_commands if data storage {ns}:{storage} game.map.respawn_command.command run data modify storage {ns}:{storage} game.map.respawn_commands set value []
execute unless data storage {ns}:{storage} game.map.respawn_commands[0] if data storage {ns}:{storage} game.map.respawn_command.command run data modify storage {ns}:{storage} game.map.respawn_commands append from storage {ns}:{storage} game.map.respawn_command
execute unless data storage {ns}:{storage} game.map.respawn_commands run data modify storage {ns}:{storage} game.map.respawn_commands set value []
execute unless data storage {ns}:{storage} game.map.start_commands run data modify storage {ns}:{storage} game.map.start_commands set value []
""".strip()  # noqa: E501


def schedule_preload_complete_line(ns: str, mode: str) -> str:
    """ Return the preload-complete schedule command for a mode. """
    version: str = Mem.ctx.project_version
    return f'schedule function {ns}:v{version}/{mode}/preload_complete 20t'


def prep_freeze_lines(ns: str, score_prefix: str, prepend: str = "", append: str = "") -> str:
    """ Return shared prep freeze/effects lines for a mode's in-game players. """
    selector: str = f'@a[scores={{{ns}.{score_prefix}.in_game=1}}]'
    parts: list[str] = [
        f'effect give {selector} darkness 25 255 true',
        f'effect give {selector} blindness 25 255 true',
        f'effect give {selector} night_vision 25 255 true',
        f'effect give {selector} saturation infinite 255 true',
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
        f'effect give {selector} saturation infinite 255 true',
    ]
    return "\n".join(parts)


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
) -> str:
    """ Return a mode late-join flow with hook points for mode-specific setup. """
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
    parts.extend([
        'effect give @s saturation infinite 255 true',
        f'# Enable class menu and show class selection\ntag @s add {ns}.give_class_menu\nfunction {ns}:v{version}/multiplayer/select_class',
        f'# Apply class if already chosen\nexecute unless score @s {ns}.mp.class matches 0 run function {ns}:v{version}/multiplayer/apply_class',
    ])
    if post_class_lines.strip():
        parts.append(post_class_lines.strip())
    parts.extend([
        f'# Teleport to spawn\nfunction {respawn_function}',
        f'# Call map join script (executed as the joining player)\nfunction {ns}:v{version}/shared/maps/call_join_script_at_base',
        f'# Announce\ntellraw @a ["",{{"selector":"@s","color":"{announce_color}"}},{{"text":" {announce_text}","color":"{announce_color}"}}]',
    ])
    return "\n\n".join(parts)


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
        parts.append(normalize_map_command_lines(ns, mode))
    parts.append(f'# Set state to preparing\ndata modify storage {ns}:{mode} game.state set value "preparing"')
    return "\n\n".join(parts)


def regen_enable_lines(ns: str) -> str:
	""" Lines to add at game start: disable natural regen, activate custom regen system. """
	return f"""
# Disable natural regeneration, enable custom regen system
gamerule natural_health_regeneration false
scoreboard players set #any_game_active {ns}.data 1

# Reset per-player regen state
scoreboard players set @a {ns}.last_hit 0
execute as @a run execute store result score @s {ns}.hp_prev run data get entity @s Health 1
""".strip()


def regen_disable_lines(ns: str) -> str:
	""" Lines to add at game stop: re-enable natural regen, deactivate custom regen system. """
	return f"""
# Re-enable natural regeneration, disable custom regen system
gamerule natural_health_regeneration true
scoreboard players set #any_game_active {ns}.data 0
""".strip()


def styled_text(text: str, **attrs: str) -> str:
    """ Create a styled text component, automatically splitting non-alphanumeric
    prefixes/suffixes into raw strings so the lang plugin only sees clean alpha text.

    Args:
        text    (str): The text to display (may contain leading/trailing emoji/symbols).
        **attrs (str): SNBT attributes like color, bold, italic.

    Returns:
        str: SNBT text component (single object or list with style inheritance).
    """
    # Check if text has non-alphanumeric content (besides spaces)
    m = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', text, re.DOTALL)
    prefix, alpha, suffix = m.groups() if m else ("", text, "")

    # Build attributes string for SNBT
    attr_str = ",".join(f'{k}:"{v}"' if v not in ("true", "false") else f'{k}:{v}' for k, v in attrs.items())

    if not prefix and not suffix:
        # Pure alphanumeric - single component
        return f'{{text:"{alpha}",{attr_str}}}' if attr_str else f'{{text:"{alpha}"}}'

    # Build list: base element with style, raw prefix, alpha text, raw suffix
    base = f'{{text:"",{attr_str}}}' if attr_str else '""'
    parts = [base]
    if prefix:
        parts.append(f'"{prefix}"')
    if alpha:
        parts.append(f'{{text:"{alpha}"}}')
    if suffix:
        parts.append(f'"{suffix}"')
    return f'[{",".join(parts)}]'


def btn(label: str, command: str, color: str = "yellow", hover: str = "", action: str = "suggest_command") -> str:
    """ Create a clickable button JSON component.

    Args:
        label     (str): The text to display on the button.
        command   (str): The command to run when the button is clicked.
        color     (str): The color of the button text.
        hover     (str): Optional tooltip text to show when hovering over the button.
        action    (str): The click event action type (default: "suggest_command").
    """
    obj: TextComponent = [
        {"text": "[", "color": color, "click_event": {"action": action, "command": command}},
        label,
        "]",
    ]
    if hover:
        obj[0]["hover_event"] = {"action": "show_text", "value": hover}
    return json.dumps(obj)


def write_shared_projectile_functions() -> None:
    """ Write shared mcfunctions used by both projectile and grenade systems. """
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    from ..config.stats import PROJECTILE_SPEED

    # Shared: Calculate velocity from look direction and apply to bs.vel, then teleport back
    # Requires: entity @s at summon position, data.config.PROJECTILE_SPEED set on entity
    # Uses raycast/accuracy/apply_spread for spread
    write_versioned_function("shared/calc_velocity", f"""
# Record current position for teleporting back later
execute store result score #proj_ox {ns}.data run data get entity @s Pos[0] 1000
execute store result score #proj_oy {ns}.data run data get entity @s Pos[1] 1000
execute store result score #proj_oz {ns}.data run data get entity @s Pos[2] 1000

# Apply accuracy spread to the rotation
tp @s ~ ~ ~ ~ ~
function {ns}:v{version}/raycast/accuracy/apply_spread

# Get direction vector by teleporting from origin
execute positioned 0.0 0.0 0.0 positioned ^ ^ ^1 run tp @s ~ ~ ~

# Read direction as velocity components (thousandths of a block)
execute store result score @s bs.vel.x run data get entity @s Pos[0] 1000
execute store result score @s bs.vel.y run data get entity @s Pos[1] 1000
execute store result score @s bs.vel.z run data get entity @s Pos[2] 1000

# Multiply direction by speed / 1000 to get velocity
execute store result score #proj_speed {ns}.data run data get entity @s data.config.{PROJECTILE_SPEED}
scoreboard players operation @s bs.vel.x *= #proj_speed {ns}.data
scoreboard players operation @s bs.vel.y *= #proj_speed {ns}.data
scoreboard players operation @s bs.vel.z *= #proj_speed {ns}.data
scoreboard players operation @s bs.vel.x /= #1000 {ns}.data
scoreboard players operation @s bs.vel.y /= #1000 {ns}.data
scoreboard players operation @s bs.vel.z /= #1000 {ns}.data

# Teleport back to original position
execute store result storage {ns}:temp _tp_pos.x double 0.001 run scoreboard players get #proj_ox {ns}.data
execute store result storage {ns}:temp _tp_pos.y double 0.001 run scoreboard players get #proj_oy {ns}.data
execute store result storage {ns}:temp _tp_pos.z double 0.001 run scoreboard players get #proj_oz {ns}.data
function {ns}:v{version}/shared/tp_back with storage {ns}:temp _tp_pos
""")

    # Shared: Teleport back to original position (macro)
    write_versioned_function("shared/tp_back",
"""
$tp @s $(x) $(y) $(z)
""")

