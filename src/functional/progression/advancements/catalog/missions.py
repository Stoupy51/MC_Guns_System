""" The Missions branch: two chains of ten and one event challenge, 2,600 XP into the `mp` pool.

Both counters are fed from `missions/victory`, the point where the per-player numbers are final and
everyone who played is still on the roster. Missions has award functions of its own now (see
`missions/xp.py`), but neither of these two counts an award: one counts victories and the other reads the
mission's kill total in one go, so the victory function is still the right and only place for them.

Payouts go into the Multiplayer pool, which is the same pool `missions/xp.py` pays. Missions already runs
on the multiplayer side (`mp.class`, `mp.team`, `mp.default`, the multiplayer loadout and class
functions), and `progression/tick_player` shows the Multiplayer level everywhere outside a Zombies game,
so a missions player is looking at their Multiplayer bar while they play.
"""
# Imports
from ..model import Branch, Chain, EventChallenge, Stat, StatKind, Tier

# Constants
MI_BRANCH: Branch = Branch(
	key="mi",
	side="mp",
	title="Missions",
	description="Challenges for co-op missions. Pays Multiplayer XP",
	icon="minecraft:compass",
)
""" Missions sub-root. """

MI_CHAINS: tuple[Chain, ...] = (
	Chain(
		key="completed",
		branch="mi",
		icon="minecraft:filled_map",
		description="Complete {count} missions",
		stat=Stat(
			objective="mgs.adv.mi.completed",
			kind=StatKind.COUNT_ONE,
			unit="1 mission completed",
			note="Victories only. A mission that ends any other way pays nothing, which is what makes tier 1 worth having",
		),
		tiers=(
			Tier(threshold=1,   xp=10,  title="First Deployment", icon="minecraft:compass", description="Complete a mission"),
			Tier(threshold=3,   xp=20,  title="Second Tour",      icon="minecraft:map"),
			Tier(threshold=5,   xp=30,  title="Operator",         icon="minecraft:filled_map"),
			Tier(threshold=10,  xp=50,  title="Deployed",         icon="minecraft:lead"),
			Tier(threshold=20,  xp=75,  title="Specialist",       icon="minecraft:spyglass"),
			Tier(threshold=35,  xp=110, title="Team Leader",      icon="minecraft:golden_helmet"),
			Tier(threshold=50,  xp=160, title="Career Soldier",   icon="minecraft:iron_chestplate"),
			Tier(threshold=75,  xp=230, title="Hardened Command", icon="minecraft:diamond_chestplate"),
			Tier(threshold=100, xp=275, title="Legend Of The Op", icon="minecraft:netherite_chestplate"),
			Tier(threshold=150, xp=340, title="Never Off Duty",   icon="minecraft:nether_star"),
		),
	),
	Chain(
		key="kills",
		branch="mi",
		icon="scar17",
		description="Kill {count} enemies in missions",
		stat=Stat(
			objective="mgs.adv.mi.kills",
			kind=StatKind.COUNT_SCORE,
			source="@s mgs.mi.kills",
			unit="1 kill",
			note="Read off the per-mission score the victory function has just finished computing, so an aborted mission counts nothing",
		),
		tiers=(
			Tier(threshold=100,   xp=10,  title="Hostile Contact", icon="sten",   description="Kill 100 enemies in missions"),
			Tier(threshold=250,   xp=20,  title="Pushing Through", icon="ppsh41"),
			Tier(threshold=500,   xp=30,  title="Room Clearer",    icon="mac10"),
			Tier(threshold=1000,  xp=50,  title="Clearing House",  icon="ak47"),
			Tier(threshold=2000,  xp=75,  title="Heavy Contact",   icon="fnfal"),
			Tier(threshold=3500,  xp=110, title="Overwhelming",    icon="aug"),
			Tier(threshold=6000,  xp=160, title="Spearhead",       icon="scar17"),
			Tier(threshold=10000, xp=230, title="Force Of Nature", icon="g3a3"),
			Tier(threshold=20000, xp=275, title="One Man Army",    icon="rpk"),
			Tier(threshold=35000, xp=340, title="Total War",       icon="rpg7"),
		),
	),
)
""" Missions chains, 20 tiers. """

MI_EVENTS: tuple[EventChallenge, ...] = (
	EventChallenge(
		key="flawless",
		branch="mi",
		xp=300,
		title="No Casualties",
		description="Complete a mission without dying once",
		icon="minecraft:totem_of_undying",
		site="missions/victory",
	),
)
""" Not expressible as a score: `mgs.mi.deaths` is zeroed for everyone at mission start, so outside the
instant of a victory it reads 0 whether or not anybody earned it. """
