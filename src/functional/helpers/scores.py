""" The per-player `special.*` flags every mode writes, and the lines that declare and clear them. """
# Imports
from typing import ClassVar


# Classes
class SpecialScores:
	""" The per-player `special.*` flags every mode writes, and the lines that declare and clear them. """

	ALL: ClassVar[dict[str, str]] = {
		"instant_kill": r"Instant kill: duration in ticks (kills entities in one hit, except {ns}.no_instant_kill tagged)",
		"infinite_ammo": r"Infinite ammo: duration in ticks (don't consume ammo, set ammo to max capacity)",
		"double_points": r"Double points: duration in ticks (double points earned from kills/hits in zombies)",
		"quick_reload": r"Quick reload: percentage faster reload (20 = 20% faster, 50 = 50% faster)",
		"quick_swap": r"Quick swap: percentage faster weapon switch (20 = 20% faster, 50 = 50% faster)",
		"additional_shots": r"Additional shots: number of extra projectiles per shot (Double Tap perk)",
		"phd_flopper": r"PhD Flopper perk: immune to explosive self-damage (fall damage handled by attribute)",
		"deadshot": r"Deadshot Daiquiri perk: 65% weapon spread + recoil",
		"timeslip": r"Timeslip perk: faster traps / Mystery Box / Pack-a-Punch for the owner",
		"electric_cherry": r"Electric Cherry perk: reload discharges a shock that damages/stuns nearby zombies",
		"widows_wine": r"Widow's Wine perk: web grenades + web-on-hurt passive + stronger knife",
		"juggernaut": r"Multiplayer loadout perk flags, set on loadout apply",
		"scavenger": r"",
		"flak_jacket": r"",
		"tracker": r"",
		"tactical_mask": r"",
		"overkill": r"",
		"quick_fix": r"",
	}
	""" Per-player "special" flags and timers, mapping objective suffix to its documentation comment.

	Several unrelated systems write these: multiplayer and missions loadout perks, zombies perks and power-ups, and the debug menu.
	Each one only ever clears what it sets, so a mode MUST wipe the whole set when its game starts.
	Otherwise Quick Reload bought as a multiplayer perk is still active when the next zombies game begins.
	"""

	@staticmethod
	def special_objectives_lines(ns: str) -> str:
		""" Return the `scoreboard objectives add` block for every special score, with its comment. """
		parts: list[str] = []
		for name, comment in SpecialScores.ALL.items():
			if comment:
				parts.append(f"# {comment.format(ns=ns)}")
			parts.append(f"scoreboard objectives add {ns}.special.{name} dummy")
		return "\n".join(parts)

	@staticmethod
	def reset_special_scores_lines(ns: str, selector: str) -> str:
		""" Return the lines zeroing every special score for `selector` (clean slate on game start). """
		return "\n".join(f"scoreboard players set {selector} {ns}.special.{name} 0" for name in SpecialScores.ALL)

