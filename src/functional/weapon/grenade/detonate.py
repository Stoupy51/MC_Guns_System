""" Detonation per grenade type: web, frag/semtex blast, smoke and flash. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import GRENADE_DURATION, GRENADE_EFFECT_RADIUS, GRENADE_TYPE
from ...helpers.titles import TitleTimes
from ..explosion import Explosion


# Functions
def write_grenade_detonation() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("grenade/detonate", f"""
execute if data entity @s data.config{{{GRENADE_TYPE}:"frag"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"semtex"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"monkey_bomb"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"smoke"}} run return run function {ns}:v{version}/grenade/detonate_smoke
execute if data entity @s data.config{{{GRENADE_TYPE}:"flash"}} run return run function {ns}:v{version}/grenade/detonate_flash
execute if data entity @s data.config{{{GRENADE_TYPE}:"web"}} run return run function {ns}:v{version}/grenade/detonate_web
""")

	## Widow's Wine web grenade: the webbing lives in zombies (widows_web_burst); outside zombies there are no zombie_round entities to web.
	write_versioned_function("grenade/detonate_web", f"""
particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~0.5 ~ 1.2 0.8 1.2 0.1 80 force @a[distance=..64]
particle minecraft:block{{block_state:"minecraft:cobweb"}} ~ ~0.5 ~ 1.5 1 1.5 0.05 40 force @a[distance=..64]
playsound minecraft:block.wool.place player @a[distance=..48] ~ ~ ~ 1 0.7
playsound minecraft:entity.spider.step player @a[distance=..48] ~ ~ ~ 1 0.6

# Radius from the grenade's effect radius.
execute store result score #web_r {ns}.data run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
execute store result storage {ns}:temp _web.radius float 1 run scoreboard players get #web_r {ns}.data
execute at @s run function {ns}:v{version}/zombies/perks/widows_web_burst with storage {ns}:temp _web

function {ns}:v{version}/grenade/delete
""")

	## Frag and Semtex: explosion with area damage (the projectile explosion logic).
	write_versioned_function("grenade/detonate_frag", f"""
particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 100 force @a[distance=..128]
particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# RealisticExplosionLibrary, when grenade_explosion_power > 0.
execute if score #grenade_explosion_power {ns}.config matches 1.. run function {ns}:v{version}/grenade/realistic_explosion

# Read by projectile/damage_entity.
{Explosion.setup_lines(ns, version)}

# Macro, for the configurable radius.
{Explosion.area_damage_lines(ns, version)}

data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
data modify storage {ns}:signals on_explosion.grenade set value true
function #{ns}:signals/on_explosion

tag @e[tag={ns}.temp_shooter] remove {ns}.temp_shooter

function {ns}:v{version}/grenade/delete
""")

	write_versioned_function("grenade/realistic_explosion", f"""
scoreboard players operation #explosion_power realistic_explosion.data = #grenade_explosion_power {ns}.config
execute if score #grenade_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #grenade_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode
""")

	write_versioned_function("grenade/detonate_smoke", f"""
playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 1 0.8
playsound minecraft:entity.generic.extinguish_fire player @a[distance=..32] ~ ~ ~ 1 0.5

# The fuse score counts the duration down.
execute store result score @s {ns}.data run data get entity @s data.config.{GRENADE_DURATION}

# The tick skips movement for active effects.
tag @s add {ns}.grenade_active_effect

scoreboard players set @s bs.vel.x 0
scoreboard players set @s bs.vel.y 0
scoreboard players set @s bs.vel.z 0

particle campfire_signal_smoke ~ ~ ~ 1.5 1 1.5 0.02 200 force @a[distance=..128]
""")

	write_versioned_function("grenade/detonate_flash", f"""
playsound minecraft:entity.firework_rocket.blast player @a[distance=..32] ~ ~ ~ 2 2
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..16] ~ ~ ~ 0.3 2

particle flash{{color:[1.0,1.0,1.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]
particle end_rod ~ ~ ~ 1 1 1 0.1 50 force @a[distance=..64]

# For the visibility checks.
tag @s add {ns}.flash_source

function {ns}:v{version}/grenade/flash_apply

tag @s remove {ns}.flash_source

data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
data modify storage {ns}:signals on_explosion.grenade set value true
function #{ns}:signals/on_explosion

function {ns}:v{version}/grenade/delete
""")

	## Macro, for the configurable radius.
	write_versioned_function("grenade/flash_apply", f"""
execute store result storage {ns}:temp flash.radius_float float 1 run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
function {ns}:v{version}/grenade/flash_area with storage {ns}:temp flash
""")

	write_versioned_function("grenade/flash_area", f"""
$execute as @a[distance=..$(radius_float)] at @s run function {ns}:v{version}/grenade/flash_check
""")

	# Close range, or looking at the grenade with line of sight.
	write_versioned_function("grenade/flash_check", f"""
# Run as the player, at them; the grenade carries {ns}.flash_source.

# Within 3 blocks: always flashed.
execute if entity @e[tag={ns}.flash_source,distance=..3] run return run function {ns}:v{version}/grenade/flash_player

# Within a 110 degree view cone.
execute at @n[tag={ns}.flash_source] store result score #in_fov {ns}.data run function #bs.view:in_view_ata {{angle:110}}
execute unless score #in_fov {ns}.data matches 1 run return 0

scoreboard players set #can_see {ns}.data 0
execute at @n[tag={ns}.flash_source] store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute unless score #can_see {ns}.data matches 1 run return 0

function {ns}:v{version}/grenade/flash_player
""")

	write_versioned_function("grenade/flash_player", f"""
# Tactical Mask (MP): short blindness, no darkness, a brief screen flash.
execute if score @s {ns}.mp.in_game matches 1 if score @s {ns}.special.tactical_mask matches 1 run return run function {ns}:v{version}/grenade/flash_player_masked

effect give @s minecraft:blindness 5 0 true
effect give @s minecraft:darkness 3 0 true

# A custom font pixel scaled to fill the screen.
{TitleTimes.FLASH_FULL.cmd()}
title @s title {{"text":"F","font":"{ns}:flash"}}
""")

	write_versioned_function("grenade/flash_player_masked", f"""
effect give @s minecraft:blindness 1 0 true
{TitleTimes.FLASH_WEAK.cmd()}
title @s title {{"text":"F","font":"{ns}:flash"}}
""")

