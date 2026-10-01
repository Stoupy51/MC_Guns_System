""" Pack-a-Punch resolution: max level, per-level stat overrides and display names. """
# Imports
from typing import cast

from stewbeet import JsonDict
from stouputils.typing import JsonList

from .keys import PAP_NAME, PAP_STATS


# Classes
class PapStats:
	""" Pap helpers. """

	# Functions
	@staticmethod
	def pap_stats(weapon_stats: JsonDict) -> JsonDict:
		""" The weapon's PAP overrides, empty when it has none. """
		stats: object = weapon_stats.get(PAP_STATS)
		return cast(JsonDict, stats) if isinstance(stats, dict) else {}

	@staticmethod
	def levels(value: object) -> JsonList:
		""" A PAP value as one entry per level: a scalar applies to every level, so it is a list of one. """
		return list(cast(JsonList, value)) if isinstance(value, (list, tuple)) else [value]

	@staticmethod
	def get_pap_max_level(weapon_stats: JsonDict) -> int:
		""" Return max PAP level based on the longest PAP stat list for this weapon. """
		return max((len(PapStats.levels(value)) for value in PapStats.pap_stats(weapon_stats).values()), default=0)

	@staticmethod
	def resolve_pap_overrides(weapon_stats: JsonDict, pap_level: int) -> JsonDict:
		""" Resolve PAP overrides for a given level.

		For list values, this clamps to the last value when pap_level exceeds list length.
		For scalar values, the same value is used at every PAP level.
		"""
		if pap_level <= 0:
			return {}
		resolved: JsonDict = {}
		for stat_key, value in PapStats.pap_stats(weapon_stats).items():
			values: JsonList = PapStats.levels(value)
			if values:
				resolved[stat_key] = values[min(pap_level - 1, len(values) - 1)]
		return resolved

	@staticmethod
	def resolve_pap_name(weapon_stats: JsonDict, pap_level: int, default_name: str) -> str:
		""" Resolve PAP display name for a given level.

		Reads PAP_STATS[PAP_NAME] as scalar or list and clamps list indexing to the last value.
		Falls back to default_name when PAP name is missing or invalid.
		"""
		if pap_level <= 0:
			return default_name
		names: JsonList = PapStats.levels(PapStats.pap_stats(weapon_stats).get(PAP_NAME))
		picked: object = names[min(pap_level - 1, len(names) - 1)] if names else None
		return picked if isinstance(picked, str) else default_name

