""" Per-box state objectives, the default weapon pool and the give functions behind it. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .....config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from .....config.stats.keys import WEIGHT
from .....database.items import CONSUMABLE_MAGAZINES, WEAPON_STATS
from .shared import MONKEY_BOMB_WEIGHT


# Functions
def write_mystery_box_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Each box is an independent pull, so several can spin at once.
	write_load_file(f"""
# Shared by a box's interaction entity and its pull display.
scoreboard objectives add {ns}.mb.box dummy
# >0 spinning, <=0 ready window.
scoreboard objectives add {ns}.mb.anim dummy
# 1 when the buyer owns Timeslip (2x spin).
scoreboard objectives add {ns}.mb.timeslip dummy
# 1 when the pull ends in a box move (active box only, never during a Fire Sale).
scoreboard objectives add {ns}.mb.willmove dummy
# Stable player id, assigned on first pull. During a Fire Sale one player can run several pulls,
# so the buyer is stored per display (mb.buyer).
scoreboard objectives add {ns}.mb.pid dummy
scoreboard objectives add {ns}.mb.buyer dummy
""")

	# The move animation uses the shared teddy bear loot table (mgs:zombies/roaming_bear, see roaming).

	pool_entries: list[str] = []
	pool_weights: list[int] = []
	for weapon in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS):
		weight: int = WEAPON_STATS.get(weapon.item_id, {}).get("stats", {}).get(WEIGHT, 5)
		if weight == 0:
			continue  # Weight 0 = excluded from mystery box
		consumable: str = "1b" if weapon.magazine_id in CONSUMABLE_MAGAZINES else "0b"
		pool_entries.append(
			f'{{weapon_id:"{weapon.item_id}",'
			f'give_function:"{ns}:v{version}/zombies/mystery_box/default_give/weapon",'
			f'magazine_id:"{weapon.magazine_id}",'
			f'mag_count:{weapon.default_mag_count},'
			f'consumable:{consumable}}}'
		)
		pool_weights.append(weight)

	# Monkey Bomb: zombies-only tactical for hotbar.6 (wallbuys/give_tactical); holding any counts as owned, so duplicates re-roll.
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

	## The pool entry carries weapon_id, magazine_id, mag_count and consumable, so one give function serves every gun.
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

	## To the tactical slot (hotbar.6), not the gun flow.
	write_versioned_function("zombies/mystery_box/default_give/monkey_bomb", f"""
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/give_tactical {{weapon_id:"monkey_bomb"}}
""")

	write_versioned_function("zombies/mystery_box/ensure_default_pool", f"""
data modify storage {ns}:zombies mystery_box_pool set value [{default_pool_entries}]
data modify storage {ns}:zombies mystery_box_weights set value [{default_pool_weights}]
""")

