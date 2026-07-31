""" Every way a player earns XP, and what the message says when they do.

One table per side, and every balance number in the whole system lives here. Nothing else hard-codes an
amount, so retuning the pacing is a one-file edit followed by the admin recompute (see curve.py): the totals
players already banked are authoritative, and their levels are re-derived from them.

Each row carries its own suffix text because no award ever prints a message of its own — the amount is
appended to the message the event already broadcasts.
"""
# Imports
from dataclasses import dataclass

# Classes


@dataclass(frozen=True)
class XpAward:
	""" One way to earn XP.

	`amount` is 0 for the two awards that scale with the round number; those pass their value through
	`#xp_gain {ns}.data` instead and set `scaled=True`.

	Examples:
		>>> MP_AWARDS["kill"].suffix_text
		'+10 XP'
		>>> ZB_AWARDS["round_survived"].scaled
		True
	"""
	key: str
	""" Lookup name, used by the hook sites. """
	amount: int
	""" Flat XP for a plain award. For a `scaled` one it is the PER-UNIT rate the call site multiplies by
	(per zombie killed, per round cleared), and 0 where the rate lives in its own constant instead. """
	note: str
	""" What earns it, for whoever reads this table next. """
	scaled: bool = False
	""" The total comes from `#xp_gain` at runtime, because the call site is the only thing that knows how
	many units it is paying for. The suffix then reads that score instead of a compile-time number. """

	@property
	def suffix_text(self) -> str:
		""" The literal suffix appended to the event's own message.

		Returns:
			str: ex: "+10 XP", or "+XP" for a scaled award whose number is a score component.
		"""
		return "+XP" if self.scaled else f"+{self.amount} XP"


# Functions
def by_key(awards: list[XpAward]) -> dict[str, XpAward]:
	""" Index a table by its rows' keys.

	Args:
		awards (list[XpAward]): The rows to index.
	Returns:
		dict[str, XpAward]: Rows keyed by `XpAward.key`.

	Examples:
		>>> by_key([XpAward(key="a", amount=1, note="")])["a"].amount
		1
	"""
	return {award.key: award for award in awards}


# Constants
MP_AWARDS: dict[str, XpAward] = by_key([
	XpAward(key="kill",            amount=10, note="Any kill, every gamemode, via the on_kill signal"),
	XpAward(key="headshot",        amount=10, note="Added ON TOP of kill, so a headshot kill is worth double"),
	XpAward(key="dom_capture",     amount=20, note="Domination zone taken, to every contributor standing on it"),
	XpAward(key="dom_neutralize",  amount=5,  note="Domination zone dragged back to neutral, the halfway state"),
	XpAward(key="dom_hold",        amount=1,  note="Standing in a zone your team owns, once per 5s score tick"),
	XpAward(key="hp_capture",      amount=20, note="First hold of a Hardpoint hill after it rotates"),
	XpAward(key="hp_hold",         amount=1,  note="Standing in the active hill, once per 5s"),
	XpAward(key="bomb_pickup",     amount=2,  note="Picking the S&D bomb up off the ground; small on purpose"),
	XpAward(key="bomb_plant",      amount=20, note="S&D or Demolition plant, to whoever was channeling it"),
	XpAward(key="bomb_defuse",     amount=25, note="S&D or Demolition defuse; worth more than a plant, it is rarer"),
	XpAward(key="site_destroyed",  amount=20, note="A Demolition site actually going down, to the attackers in the blast"),
	XpAward(key="round_win",       amount=20, note="Winning an S&D or Demolition round"),
	XpAward(key="round_loss",      amount=5,  note="Losing one; never zero, so a losing side still progresses"),
	XpAward(key="match_win",       amount=50, note="Match win, to every player on the winning side"),
	XpAward(key="match_loss",      amount=20, note="Match loss or draw, to everyone who played it"),
])
""" Multiplayer awards. Tuned so a 20-kill win lands around 300-400 XP, which is ~2400 XP/hour.
A death is deliberately absent: XP never goes down. """

ZB_AWARDS: dict[str, XpAward] = by_key([
	XpAward(key="kill",            amount=2,  note="Per zombie, any kill type, via the totalKillCount delta", scaled=True),
	XpAward(key="headshot",        amount=2,  note="Added ON TOP of kill; raycast kills only, which is the only path that knows"),
	XpAward(key="points_spent",    amount=0,  note="One XP per POINTS_PER_XP spent, remainder carried", scaled=True),
	XpAward(key="round_survived",  amount=0,  note="ROUND_XP x the round just cleared", scaled=True),
	XpAward(key="revive",          amount=10, note="Getting a teammate back on their feet"),
	XpAward(key="perk",            amount=5,  note="Any perk acquired, bought or from a power-up"),
	XpAward(key="pack_a_punch",    amount=10, note="Upgrading a weapon"),
	XpAward(key="power",           amount=10, note="Flipping the power switch; one-off, and the whole team earns it"),
	XpAward(key="door",            amount=3,  note="Opening a door or clearing debris"),
	XpAward(key="powerup",         amount=3,  note="Picking up any power-up"),
	XpAward(key="mystery_box",     amount=3,  note="Collecting a weapon off the box"),
	XpAward(key="trap",            amount=2,  note="Activating a trap"),
	XpAward(key="barricade",       amount=1,  note="Repairing a barricade; already capped at 25 repairs per round"),
	XpAward(key="game_over",       amount=0,  note="GAME_OVER_XP x the final round", scaled=True),
])
""" Zombies awards. Tuned so a round-20 run lands around 1580 XP over ~45 minutes, which is ~2100 XP/hour —
close enough to multiplayer that neither side is the obvious grind. """

POINTS_PER_XP: int = 100
""" Zombies points spent per 1 XP. Spending is a secondary stream (~11% of a run's total), not a main one:
you already earned XP for the kills that produced those points, so this only rewards putting them to use. """
ROUND_XP: int = 2
""" XP per round cleared, multiplied by the round number. Quadratic in the total, which is what makes a deep
run worth pushing: rounds 1-20 come to 420 XP, rounds 1-100 to 10,100. """
GAME_OVER_XP: int = 5
""" XP per round reached, paid once when the run ends. Rewards going deep rather than farming early rounds. """
