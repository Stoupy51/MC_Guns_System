""" The Multiplayer branch: five chains of ten and one event challenge, 7,200 XP into the `mp` pool.

Every counter here rides an award function that already exists, so nothing in `multiplayer/` is touched
except the one `advancement grant` for `flawless`.

`level` is the odd one: it reads `mgs.mp.xp_level` directly instead of mirroring it into a counter of its
own. The score is already permanent and already the number the challenge is about.

Ten rows per chain is a shape rather than a coincidence. Four-row chains stacked sixteen deep made the
advancement screen a tall thin column; ten across turns it into something you read left to right. Rows
carry only their threshold, payout and name, and take the description, icon and frame from the chain.
"""
# Imports
from ..model import Branch, Chain, EventChallenge, Stat, StatKind, Tier

# Constants
MP_BRANCH: Branch = Branch(
	key="mp",
	side="mp",
	title="Multiplayer",
	description="Challenges across every competitive gamemode",
	icon="m4a1",
)
""" Multiplayer sub-root. """

MP_CHAINS: tuple[Chain, ...] = (
	Chain(
		key="kills",
		branch="mp",
		icon="m4a1",
		description="Kill {count} players",
		stat=Stat(
			objective="mgs.adv.mp.kills",
			kind=StatKind.COUNT_ONE,
			sources=("kill",),
			unit="1 kill",
			note="Every kill in every gamemode, from the shared on_kill listener",
		),
		tiers=(
			Tier(threshold=25,    xp=10,  title="First Blood",   icon="makarov", description="Kill 25 players"),
			Tier(threshold=50,    xp=20,  title="Contact",       icon="m1911"),
			Tier(threshold=100,   xp=30,  title="Trigger Time",  icon="deagle"),
			Tier(threshold=250,   xp=50,  title="Regular",       icon="vz61"),
			Tier(threshold=500,   xp=75,  title="Seasoned",      icon="mp5"),
			Tier(threshold=1000,  xp=110, title="Hardened",      icon="mp7"),
			Tier(threshold=2000,  xp=160, title="Veteran",       icon="famas"),
			Tier(threshold=3500,  xp=230, title="Elite",         icon="m4a1"),
			Tier(threshold=6000,  xp=275, title="Relentless",    icon="rpk"),
			Tier(threshold=10000, xp=340, title="War Machine",   icon="m249"),
		),
	),
	Chain(
		key="headshots",
		branch="mp",
		icon="m82",
		description="Land {count} headshot kills",
		stat=Stat(
			objective="mgs.adv.mp.headshots",
			kind=StatKind.COUNT_ONE,
			sources=("headshot",),
			unit="1 headshot kill",
			note="The bonus award, which only fires on top of a kill, so this counts headshot KILLS",
		),
		tiers=(
			Tier(threshold=10,   xp=10,  title="Lucky Shot",         icon="m9",     description="Land 10 headshot kills"),
			Tier(threshold=25,   xp=20,  title="Steady Hands",       icon="glock17"),
			Tier(threshold=50,   xp=30,  title="Eyes Up",            icon="mp7"),
			Tier(threshold=100,  xp=50,  title="Clean Aim",          icon="aug"),
			Tier(threshold=250,  xp=75,  title="Marksman",           icon="g3a3"),
			Tier(threshold=500,  xp=110, title="Deadeye",            icon="m16a4"),
			Tier(threshold=1000, xp=160, title="Headhunter",         icon="m24"),
			Tier(threshold=1750, xp=230, title="Cold Precision",     icon="mosin"),
			Tier(threshold=3000, xp=275, title="Surgical",           icon="svd"),
			Tier(threshold=5000, xp=340, title="One Shot, One Kill", icon="m82"),
		),
	),
	Chain(
		key="objectives",
		branch="mp",
		icon="minecraft:beacon",
		description="Complete {count} objective plays",
		stat=Stat(
			objective="mgs.adv.mp.objectives",
			kind=StatKind.COUNT_ONE,
			sources=("dom_capture", "hp_capture", "bomb_plant", "bomb_defuse", "site_destroyed"),
			unit="1 objective play",
			note="Zone taken, hill held first, bomb planted or defused, site destroyed. The five awards that mean somebody played the mode instead of the scoreboard",
		),
		tiers=(
			Tier(threshold=5,    xp=10,  title="Doing Your Bit",        icon="minecraft:white_banner", description="Complete 5 objective plays"),
			Tier(threshold=10,   xp=20,  title="Playing The Objective", icon="minecraft:light_gray_banner"),
			Tier(threshold=25,   xp=30,  title="Useful",                icon="minecraft:blue_banner"),
			Tier(threshold=50,   xp=50,  title="Team Player",           icon="minecraft:cyan_banner"),
			Tier(threshold=100,  xp=75,  title="Carrying",              icon="minecraft:green_banner"),
			Tier(threshold=200,  xp=110, title="Point Runner",          icon="minecraft:lime_banner"),
			Tier(threshold=350,  xp=160, title="Flag Bearer",           icon="minecraft:yellow_banner"),
			Tier(threshold=600,  xp=230, title="Objective Machine",     icon="minecraft:orange_banner"),
			Tier(threshold=1000, xp=275, title="Backbone",              icon="minecraft:red_banner"),
			Tier(threshold=1500, xp=340, title="The Whole Reason",      icon="minecraft:beacon"),
		),
	),
	Chain(
		key="wins",
		branch="mp",
		icon="minecraft:golden_apple",
		description="Win {count} matches",
		stat=Stat(
			objective="mgs.adv.mp.wins",
			kind=StatKind.COUNT_ONE,
			sources=("match_win",),
			unit="1 match won",
			note="Match wins only. The losing side's award is deliberately not counted here",
		),
		tiers=(
			Tier(threshold=1,   xp=10,  title="On The Board",   icon="minecraft:leather_helmet", description="Win a match"),
			Tier(threshold=3,   xp=20,  title="Winning Habit",  icon="minecraft:chainmail_helmet"),
			Tier(threshold=5,   xp=30,  title="Victor",         icon="minecraft:iron_helmet"),
			Tier(threshold=10,  xp=50,  title="Reliable",       icon="minecraft:golden_helmet"),
			Tier(threshold=20,  xp=75,  title="Contender",      icon="minecraft:diamond_helmet"),
			Tier(threshold=35,  xp=110, title="Favourite",      icon="minecraft:netherite_helmet"),
			Tier(threshold=50,  xp=160, title="Dominant",       icon="minecraft:golden_apple"),
			Tier(threshold=75,  xp=230, title="Feared",         icon="minecraft:enchanted_golden_apple"),
			Tier(threshold=100, xp=275, title="Champion",       icon="minecraft:totem_of_undying"),
			Tier(threshold=150, xp=340, title="Undisputed",     icon="minecraft:nether_star"),
		),
	),
	Chain(
		key="level",
		branch="mp",
		icon="minecraft:gold_ingot",
		description="Reach Multiplayer level {count}",
		stat=Stat(
			objective="mgs.mp.xp_level",
			owned=False,
			unit="1 level",
			note="Borrowed from the curve. Permanent already, so mirroring it into a counter would be a second copy to keep in sync",
		),
		tiers=(
			Tier(threshold=10,  xp=15,  title="Rank 10",  icon="minecraft:copper_ingot"),
			Tier(threshold=20,  xp=30,  title="Rank 20",  icon="minecraft:iron_nugget"),
			Tier(threshold=30,  xp=50,  title="Rank 30",  icon="minecraft:iron_ingot"),
			Tier(threshold=40,  xp=80,  title="Rank 40",  icon="minecraft:gold_nugget"),
			Tier(threshold=50,  xp=120, title="Rank 50",  icon="minecraft:gold_ingot"),
			Tier(threshold=75,  xp=175, title="Rank 75",  icon="minecraft:emerald"),
			Tier(threshold=100, xp=250, title="Rank 100", icon="minecraft:diamond"),
			Tier(threshold=125, xp=350, title="Rank 125", icon="minecraft:netherite_scrap"),
			Tier(threshold=150, xp=425, title="Rank 150", icon="minecraft:netherite_ingot"),
			Tier(threshold=200, xp=505, title="Rank 200", icon="minecraft:nether_star"),
		),
	),
)
""" Multiplayer chains, 50 tiers. """

MP_EVENTS: tuple[EventChallenge, ...] = (
	EventChallenge(
		key="flawless",
		branch="mp",
		xp=300,
		title="Flawless Victory",
		description="Win a match without dying once",
		icon="minecraft:shield",
		site="multiplayer/xp/on_game_end",
	),
)
""" Not expressible as a score: `mgs.mp.deaths` is per-match and is zeroed on join and on start, so it
reads 0 for almost everyone almost always. """
