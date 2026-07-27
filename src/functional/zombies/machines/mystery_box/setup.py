""" Per-box state objectives, the default weapon pool and the give functions behind it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .....config.stats.keys import WEIGHT
from .....database.items import WEAPON_STATS
from ...common import ZombiesCommon
from .shared import MONKEY_BOMB_WEIGHT


# Functions
def write_mystery_box_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Per-box state objectives (each box is an independent pull, so multiple can spin at once)
	write_load_file(f"""
# Box id shared by a box's interaction entity and its active pull display
scoreboard objectives add {ns}.mb.box dummy
# Spin animation timer carried by each pull display (>0 spinning, <=0 ready window)
scoreboard objectives add {ns}.mb.anim dummy
# 1 when the buyer of this pull owns Timeslip (spin runs 2x faster for their display)
scoreboard objectives add {ns}.mb.timeslip dummy
# Whether this pull will end in a box move (teddy bear) — only the active box, never Fire Sale
scoreboard objectives add {ns}.mb.willmove dummy
# Stable per-player id, assigned lazily on first pull, so a pull display can record WHICH player
# bought it. During a Fire Sale one player can have several pulls running at once, so the buyer
# must be tracked per-display (mb.buyer below) — a single "which box am I buying" value on the
# player would be overwritten by the second pull and orphan the first box's collectible.
scoreboard objectives add {ns}.mb.pid dummy
# Buyer's pid, stamped on each pull display
scoreboard objectives add {ns}.mb.buyer dummy
""")

	# Teddy bear loot table for the move animation is shared (see zombies/roaming.py) and referenced below as mgs:zombies/roaming_bear.

	# Use common helper to build weapon->magazine mappings from catalogs
	weapon_mag_data: dict[str, tuple[str, int, bool]] = ZombiesCommon.build_weapon_magazine_data()
	default_pool_weapons: tuple[str, ...] = tuple(weapon_mag_data.keys())

	pool_entries: list[str] = []
	pool_weights: list[int] = []
	for weapon_id in default_pool_weapons:
		weight: int = WEAPON_STATS.get(weapon_id, {}).get("stats", {}).get(WEIGHT, 5)
		if weight == 0:
			continue  # Weight 0 = excluded from mystery box
		mag_id, mag_count, is_consumable = weapon_mag_data[weapon_id]
		pool_entries.append(
			f'{{weapon_id:"{weapon_id}",'
			f'give_function:"{ns}:v{version}/zombies/mystery_box/default_give/weapon",'
			f'magazine_id:"{mag_id}",'
			f'mag_count:{mag_count},'
			f'consumable:{"1b" if is_consumable else "0b"}}}'
		)
		pool_weights.append(weight)

	# Monkey Bomb: zombies-exclusive tactical (no magazine, given to hotbar.6 via the shared wallbuys/give_tactical — holding any monkeys counts as "owned" so duplicates reroll)
	pool_entries.append(
		f'{{weapon_id:"monkey_bomb",'
		f'give_function:"{ns}:v{version}/zombies/mystery_box/default_give/monkey_bomb",'
		f'magazine_id:"",'
		f'mag_count:0,'
		f'consumable:0b}}'
	)
	pool_weights.append(MONKEY_BOMB_WEIGHT)
	default_pool_entries: str = ",".join(pool_entries)
	default_pool_weights: str = ",".join(str(w) for w in pool_weights)

	## Default give for every pooled gun: the chosen pool entry already carries weapon_id/magazine_id/ mag_count/consumable, so this reads them back off mystery_box.result rather than one function per weapon restating the same literals.
	## Custom pools keep their own give_function.
	write_versioned_function("zombies/mystery_box/default_give/weapon", f"""
data modify storage {ns}:temp _wb_weapon set value {{}}
data modify storage {ns}:temp _wb_weapon.weapon_id set from storage {ns}:zombies mystery_box.result.weapon_id
data modify storage {ns}:temp _wb_weapon.name set from storage {ns}:zombies mystery_box.result.weapon_id
data modify storage {ns}:temp _wb_weapon.consumable set from storage {ns}:zombies mystery_box.result.consumable
data modify storage {ns}:temp _wb_weapon.magazine_id set from storage {ns}:zombies mystery_box.result.magazine_id
data modify storage {ns}:temp _wb_weapon.mag_count set from storage {ns}:zombies mystery_box.result.mag_count
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon
""")

	## Monkey Bomb give: routes to the tactical slot (hotbar.6) instead of the gun flow
	write_versioned_function("zombies/mystery_box/default_give/monkey_bomb", f"""
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/give_tactical {{weapon_id:"monkey_bomb"}}
""")

	write_versioned_function("zombies/mystery_box/ensure_default_pool", f"""
data modify storage {ns}:zombies mystery_box_pool set value [{default_pool_entries}]
data modify storage {ns}:zombies mystery_box_weights set value [{default_pool_weights}]
""")

