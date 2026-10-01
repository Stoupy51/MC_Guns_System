""" The reload flow and the Sleight of Hand speed-up. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.items import ItemBuilder
from .....config.stats.keys import BASE_WEAPON, CAPACITY, RELOAD_TIME, REMAINING_BULLETS


# Functions
def write_reload() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# A matching magazine with bullets, without consuming it.
	loaded_magazine: str = f'*[custom_data~{{{ns}:{{magazine:true,weapon:"$({BASE_WEAPON})"}}}},!custom_data~{{{ns}:{{stats:{{{REMAINING_BULLETS}:0}}}}}}]'
	has_ammo_checks: str = "".join(f"$execute if items entity @s {slots} {loaded_magazine} run return 1\n" for slots in ItemBuilder.ALL_SLOT_RANGES)
	write_versioned_function("ammo/inventory/has_ammo", f"""
# Returns 1 when found. Empty regular magazines (remaining_bullets 0) are skipped; consumables have no such field.
{has_ammo_checks}
return fail
""")

	# Deferred: magazines are consumed when the reload ends.
	write_versioned_function("ammo/reload", f"""
# Already reloading, or full.
execute if entity @s[tag={ns}.reloading] run return fail
execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute if score @s {ns}.{REMAINING_BULLETS} >= #capacity {ns}.data run return fail

# Magazines available, without consuming them.
scoreboard players set @s {ns}.cooldown 5
scoreboard players operation @s {ns}.cooldown += #total_tick {ns}.data
execute unless data storage {ns}:config no_magazine store success score #success {ns}.data run function {ns}:v{version}/ammo/inventory/has_ammo with storage {ns}:gun all.stats
execute unless data storage {ns}:config no_magazine if score #success {ns}.data matches 0 run return run playsound {ns}:common/empty ambient @s

# Reload duration, with the quick_reload reduction.
execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{RELOAD_TIME}

# quick_reload is a percentage (20 = 20% faster).
execute if score @s {ns}.special.quick_reload matches 1.. run function {ns}:v{version}/ammo/apply_quick_reload

# As an expiry tick.
scoreboard players operation @s {ns}.cooldown += #total_tick {ns}.data

function {ns}:v{version}/switch/force_switch_animation

# Each sound is guarded: not every weapon defines all of them, and a missing macro argument errors.
execute if data storage {ns}:gun all.sounds.reload run function {ns}:v{version}/sound/reload_start with storage {ns}:gun all.sounds
execute if data storage {ns}:gun all.sounds.playerbegin run function {ns}:v{version}/sound/player_begin with storage {ns}:gun all.sounds

tag @s add {ns}.reloading

# Run as the player; weapon data in mgs:signals.
data modify storage {ns}:signals on_reload set value {{}}
data modify storage {ns}:signals on_reload.weapon set from storage {ns}:gun all
function #{ns}:signals/on_reload
""")

	write_versioned_function("ammo/apply_quick_reload", f"""
# cooldown x (100 - quick_reload) / 100
scoreboard players operation #reduction {ns}.data = #100 {ns}.data
scoreboard players operation #reduction {ns}.data -= @s {ns}.special.quick_reload
scoreboard players operation @s {ns}.cooldown *= #reduction {ns}.data
scoreboard players operation @s {ns}.cooldown /= #100 {ns}.data

# At least 1 tick.
execute if score @s {ns}.cooldown matches ..0 run scoreboard players set @s {ns}.cooldown 1
""")

