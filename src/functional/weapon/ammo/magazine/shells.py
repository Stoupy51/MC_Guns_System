""" Shell-at-a-time reloading and the reserve-ammo total. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import BASE_WEAPON, CAPACITY, REMAINING_BULLETS


# Functions
def write_shell_reload() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Single-shell reload (no_magazine mode): add one bullet, clamped to capacity
	write_versioned_function("ammo/single_reload_add_one", f"""
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
scoreboard players add @s {ns}.{REMAINING_BULLETS} 1
execute if score @s {ns}.{REMAINING_BULLETS} > #capacity {ns}.data run scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #capacity {ns}.data
""")

	## Single-shell reload: decide whether to load the next shell Chains until full; aborted by firing (pending clicks) — switching weapon already cancels the {ns}.reloading tag, which breaks the chain naturally.
	write_versioned_function("ammo/single_reload_continue", f"""
# Stop if the player is actively trying to shoot (lets them fire mid-reload)
execute if score @s {ns}.pending_clicks matches 0.. run return fail

# Stop if the magazine is already full
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute if score @s {ns}.{REMAINING_BULLETS} >= #capacity {ns}.data run return fail

# Stop silently if no matching ammo remains in the inventory
execute unless data storage {ns}:config no_magazine store success score #success {ns}.data run function {ns}:v{version}/ammo/inventory/has_ammo with storage {ns}:gun all.stats
execute unless data storage {ns}:config no_magazine if score #success {ns}.data matches 0 run return fail

# Load the next shell (plays the reload sound and sets a fresh per-shell cooldown)
function {ns}:v{version}/ammo/reload
""")

	## compute_reserve - Sum all magazine bullets in inventory for the current weapon Only counts magazines whose base_weapon matches the gun in hand Called on reload and when player is idle (~60 ticks without shooting) Build per-slot check lines: for each inventory/hotbar slot, if it contains a matching magazine (but skip the mainhand weapon itself), extract and add bullet count.
	reserve_slot_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		if slot == "weapon.mainhand":
			continue
		reserve_slot_checks += (
			f"$execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true,weapon:\"$({BASE_WEAPON})\"}}}}] run "
			f"function {ns}:v{version}/ammo/reserve/extract_slot {{slot:\"{slot}\"}}\n"
		)
	write_versioned_function("ammo/compute_reserve", f"""
# Skip if not holding a gun
execute unless data storage {ns}:gun all.gun run return fail

# Skip if weapon has no base_weapon (e.g. grenades)
execute unless data storage {ns}:gun all.stats.{BASE_WEAPON} run return fail

# Reset reserve counter
scoreboard players set @s {ns}.reserve_ammo 0

# Sum bullets from all matching magazine slots (runs as ticking player)
function {ns}:v{version}/ammo/reserve/scan with storage {ns}:gun all.stats
return 0
""")

	write_versioned_function("ammo/reserve/scan", f"""
# @s = player, $(base_weapon) = current gun id
{reserve_slot_checks}
""")

	write_versioned_function("ammo/reserve/extract_slot", f"""
# Called for each slot containing a matching magazine
# Spawn temp entity to read item data
tag @s add {ns}.reading_reserve
$execute summon item_display run function {ns}:v{version}/ammo/reserve/read_item {{slot:"$(slot)"}}
tag @s remove {ns}.reading_reserve
""")

	write_versioned_function("ammo/reserve/read_item", f"""
# Copy item to entity
$item replace entity @s contents from entity @p[tag={ns}.reading_reserve] $(slot)

# Consumable (1b = true consumable): stack count = bullet count
execute if data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #mag_bullets {ns}.data run data get entity @s item.count

# Non-consumable: read remaining_bullets from custom data
execute unless data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #mag_bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}

# Add to reserve
scoreboard players operation @p[tag={ns}.reading_reserve] {ns}.reserve_ammo += #mag_bullets {ns}.data

# Kill entity
kill @s
""")

