""" The Zombies branch: nine chains of ten and one event challenge, 13,100 XP into the `zb` pool.

Two counters are not worth one per event and say so. `kills` reads `#zb_kills_delta`, the same score the
kill award multiplies for its XP, so a Nuke moves the counter by the number of zombies it actually
killed. `spending` reads `#xp_gain`, which the spend tracker has already divided by `POINTS_PER_XP`, so
one unit of that counter is 100 points and the descriptions say points rather than units.

`best_round` is a high-water mark rather than a count, fed from the round-end tag. `level` borrows
`mgs.zb.xp_level` and needs no feed at all.
"""
# Imports
from ..model import Branch, Chain, EventChallenge, Stat, StatKind, Tier

# Constants
ZB_BRANCH: Branch = Branch(
	key="zb",
	side="zb",
	title="Zombies",
	description="Challenges for the undead survival mode",
	icon="ray_gun",
)
""" Zombies sub-root. """

SOLO_ROUND: int = 20
""" Round the solo challenge asks for. Lives here next to the challenge it describes, so the round-end
listener and the description can never drift apart. """

ZB_CHAINS: tuple[Chain, ...] = (
	Chain(
		key="kills",
		branch="zb",
		icon="ray_gun",
		description="Kill {count} zombies",
		stat=Stat(
			objective="mgs.adv.zb.kills",
			kind=StatKind.COUNT_SCORE,
			sources=("kill",),
			source="#zb_kills_delta mgs.data",
			unit="1 zombie",
			note="The same delta the points economy pays for, so gun, knife, trap and Nuke kills all count",
		),
		tiers=(
			Tier(threshold=100,   xp=10,  title="Undead Cleanup",  icon="minecraft:rotten_flesh", description="Kill 100 zombies"),
			Tier(threshold=250,   xp=20,  title="Holding The Line", icon="m590"),
			Tier(threshold=500,   xp=30,  title="Culling",          icon="spas12"),
			Tier(threshold=1000,  xp=50,  title="Exterminator",     icon="m500"),
			Tier(threshold=2500,  xp=75,  title="Meat Grinder",     icon="ppsh41"),
			Tier(threshold=5000,  xp=110, title="Horde Breaker",    icon="mac10"),
			Tier(threshold=10000, xp=160, title="Thinning Them Out", icon="ak47"),
			Tier(threshold=20000, xp=230, title="Body Count",       icon="rpk"),
			Tier(threshold=35000, xp=275, title="Ocean Of Bodies",  icon="m249"),
			Tier(threshold=50000, xp=340, title="Undertaker",       icon="ray_gun"),
		),
	),
	Chain(
		key="headshots",
		branch="zb",
		icon="m82",
		description="Land {count} headshot kills",
		stat=Stat(
			objective="mgs.adv.zb.headshots",
			kind=StatKind.COUNT_ONE,
			sources=("headshot",),
			unit="1 headshot kill",
			note="Raycast kills only, which is the only path that knows where the bullet landed",
		),
		tiers=(
			Tier(threshold=50,    xp=10,  title="Aim For The Head",     icon="minecraft:skeleton_skull", description="Land 50 headshot kills"),
			Tier(threshold=100,   xp=20,  title="Skull Cracker",        icon="minecraft:zombie_head"),
			Tier(threshold=250,   xp=30,  title="Steady Under Fire",    icon="glock18"),
			Tier(threshold=500,   xp=50,  title="Cranial Specialist",   icon="vz61"),
			Tier(threshold=1000,  xp=75,  title="Clean Work",           icon="m16a4"),
			Tier(threshold=2000,  xp=110, title="Double Tap Certified", icon="aug"),
			Tier(threshold=3500,  xp=160, title="Precision Rot",        icon="m24"),
			Tier(threshold=6000,  xp=230, title="Nothing Wasted",       icon="mosin"),
			Tier(threshold=10000, xp=275, title="Surgical Undertaking", icon="svd"),
			Tier(threshold=15000, xp=340, title="Ten Thousand Skulls",  icon="m82"),
		),
	),
	Chain(
		key="best_round",
		branch="zb",
		icon="minecraft:totem_of_undying",
		description="Clear round {count}",
		stat=Stat(
			objective="mgs.adv.zb.best_round",
			kind=StatKind.MAX_SCORE,
			source="#adv_round mgs.data",
			unit="1 round",
			note="Deepest round ever cleared. A max rather than a count, so a short game never drags it back down",
		),
		tiers=(
			Tier(threshold=5,  xp=15,  title="Round 5",  icon="minecraft:wooden_sword"),
			Tier(threshold=10, xp=30,  title="Round 10", icon="minecraft:clock"),
			Tier(threshold=15, xp=50,  title="Round 15", icon="minecraft:cooked_beef"),
			Tier(threshold=20, xp=80,  title="Round 20", icon="minecraft:golden_carrot"),
			Tier(threshold=25, xp=120, title="Round 25", icon="minecraft:lantern"),
			Tier(threshold=30, xp=175, title="Round 30", icon="minecraft:totem_of_undying"),
			Tier(threshold=35, xp=250, title="Round 35", icon="minecraft:blaze_powder"),
			Tier(threshold=40, xp=350, title="Round 40", icon="minecraft:ghast_tear"),
			Tier(threshold=50, xp=425, title="Round 50", icon="minecraft:dragon_head"),
			Tier(threshold=60, xp=505, title="Round 60", icon="minecraft:dragon_egg"),
		),
	),
	Chain(
		key="revives",
		branch="zb",
		icon="minecraft:totem_of_undying",
		description="Revive {count} teammates",
		stat=Stat(
			objective="mgs.adv.zb.revives",
			kind=StatKind.COUNT_ONE,
			sources=("revive",),
			unit="1 teammate revived",
			note="Getting a teammate back on their feet, not being revived yourself",
		),
		tiers=(
			Tier(threshold=1,   xp=10,  title="Get Up",            icon="minecraft:red_bed", description="Revive a teammate"),
			Tier(threshold=3,   xp=20,  title="Good Hands",        icon="minecraft:white_bed"),
			Tier(threshold=5,   xp=30,  title="Corpsman",          icon="minecraft:leather_boots"),
			Tier(threshold=10,  xp=50,  title="Field Medic",       icon="minecraft:golden_apple"),
			Tier(threshold=20,  xp=75,  title="Guardian Angel",    icon="minecraft:feather"),
			Tier(threshold=35,  xp=110, title="Always There",      icon="minecraft:glowstone_dust"),
			Tier(threshold=50,  xp=160, title="Lifeline",          icon="minecraft:glistering_melon_slice"),
			Tier(threshold=75,  xp=230, title="Nobody Dies Today", icon="minecraft:enchanted_golden_apple"),
			Tier(threshold=100, xp=275, title="Second Chances",    icon="minecraft:beacon"),
			Tier(threshold=150, xp=340, title="Death Denied",      icon="minecraft:totem_of_undying"),
		),
	),
	Chain(
		key="perks",
		branch="zb",
		icon="minecraft:milk_bucket",
		description="Acquire {count} perks",
		stat=Stat(
			objective="mgs.adv.zb.perks",
			kind=StatKind.COUNT_ONE,
			sources=("perk",),
			unit="1 perk",
			note="Any perk acquired, bought or from a power-up",
		),
		tiers=(
			Tier(threshold=5,   xp=10,  title="Taste Test",     icon="minecraft:glass_bottle"),
			Tier(threshold=10,  xp=20,  title="Acquired Taste", icon="minecraft:potion"),
			Tier(threshold=25,  xp=30,  title="Regular Round",  icon="minecraft:splash_potion"),
			Tier(threshold=50,  xp=50,  title="Perkaholic",     icon="minecraft:honey_bottle"),
			Tier(threshold=75,  xp=75,  title="Well Stocked",   icon="minecraft:brewing_stand"),
			Tier(threshold=100, xp=110, title="Liquid Courage", icon="minecraft:cauldron"),
			Tier(threshold=150, xp=160, title="Liquid Diet",    icon="minecraft:milk_bucket"),
			Tier(threshold=200, xp=230, title="Fully Loaded",   icon="minecraft:lingering_potion"),
			Tier(threshold=300, xp=275, title="Better Living",  icon="minecraft:dragon_breath"),
			Tier(threshold=500, xp=340, title="Chemically Bound", icon="minecraft:experience_bottle"),
		),
	),
	Chain(
		key="pack_a_punch",
		branch="zb",
		icon="minecraft:enchanted_book",
		description="Upgrade {count} weapons",
		stat=Stat(
			objective="mgs.adv.zb.pap",
			kind=StatKind.COUNT_ONE,
			sources=("pack_a_punch",),
			unit="1 weapon upgraded",
			note="Every trip to the machine counts, including re-packing the same weapon",
		),
		tiers=(
			Tier(threshold=1,   xp=10,  title="Packed",          icon="minecraft:anvil", description="Upgrade a weapon"),
			Tier(threshold=3,   xp=20,  title="Back For More",   icon="minecraft:chipped_anvil"),
			Tier(threshold=5,   xp=30,  title="Tooled Up",       icon="minecraft:damaged_anvil"),
			Tier(threshold=10,  xp=50,  title="Upgrade Addict",  icon="minecraft:enchanting_table"),
			Tier(threshold=20,  xp=75,  title="Machine Regular", icon="minecraft:lapis_lazuli"),
			Tier(threshold=35,  xp=110, title="Overclocked",     icon="minecraft:redstone_block"),
			Tier(threshold=50,  xp=160, title="Fully Packed",    icon="minecraft:enchanted_book"),
			Tier(threshold=75,  xp=230, title="Nothing Stock",   icon="minecraft:netherite_scrap"),
			Tier(threshold=100, xp=275, title="Hundred Punches", icon="minecraft:netherite_ingot"),
			Tier(threshold=150, xp=340, title="Beyond Upgraded", icon="minecraft:nether_star"),
		),
	),
	Chain(
		key="box",
		branch="zb",
		icon="minecraft:ender_chest",
		description="Collect {count} weapons from the box",
		stat=Stat(
			objective="mgs.adv.zb.box",
			kind=StatKind.COUNT_ONE,
			sources=("mystery_box",),
			unit="1 weapon collected",
			note="Weapons actually taken off the box, not rolls paid for",
		),
		tiers=(
			Tier(threshold=1,   xp=10,  title="First Roll",           icon="minecraft:chest", description="Collect a weapon from the box"),
			Tier(threshold=5,   xp=20,  title="Rolling The Box",      icon="minecraft:trapped_chest"),
			Tier(threshold=10,  xp=30,  title="Feeling Lucky",        icon="minecraft:barrel"),
			Tier(threshold=25,  xp=50,  title="Box Addict",           icon="minecraft:ender_chest"),
			Tier(threshold=50,  xp=75,  title="Points Well Spent",    icon="minecraft:gold_nugget"),
			Tier(threshold=75,  xp=110, title="Gambler",              icon="minecraft:emerald"),
			Tier(threshold=100, xp=160, title="Teddy Bear Collector", icon="minecraft:white_wool"),
			Tier(threshold=200, xp=230, title="Box Is Home",          icon="minecraft:shulker_box"),
			Tier(threshold=300, xp=275, title="Ray Gun Eventually",   icon="ray_gun"),
			Tier(threshold=500, xp=340, title="The House Always Pays", icon="minecraft:nether_star"),
		),
	),
	Chain(
		key="spending",
		branch="zb",
		icon="minecraft:gold_block",
		description="Spend points in Zombies",
		stat=Stat(
			objective="mgs.adv.zb.spending",
			kind=StatKind.COUNT_SCORE,
			sources=("points_spent",),
			source="#xp_gain mgs.data",
			unit="100 points",
			note="One unit per 100 points, because the spend tracker has already divided by POINTS_PER_XP. Every description spells the real point total out",
		),
		tiers=(
			Tier(threshold=100,   xp=10,  title="Opening Doors",      icon="minecraft:iron_nugget",  description="Spend 10,000 points"),
			Tier(threshold=250,   xp=20,  title="Paying The Rent",    icon="minecraft:gold_nugget",  description="Spend 25,000 points"),
			Tier(threshold=500,   xp=30,  title="Big Spender",        icon="minecraft:iron_ingot",   description="Spend 50,000 points"),
			Tier(threshold=1000,  xp=50,  title="Loose Wallet",       icon="minecraft:gold_ingot",   description="Spend 100,000 points"),
			Tier(threshold=2000,  xp=75,  title="Burning Through It", icon="minecraft:emerald",      description="Spend 200,000 points"),
			Tier(threshold=3500,  xp=110, title="Economy Ruined",     icon="minecraft:diamond",      description="Spend 350,000 points"),
			Tier(threshold=6000,  xp=160, title="Nothing Saved",      icon="minecraft:emerald_block", description="Spend 600,000 points"),
			Tier(threshold=10000, xp=230, title="Money Is No Object", icon="minecraft:gold_block",   description="Spend 1,000,000 points"),
			Tier(threshold=20000, xp=275, title="Points Are Fake",    icon="minecraft:diamond_block", description="Spend 2,000,000 points"),
			Tier(threshold=35000, xp=340, title="Bottomless Pockets", icon="minecraft:netherite_block", description="Spend 3,500,000 points"),
		),
	),
	Chain(
		key="level",
		branch="zb",
		icon="minecraft:gold_ingot",
		description="Reach Zombies level {count}",
		stat=Stat(
			objective="mgs.zb.xp_level",
			owned=False,
			unit="1 level",
			note="Borrowed from the curve, same as the Multiplayer level chain",
		),
		tiers=(
			Tier(threshold=10,  xp=15,  title="Zombies Rank 10",  icon="minecraft:copper_ingot"),
			Tier(threshold=20,  xp=30,  title="Zombies Rank 20",  icon="minecraft:iron_nugget"),
			Tier(threshold=30,  xp=50,  title="Zombies Rank 30",  icon="minecraft:iron_ingot"),
			Tier(threshold=40,  xp=80,  title="Zombies Rank 40",  icon="minecraft:gold_nugget"),
			Tier(threshold=50,  xp=120, title="Zombies Rank 50",  icon="minecraft:gold_ingot"),
			Tier(threshold=75,  xp=175, title="Zombies Rank 75",  icon="minecraft:emerald"),
			Tier(threshold=100, xp=250, title="Zombies Rank 100", icon="minecraft:diamond"),
			Tier(threshold=125, xp=350, title="Zombies Rank 125", icon="minecraft:netherite_scrap"),
			Tier(threshold=150, xp=425, title="Zombies Rank 150", icon="minecraft:netherite_ingot"),
			Tier(threshold=200, xp=505, title="Zombies Rank 200", icon="minecraft:nether_star"),
		),
	),
)
""" Zombies chains, 90 tiers. """

ZB_EVENTS: tuple[EventChallenge, ...] = (
	EventChallenge(
		key="solo_run",
		branch="zb",
		xp=500,
		title="Alone In The Dark",
		description=f"Reach round {SOLO_ROUND} with nobody else in the game",
		icon="minecraft:soul_lantern",
		site="zombies/adv/on_round_end",
	),
)
""" Not expressible as a score: it needs the round number and the roster size at the same instant, and
the roster is a selector count rather than anything persistent. """
