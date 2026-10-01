""" Gun-wielding mob AI: arms mobs with weapons and drives their firing loop. """
# Imports
from stewbeet import (
	Mem,
	write_function,
	write_load_file,
	write_tick_file,
	write_versioned_function,
)

from ..config.stats.keys import (
	ACCURACY_BASE,
	COOLDOWN,
	GRENADE_TYPE,
	PELLET_COUNT,
	PROJECTILE_SPEED,
)


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# The tick loop is skipped at 0.
scoreboard players add #armed_mob_count {ns}.data 0

scoreboard objectives add {ns}.mob.timer dummy
scoreboard objectives add {ns}.mob.active_time dummy
scoreboard objectives add {ns}.mob.sleep_time dummy
""")

	write_versioned_function("mob/tick", f"""
execute unless entity @s[tag={ns}.mob_init] run function {ns}:v{version}/mob/init

execute if score @s {ns}.mob.timer matches 1.. run scoreboard players remove @s {ns}.mob.timer 1

execute if score @s {ns}.mob.timer matches 0 if entity @s[tag={ns}.mob_sleeping] run function {ns}:v{version}/mob/wake_up
execute if score @s {ns}.mob.timer matches 0 unless entity @s[tag={ns}.mob_sleeping] unless score @s {ns}.mob.sleep_time matches 0 run function {ns}:v{version}/mob/go_sleep

execute if entity @s[tag={ns}.mob_sleeping] run return 0

execute if score @s {ns}.cooldown matches 1.. run scoreboard players remove @s {ns}.cooldown 1

execute if score @s {ns}.cooldown matches 1.. run return 0

# Target first, before the costly equipment NBT gun copy: last attacker, else the nearest player.
scoreboard players set #mob_has_target {ns}.data 0
execute store success score #mob_has_target {ns}.data on attacker run tag @s add {ns}.target

# `on attacker` outlives the fight, so a dead (spectator) or creative attacker is dropped and the search below runs;
# the untag scan only runs in that rare case.
scoreboard players set #mob_dead_target {ns}.data 0
execute if score #mob_has_target {ns}.data matches 1 if entity @a[tag={ns}.target,gamemode=!adventure,gamemode=!survival] run scoreboard players set #mob_dead_target {ns}.data 1
execute if score #mob_dead_target {ns}.data matches 1 run scoreboard players set #mob_has_target {ns}.data 0
execute if score #mob_dead_target {ns}.data matches 1 run tag @a[tag={ns}.target] remove {ns}.target

# The nearest-player result goes to a scratch score: `store success` writes 0 when a guard filters the command out,
# which zeroed the attacker hit above. The range test is separate from `tag ... add`, which fails when the tag is already there.
scoreboard players set #mob_near_target {ns}.data 0
execute if score #mob_has_target {ns}.data matches 0 if entity @p[distance=..64,gamemode=!spectator,gamemode=!creative] run scoreboard players set #mob_near_target {ns}.data 1
execute if score #mob_near_target {ns}.data matches 1 run tag @p[distance=..64,gamemode=!spectator,gamemode=!creative] add {ns}.target
scoreboard players operation #mob_has_target {ns}.data > #mob_near_target {ns}.data

execute if score #mob_has_target {ns}.data matches 0 run return 0

# From the mainhand equipment.
function {ns}:v{version}/mob/copy_gun_data

# Also cleans the target tag up.
execute unless data storage {ns}:gun all.stats run return run tag @e[tag={ns}.target,limit=1] remove {ns}.target

# limit=1 skips the @n distance sort: only one entity carries the tag.
scoreboard players set #can_see {ns}.data 0
execute positioned as @e[tag={ns}.target,limit=1] store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute unless score #can_see {ns}.data matches 1 run return run tag @e[tag={ns}.target,limit=1] remove {ns}.target

# The damage and raycast system expects it.
tag @s add {ns}.ticking

execute anchored eyes facing entity @e[tag={ns}.target,limit=1] feet run function {ns}:v{version}/mob/fire_weapon

tag @e[tag={ns}.target,limit=1] remove {ns}.target
tag @s remove {ns}.ticking
""")

	write_versioned_function("mob/init", f"""
tag @s add {ns}.mob_init

# 50 ticks unless set.
execute unless score @s {ns}.mob.active_time matches 1.. run scoreboard players set @s {ns}.mob.active_time 50

# 100 ticks unless set.
execute unless score @s {ns}.mob.sleep_time matches 0.. run scoreboard players set @s {ns}.mob.sleep_time 100

# 1 s.
scoreboard players set @s {ns}.cooldown 20

function {ns}:v{version}/mob/wake_up
""")

	write_versioned_function("mob/wake_up", f"""
tag @s remove {ns}.mob_sleeping
scoreboard players operation @s {ns}.mob.timer = @s {ns}.mob.active_time
""")

	write_versioned_function("mob/go_sleep", f"""
tag @s add {ns}.mob_sleeping
scoreboard players operation @s {ns}.mob.timer = @s {ns}.mob.sleep_time
""")

	write_versioned_function("mob/copy_gun_data", f"""
data remove storage {ns}:gun all
data modify storage {ns}:gun all set from entity @s equipment.mainhand.components."minecraft:custom_data".{ns}
""")

	## Not for level 5 mobs.
	write_versioned_function("mob/apply_inaccuracy", f"""
# -20 to +20 degrees (-200..200 at 0.1).
execute store result storage {ns}:temp _rot.yaw double 0.1 run random value -200..200
execute store result storage {ns}:temp _rot.pitch double 0.1 run random value -200..200
function {ns}:v{version}/mob/apply_rotation_offset with storage {ns}:temp _rot
""")

	write_versioned_function("mob/apply_rotation_offset", """
$rotate @s ~$(yaw) ~$(pitch)
""")

	write_versioned_function("mob/fire_weapon", f"""
rotate @s facing entity @n[tag={ns}.target] eyes

# Level 5 mobs have perfect aim.
execute unless entity @s[tag={ns}.mob_lv5] run function {ns}:v{version}/mob/apply_inaccuracy

execute store result score @s {ns}.cooldown run data get storage {ns}:gun all.stats.{COOLDOWN}

scoreboard players set #bullets_to_fire {ns}.data 1
execute if data storage {ns}:gun all.stats.{PELLET_COUNT} store result score #bullets_to_fire {ns}.data run data get storage {ns}:gun all.stats.{PELLET_COUNT}

execute if data storage {ns}:gun all.stats.{GRENADE_TYPE} run return run function {ns}:v{version}/grenade/throw

# Weapons with projectile config fire slow projectiles instead of a raycast.
execute if data storage {ns}:gun all.stats.{PROJECTILE_SPEED} run return run function {ns}:v{version}/projectile/summon_loop

function {ns}:v{version}/mob/shoot

execute if data storage {ns}:gun all.sounds.fire run function {ns}:v{version}/mob/fire_sound with storage {ns}:gun all.sounds

# Weapon data in {ns}:signals.
data modify storage {ns}:signals on_shoot set value {{}}
data modify storage {ns}:signals on_shoot.weapon set from storage {ns}:gun all
function #{ns}:signals/on_shoot
""")

	write_versioned_function("mob/shoot", f"""
# Mobs use the base accuracy.
data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_BASE}

tag @s add bs.raycast.omit
execute anchored eyes positioned ^ ^ ^ summon marker run function {ns}:v{version}/raycast/main
tag @s remove bs.raycast.omit

scoreboard players remove #bullets_to_fire {ns}.data 1
execute if score #bullets_to_fire {ns}.data matches 1.. run function {ns}:v{version}/mob/shoot
""")

	write_versioned_function("mob/fire_sound", f"""
$playsound {ns}:$(fire) player @a[distance=0.01..48] ~ ~ ~ 0.35 1 0.10
""")

	write_tick_file(f"""
execute if score #armed_mob_count {ns}.data matches 1.. as @e[tag={ns}.armed] at @s run function {ns}:v{version}/mob/tick

# Every 5 s: dying mobs never decrement the counter.
scoreboard players operation #armed_mob_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #armed_mob_phase {ns}.data %= #100 {ns}.data
execute if score #armed_mob_count {ns}.data matches 1.. if score #armed_mob_phase {ns}.data matches 0 store result score #armed_mob_count {ns}.data if entity @e[tag={ns}.armed]
""")

	write_versioned_function("mob/default/on_new", f"""
tag @s add {ns}.armed
$data modify entity @s CustomName set value {{"text":"Armed $(entity) [Lv.$(level)]","color":"red"}}
data modify entity @s DeathLootTable set value "minecraft:empty"
data modify entity @s drop_chances set value {{mainhand:0.0f,offhand:0.0f}}
data modify entity @s PersistenceRequired set value true
attribute @s minecraft:waypoint_transmit_range base set 32

function {ns}:v{version}/utils/random_weapon {{slot:"weapon.mainhand"}}

$scoreboard players set @s {ns}.mob.active_time $(active_time)
$scoreboard players set @s {ns}.mob.sleep_time $(sleep_time)

scoreboard players add #armed_mob_count {ns}.data 1
""")
	# Level 5: perfect accuracy, always active.
	write_versioned_function("mob/default/on_new_lv5", f"""
$function {ns}:v{version}/mob/default/on_new {{entity:"$(entity)",level:5,active_time:72000,sleep_time:0}}
tag @s add {ns}.mob_lv5
""")

	# Unversioned entry points: maps store these function paths, and a versioned path breaks when the version changes
	# (a mission then spawns no enemy and completes at once).
	for level, active, sleep in [(1, 50, 100), (2, 50, 50), (3, 60, 20), (4, 72000, 1)]:
		write_function(
			f"{ns}:mob/default/level_{level}",
			f"""$execute summon $(entity) run function {ns}:v{version}/mob/default/on_new {{entity:"$(entity)",level:{level},active_time:{active},sleep_time:{sleep}}}"""
		)
	write_function(
		f"{ns}:mob/default/level_5",
		f"""$execute summon $(entity) run function {ns}:v{version}/mob/default/on_new_lv5 {{entity:"$(entity)"}}"""
	)

