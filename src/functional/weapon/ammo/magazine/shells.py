""" Shell-at-a-time reloading and the reserve-ammo total. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import BASE_WEAPON, CAPACITY, REMAINING_BULLETS


# Functions
def write_shell_reload() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## no_magazine mode: one bullet, clamped to capacity.
	write_versioned_function("ammo/single_reload_add_one", f"""
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
scoreboard players add @s {ns}.{REMAINING_BULLETS} 1
execute if score @s {ns}.{REMAINING_BULLETS} > #capacity {ns}.data run scoreboard players operation @s {ns}.{REMAINING_BULLETS} = #capacity {ns}.data
""")

	## Chains until full. Firing (pending clicks) stops it, and a weapon switch removes {ns}.reloading, which breaks the chain.
	write_versioned_function("ammo/single_reload_continue", f"""
# Lets the player fire mid-reload.
execute if score @s {ns}.pending_clicks matches 0.. run return fail

execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute if score @s {ns}.{REMAINING_BULLETS} >= #capacity {ns}.data run return fail

# No matching ammo left: stop silently.
execute unless data storage {ns}:config no_magazine store success score #success {ns}.data run function {ns}:v{version}/ammo/inventory/has_ammo with storage {ns}:gun all.stats
execute unless data storage {ns}:config no_magazine if score #success {ns}.data matches 0 run return fail

# Plays the reload sound and sets a fresh per-shell cooldown.
function {ns}:v{version}/ammo/reload
""")

	## Sum of the bullets in magazines matching the held gun (the main hand excluded); run on reload and after about 60 idle ticks.
	reserve_slot_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		if slot == "weapon.mainhand":
			continue
		reserve_slot_checks += (
			f"$execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true,weapon:\"$({BASE_WEAPON})\"}}}}] run "
			f"function {ns}:v{version}/ammo/reserve/extract_slot {{slot:\"{slot}\"}}\n"
		)
	write_versioned_function("ammo/compute_reserve", f"""
execute unless data storage {ns}:gun all.gun run return fail

# Grenades have no base_weapon.
execute unless data storage {ns}:gun all.stats.{BASE_WEAPON} run return fail

scoreboard players set @s {ns}.reserve_ammo 0

# Run as the ticking player.
function {ns}:v{version}/ammo/reserve/scan with storage {ns}:gun all.stats
return 0
""")

	write_versioned_function("ammo/reserve/scan", f"""
# Run as the player; $(base_weapon) is the held gun.
{reserve_slot_checks}
""")

	write_versioned_function("ammo/reserve/extract_slot", f"""
# Per slot holding a matching magazine, read through a temporary entity.
tag @s add {ns}.reading_reserve
$execute summon item_display run function {ns}:v{version}/ammo/reserve/read_item {{slot:"$(slot)"}}
tag @s remove {ns}.reading_reserve
""")

	write_versioned_function("ammo/reserve/read_item", f"""
$item replace entity @s contents from entity @p[tag={ns}.reading_reserve] $(slot)

# A consumable (1b) counts one bullet per item.
execute if data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #mag_bullets {ns}.data run data get entity @s item.count

# Others read remaining_bullets.
execute unless data entity @s item.components."minecraft:custom_data".{ns}{{consumable:1b}} store result score #mag_bullets {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}

scoreboard players operation @p[tag={ns}.reading_reserve] {ns}.reserve_ammo += #mag_bullets {ns}.data

kill @s
""")

