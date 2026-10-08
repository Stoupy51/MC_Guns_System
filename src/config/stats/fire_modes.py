""" Fire selector positions: which modes a weapon cycles through on drop, and what each one changes. """
# Imports
from dataclasses import asdict, dataclass
from typing import Literal

from stewbeet import JsonDict

from .keys import FIRE_MODE, FIRE_MODES


# Classes
@dataclass(frozen=True)
class FireMode:
	""" One position of a weapon's selector, with the values it replaces on that weapon. """
	name: Literal["auto", "semi", "burst", "pump"]
	cooldown: int | None = None
	""" Ticks between shots instead of the weapon's own. """
	pap_cooldown: int | None = None
	""" Same, once the weapon is Pack-a-Punched. """
	accuracy_sneak: int | None = None
	fire_sound: str | None = None
	""" Heard by the shooter only; other players keep the weapon's own `fire`. """
	pap_fire_sound: str | None = None
	burst: int | None = None
	""" Rounds fired per click. """
	burst_spacing: int | None = None
	""" Ticks between the rounds of a burst, the weapon's cooldown when None. """
	burst_pause: int | None = None
	""" Extra ticks after the last round of a burst. """

	def to_json(self) -> JsonDict:
		return {key: value for key, value in asdict(self).items() if value is not None}

	@staticmethod
	def stats(*modes: FireMode) -> JsonDict:
		""" Stat entries for a weapon whose selector cycles through `modes`, the first being the default.

		>>> FireMode.stats(AUTO, SEMI)
		{'fire_mode': 'auto', 'fire_modes': [{'name': 'auto'}, {'name': 'semi'}]}
		"""
		return {FIRE_MODE: modes[0].name, FIRE_MODES: [mode.to_json() for mode in modes]}

	@staticmethod
	def pap(*modes: FireMode) -> JsonDict:
		""" The same entries as a Pack-a-Punch override, whose list values are read one entry per level. """
		return {FIRE_MODE: modes[0].name, FIRE_MODES: [[mode.to_json() for mode in modes]]}


# Constants
AUTO: FireMode = FireMode(name="auto")
SEMI: FireMode = FireMode(name="semi")
PUMP: FireMode = FireMode(name="pump")

