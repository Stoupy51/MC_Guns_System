""" Melee stat table: the starting knife and the three Black Ops 2 knife upgrades.

Zombies treats every entry here as a `kind 1` wallbuy (see zombies/objects/wallbuys): buying one
replaces `hotbar.0`, so a player only ever carries a single melee weapon.
"""
# Imports
from dataclasses import dataclass

# Constants
BO_TO_MC_DAMAGE: float = 2 / 15
""" Black Ops damage -> Minecraft damage, the same 2/15 ratio the zombie HP curve is built on. """


# Classes
@dataclass(frozen=True)
class Melee:
	""" One melee weapon, converted from its Black Ops damage so the HP curve stays comparable.

	Examples:
		>>> Melee(item_id="bowie_knife", display_name="Bowie Knife", name_color="gold", bo_damage=1150).damage
		153
		>>> Melee(item_id="combat_knife", display_name="Knife", name_color="white", bo_damage=150).damage
		20
	"""
	item_id: str
	display_name: str
	name_color: str
	bo_damage: int
	one_hit_until: int | None = None
	rarity: str = "common"
	movement_bonus: float = 0.1
	attack_speed: float = -2.5

	@property
	def damage(self) -> int:
		""" Black Ops damage converted to Minecraft attack damage. """
		return round(self.bo_damage * BO_TO_MC_DAMAGE)


# Constants
MELEE_WEAPONS: list[Melee] = [
	Melee(item_id="combat_knife",  display_name="Knife",         name_color="white", bo_damage=150),
	Melee(item_id="bowie_knife",   display_name="Bowie Knife",   name_color="gold",  bo_damage=1150, one_hit_until=11, rarity="rare"),
	Melee(item_id="sickle",        display_name="Sickle",        name_color="gold",  bo_damage=1150, one_hit_until=11, rarity="rare"),
	Melee(item_id="galvaknuckles", display_name="Galvaknuckles", name_color="aqua",  bo_damage=1600, one_hit_until=15, rarity="epic"),
]
""" The Sickle is a straight Bowie Knife reskin in Black Ops 2, so it shares its damage exactly.
Galvaknuckles sit one tier up: 1600 is the value that one-hits through round 14 on the Black Ops curve.
"""
