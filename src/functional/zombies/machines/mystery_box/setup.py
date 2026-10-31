""" Per-box state objectives, the weapon catalog, the pool a game builds from it and the give of a result. """
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .....config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from .....config.stats.keys import WEIGHT
from .....database.items import CONSUMABLE_MAGAZINES, WEAPON_STATS
from .shared import MONKEY_BOMB_WEIGHT, RAY_GUN_DRY_PULLS


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

	## The catalog is the pack's own data, rewritten at each load; a pool names weapons from it by id.
	catalog: list[str] = []
	default_pool: list[str] = []
	for weapon in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS):
		weight: int = WEAPON_STATS.get(weapon.item_id, {}).get("stats", {}).get(WEIGHT, 1)
		consumable: str = "1b" if weapon.magazine_id in CONSUMABLE_MAGAZINES else "0b"
		catalog.append(f'{weapon.item_id}:{{weapon_id:"{weapon.item_id}",magazine_id:"{weapon.magazine_id}",mag_count:{weapon.default_mag_count},consumable:{consumable}}}')
		if weight:
			default_pool.append(f'{{weapon_id:"{weapon.item_id}",weight:{weight}}}')
	catalog.append('monkey_bomb:{weapon_id:"monkey_bomb"}')
	default_pool.append(f'{{weapon_id:"monkey_bomb",weight:{MONKEY_BOMB_WEIGHT}}}')
	write_load_file(f"""
data modify storage {ns}:zombies mystery_box_catalog set value {{{",".join(catalog)}}}
execute unless data storage {ns}:config zombies.mystery_box_pool run data modify storage {ns}:config zombies.mystery_box_pool set value [{",".join(default_pool)}]
""")

	## Run as the collecting player; the result carries the catalog entry.
	write_versioned_function("zombies/mystery_box/give_result", f"""
scoreboard players set #wb_price {ns}.data 0
execute if data storage {ns}:zombies mystery_box.result{{weapon_id:"monkey_bomb"}} run return run function {ns}:v{version}/zombies/wallbuys/give_tactical {{weapon_id:"monkey_bomb"}}

data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies mystery_box.result
data modify storage {ns}:temp _wb_weapon.name set from storage {ns}:zombies mystery_box.result.weapon_id
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon
""")

	## Built once per game, before `#mgs:zombies/register_mystery_box_item` appends to it: the map's own pool when it has one, the global one otherwise.
	## Weight 0 and ids missing from the catalog are left out.
	write_versioned_function("zombies/mystery_box/build_pool", f"""
data modify storage {ns}:zombies mystery_box_pool set value []
data modify storage {ns}:zombies mystery_box_weights set value []
scoreboard players set #mb_ray_index {ns}.data -1
data modify storage {ns}:temp _mb_src set from storage {ns}:config zombies.mystery_box_pool
execute if data storage {ns}:zombies game.map.mystery_box_pool run data modify storage {ns}:temp _mb_src set from storage {ns}:zombies game.map.mystery_box_pool
function {ns}:v{version}/zombies/mystery_box/build_pool_next
""")
	write_versioned_function("zombies/mystery_box/build_pool_next", f"""
execute unless data storage {ns}:temp _mb_src[0] run return 0

execute store result score #mb_w {ns}.data run data get storage {ns}:temp _mb_src[0].weight
execute if score #mb_w {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/build_pool_add with storage {ns}:temp _mb_src[0]

data remove storage {ns}:temp _mb_src[0]
function {ns}:v{version}/zombies/mystery_box/build_pool_next
""")
	write_versioned_function("zombies/mystery_box/build_pool_add", f"""
$execute unless data storage {ns}:zombies mystery_box_catalog.$(weapon_id) run return fail

$data modify storage {ns}:temp _mb_id set value "$(weapon_id)"
execute if data storage {ns}:temp {{_mb_id:"ray_gun"}} store result score #mb_ray_index {ns}.data run data get storage {ns}:zombies mystery_box_pool
execute if data storage {ns}:temp {{_mb_id:"ray_gun"}} run scoreboard players operation #mb_ray_weight {ns}.data = #mb_w {ns}.data
$data modify storage {ns}:zombies mystery_box_pool append from storage {ns}:zombies mystery_box_catalog.$(weapon_id)
data modify storage {ns}:zombies mystery_box_weights append value 0
execute store result storage {ns}:zombies mystery_box_weights[-1] int 1 run scoreboard players get #mb_w {ns}.data
""")

	## The Ray Gun's weight doubles after dry pulls, before round 25; a pool without it has nothing to weigh.
	write_versioned_function("zombies/mystery_box/weigh_ray_gun", f"""
execute if score #mb_ray_index {ns}.data matches ..-1 run return 0

scoreboard players operation #mb_w {ns}.data = #mb_ray_weight {ns}.data
execute if score #zb_round {ns}.data matches ..24 if score #mb_dry_ray_gun {ns}.data matches {RAY_GUN_DRY_PULLS + 1}.. run scoreboard players operation #mb_w {ns}.data += #mb_ray_weight {ns}.data
execute store result storage {ns}:temp _mb_ray.i int 1 run scoreboard players get #mb_ray_index {ns}.data
execute store result storage {ns}:temp _mb_ray.w int 1 run scoreboard players get #mb_w {ns}.data
function {ns}:v{version}/zombies/mystery_box/weigh_ray_gun_at with storage {ns}:temp _mb_ray
""")
	write_versioned_function("zombies/mystery_box/weigh_ray_gun_at", f"$data modify storage {ns}:zombies mystery_box_weights[$(i)] set value $(w)")

