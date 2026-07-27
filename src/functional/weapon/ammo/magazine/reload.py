""" The reload flow and the Sleight of Hand speed-up. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import BASE_WEAPON, CAPACITY, RELOAD_TIME, REMAINING_BULLETS


# Functions
def write_reload() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Check if any matching magazine with bullets exists in inventory (without consuming)
	has_ammo_checks: str = ""
	for slot in ItemBuilder.ALL_SLOTS:
		has_ammo_checks += (
			f"$execute if items entity @s {slot} *[custom_data~{{{ns}:{{magazine:true,weapon:\"$({BASE_WEAPON})\"}}}}] "
			f"unless items entity @s {slot} *[custom_data~{{{ns}:{{stats:{{{REMAINING_BULLETS}:0}}}}}}] "
			f"run return 1\n"
		)
	write_versioned_function("ammo/inventory/has_ammo", f"""
# Check all slots for matching magazines with bullets (return 1 if found, fail otherwise)
# Excludes empty non-consumable magazines (remaining_bullets: 0)
# Consumable magazines don't have this field, so they pass the 'unless' check if they exist
{has_ammo_checks}
return fail
""")

	# Reload weapon function (deferred: magazines consumed on reload end, not start)
	write_versioned_function("ammo/reload", f"""
# Stop if already reloading, or already has full ammo
execute if entity @s[tag={ns}.reloading] run return fail
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute if score @s {ns}.{REMAINING_BULLETS} >= #capacity {ns}.data run return fail

# Check if magazines are available (without consuming them)
scoreboard players set @s {ns}.cooldown 5
scoreboard players operation @s {ns}.cooldown += #total_tick {ns}.data
execute unless data storage {ns}:config no_magazine store success score #success {ns}.data run function {ns}:v{version}/ammo/inventory/has_ammo with storage {ns}:gun all.stats
execute unless data storage {ns}:config no_magazine if score #success {ns}.data matches 0 run return run playsound {ns}:common/empty ambient @s

# Set cooldown as expiration tick: get reload duration and apply quick_reload reduction
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{RELOAD_TIME}

# Apply quick reload: reduce cooldown by quick_reload% (e.g. 20 = 20% faster)
execute if score @s {ns}.special.quick_reload matches 1.. run function {ns}:v{version}/ammo/apply_quick_reload

# Convert to expiration tick
scoreboard players operation @s {ns}.cooldown += #total_tick {ns}.data

# Force weapon switch animation
function {ns}:v{version}/switch/force_switch_animation

# Play reload sound (and send sounds for macro). Each is guarded because not every
# weapon defines all reload sounds — calling the macro without the arg would error.
execute if data storage {ns}:gun all.sounds.reload run function {ns}:v{version}/sound/reload_start with storage {ns}:gun all.sounds
execute if data storage {ns}:gun all.sounds.playerbegin run function {ns}:v{version}/sound/player_begin with storage {ns}:gun all.sounds

# Add reloading tag
tag @s add {ns}.reloading

# Signal: on_reload (@s = reloading player, weapon data in mgs:signals)
data modify storage {ns}:signals on_reload set value {{}}
data modify storage {ns}:signals on_reload.weapon set from storage {ns}:gun all
function #{ns}:signals/on_reload
""")

	# Apply quick reload: reduce cooldown by quick_reload% (cooldown * (100 - quick_reload) / 100)
	write_versioned_function("ammo/apply_quick_reload", f"""
# Calculate reduced cooldown: cooldown = cooldown * (100 - quick_reload%) / 100
scoreboard players operation #reduction {ns}.data = #100 {ns}.data
scoreboard players operation #reduction {ns}.data -= @s {ns}.special.quick_reload
scoreboard players operation @s {ns}.cooldown *= #reduction {ns}.data
scoreboard players operation @s {ns}.cooldown /= #100 {ns}.data

# Ensure minimum cooldown of 1 tick
execute if score @s {ns}.cooldown matches ..0 run scoreboard players set @s {ns}.cooldown 1
""")

