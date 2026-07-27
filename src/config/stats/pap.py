""" Pack-a-Punch resolution: max level, per-level stat overrides and display names. """
# Imports
from typing import Any, cast

from stewbeet import JsonDict

from .keys import PAP_NAME, PAP_STATS


# Classes
class PapStats:
	""" Pap helpers. """

	# Functions
	# Constants
	@staticmethod
	def get_pap_max_level(weapon_stats: JsonDict) -> int:
		""" Return max PAP level based on the longest PAP stat list for this weapon. """
		pap_stats_any: Any = weapon_stats.get(PAP_STATS)
		if not isinstance(pap_stats_any, dict) or not pap_stats_any:
			return 0
		pap_stats = cast(dict[str, Any], pap_stats_any)

		max_level: int = 0
		for value in pap_stats.values():
			if isinstance(value, (list, tuple)):
				pap_values = cast(list[Any] | tuple[Any, ...], value)
				max_level = max(max_level, len(pap_values))
			else:
				max_level = max(max_level, 1)
		return max_level

	@staticmethod
	def resolve_pap_overrides(weapon_stats: JsonDict, pap_level: int) -> JsonDict:
		""" Resolve PAP overrides for a given level.

		For list values, this clamps to the last value when pap_level exceeds list length.
		For scalar values, the same value is used at every PAP level.
		"""
		pap_stats_any: Any = weapon_stats.get(PAP_STATS)
		if not isinstance(pap_stats_any, dict) or pap_level <= 0:
			return {}
		pap_stats = cast(dict[str, Any], pap_stats_any)

		resolved: JsonDict = {}
		value_index: int = pap_level - 1
		for stat_key, value in pap_stats.items():
			if isinstance(value, (list, tuple)):
				pap_values = cast(list[Any] | tuple[Any, ...], value)
				if not pap_values:
					continue
				resolved[stat_key] = pap_values[min(value_index, len(pap_values) - 1)]
			else:
				resolved[stat_key] = value
		return resolved

	@staticmethod
	def resolve_pap_name(weapon_stats: JsonDict, pap_level: int, default_name: str) -> str:
		""" Resolve PAP display name for a given level.

		Reads PAP_STATS[PAP_NAME] as scalar or list and clamps list indexing to the last value.
		Falls back to default_name when PAP name is missing or invalid.
		"""
		pap_stats_any: Any = weapon_stats.get(PAP_STATS)
		if not isinstance(pap_stats_any, dict) or pap_level <= 0:
			return default_name
		pap_stats = cast(dict[str, Any], pap_stats_any)

		pap_name: Any = pap_stats.get(PAP_NAME)
		if isinstance(pap_name, str):
			return pap_name
		if isinstance(pap_name, (list, tuple)):
			pap_names = cast(list[Any] | tuple[Any, ...], pap_name)
			if not pap_names:
				return default_name
			idx: int = min(pap_level - 1, len(pap_names) - 1)
			picked = pap_names[idx]
			return picked if isinstance(picked, str) else default_name
		return default_name

