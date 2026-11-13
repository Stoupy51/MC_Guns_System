""" What a save slot holds, as tables that both the capture and the restore iterate. """
# Imports
from dataclasses import dataclass

from ..machines.perks.definitions import PERK_DEFINITIONS


# Classes
@dataclass(frozen=True)
class SavedScore:
	""" A per-player objective, kept under `players[].scores.<key>`. """
	objective: str
	""" Without the namespace, e.g. `zb.points`. """
	key: str


@dataclass(frozen=True)
class SavedMapScore:
	""" A map element objective, kept as `map.<element>[] = {id, <key>}`, one entry per element entity. """
	element: str
	selector: str
	""" Selector arguments of the element entities, `{ns}` substituted. """
	id_objective: str
	""" The objective holding the map id the element was set up with, the same for the same element on every start. """
	objective: str
	key: str


# Constants
FORMAT: int = 1
""" Bumped when a slot written by this version cannot be read by the restore of the next one. """

PLAYER_SCORES: list[SavedScore] = [
	SavedScore(objective="zb.points", key="points"),
	SavedScore(objective="zb.kills", key="kills"),
	SavedScore(objective="zb.downs", key="downs"),
	SavedScore(objective="zb.passive", key="passive"),
	SavedScore(objective="zb.ability", key="ability"),
	SavedScore(objective="zb.ability_cd", key="ability_cd"),
	SavedScore(objective="zb.tactical_type", key="tactical_type"),
	SavedScore(objective="zb.lethal_type", key="lethal_type"),
	SavedScore(objective="zb.qr_uses", key="qr_uses"),
	SavedScore(objective="zb.dw_uses", key="dw_uses"),
	*(SavedScore(objective=f"zb.perk.{perk_id}", key=f"perk_{perk_id}") for perk_id in PERK_DEFINITIONS),
	*(SavedScore(objective=f"zb.perkpaid.{perk_id}", key=f"perkpaid_{perk_id}") for perk_id in PERK_DEFINITIONS),
]

MAP_SCORES: list[SavedMapScore] = [
	# Both sides of every door of a link group carry the group's chip-in progress.
	SavedMapScore(element="doors", selector="type=minecraft:interaction,tag={ns}.door", id_objective="zb.door.link", objective="zb.door.paid", key="paid"),
	SavedMapScore(element="barricades", selector="type=minecraft:block_display,tag={ns}.barricade_display", id_objective="zb.barricade.id", objective="zb.barricade.state", key="state"),
	SavedMapScore(element="traps", selector="type=minecraft:marker,tag={ns}.trap_center", id_objective="zb.trap.id", objective="zb.trap.cd", key="cd"),
]

