""" Detonation per grenade type: web, frag/semtex blast, smoke and flash. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import GRENADE_DURATION, GRENADE_EFFECT_RADIUS, GRENADE_TYPE
from ..explosion import Explosion


# Functions
def write_grenade_detonation() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Detonation router - dispatch based on grenade type
	write_versioned_function("grenade/detonate", f"""
# Route to the appropriate detonation effect based on grenade type
execute if data entity @s data.config{{{GRENADE_TYPE}:"frag"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"semtex"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"monkey_bomb"}} run return run function {ns}:v{version}/grenade/detonate_frag
execute if data entity @s data.config{{{GRENADE_TYPE}:"smoke"}} run return run function {ns}:v{version}/grenade/detonate_smoke
execute if data entity @s data.config{{{GRENADE_TYPE}:"flash"}} run return run function {ns}:v{version}/grenade/detonate_flash
execute if data entity @s data.config{{{GRENADE_TYPE}:"web"}} run return run function {ns}:v{version}/grenade/detonate_web
""")

	## Web grenade detonation (Widow's Wine): burst of webbing that roots + lightly damages zombies.
	## The actual webbing effect lives in the zombies module (widows_web_burst); this is the throwable delivery.
	## No-op outside zombies since there are no zombie_round entities to web.
	write_versioned_function("grenade/detonate_web", f"""
# Webbing burst visuals + sound
particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~0.5 ~ 1.2 0.8 1.2 0.1 80 force @a[distance=..64]
particle minecraft:block{{block_state:"minecraft:cobweb"}} ~ ~0.5 ~ 1.5 1 1.5 0.05 40 force @a[distance=..64]
playsound minecraft:block.wool.place player @a[distance=..48] ~ ~ ~ 1 0.7
playsound minecraft:entity.spider.step player @a[distance=..48] ~ ~ ~ 1 0.6

# Root + damage nearby zombies (radius from the grenade's effect radius stat)
execute store result score #web_r {ns}.data run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
execute store result storage {ns}:temp _web.radius float 1 run scoreboard players get #web_r {ns}.data
execute at @s run function {ns}:v{version}/zombies/perks/widows_web_burst with storage {ns}:temp _web

# Delete the grenade
function {ns}:v{version}/grenade/delete
""")

	## Frag/Semtex detonation - explosion with area damage (reuses projectile explosion logic)
	write_versioned_function("grenade/detonate_frag", f"""
# Explosion particles
particle explosion ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]
particle flame ~ ~ ~ 1 1 1 0.1 100 force @a[distance=..128]
particle campfire_cosy_smoke ~ ~ ~ 1.5 1.5 1.5 0.05 100 force @a[distance=..128]
particle campfire_signal_smoke ~ ~ ~ 0.5 0.5 0.5 0.05 20 force @a[distance=..128]
particle lava ~ ~ ~ 1 1 1 0 30 force @a[distance=..128]

# Explosion sound
playsound minecraft:entity.generic.explode player @a[distance=..64] ~ ~ ~ 2 0.8

# Block destruction via RealisticExplosionLibrary (if grenade_explosion_power > 0)
execute if score #grenade_explosion_power {ns}.config matches 1.. run function {ns}:v{version}/grenade/realistic_explosion

# Store explosion center position for damage calculation (scores used by projectile/damage_entity)
{Explosion.setup_lines(ns, version)}

# Apply area damage to nearby entities (macro for configurable radius)
{Explosion.area_damage_lines(ns, version)}

# Signal: on_explosion
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
data modify storage {ns}:signals on_explosion.grenade set value true
function #{ns}:signals/on_explosion

# Clean up shooter tag
tag @e[tag={ns}.temp_shooter] remove {ns}.temp_shooter

# Delete the grenade
function {ns}:v{version}/grenade/delete
""")

	## Realistic block destruction for grenades
	write_versioned_function("grenade/realistic_explosion", f"""
# Set explosion power from config and call the library
scoreboard players operation #explosion_power realistic_explosion.data = #grenade_explosion_power {ns}.config
execute if score #grenade_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 1
execute unless score #grenade_explosion_power {ns}.config matches 1.. run scoreboard players set #falling_fire realistic_explosion.data 0
function realistic_explosion:explode
""")

	## Smoke grenade detonation - start emitting smoke particles
	write_versioned_function("grenade/detonate_smoke", f"""
# Activation sound
playsound minecraft:block.fire.extinguish player @a[distance=..32] ~ ~ ~ 1 0.8
playsound minecraft:entity.generic.extinguish_fire player @a[distance=..32] ~ ~ ~ 1 0.5

# Set duration timer (reuse the fuse score for duration countdown)
execute store result score @s {ns}.data run data get entity @s data.config.{GRENADE_DURATION}

# Mark as active effect (skip movement in tick)
tag @s add {ns}.grenade_active_effect

# Stop all velocity
scoreboard players set @s bs.vel.x 0
scoreboard players set @s bs.vel.y 0
scoreboard players set @s bs.vel.z 0

# Initial burst of smoke
particle campfire_signal_smoke ~ ~ ~ 1.5 1 1.5 0.02 200 force @a[distance=..128]
""")

	## Flash grenade detonation - blind nearby players
	write_versioned_function("grenade/detonate_flash", f"""
# Flash sound
playsound minecraft:entity.firework_rocket.blast player @a[distance=..32] ~ ~ ~ 2 2
playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..16] ~ ~ ~ 0.3 2

# Flash particles
particle flash{{color:[1.0,1.0,1.0,1.0]}} ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]
particle end_rod ~ ~ ~ 1 1 1 0.1 50 force @a[distance=..64]

# Tag this grenade as the flash source for visibility checks
tag @s add {ns}.flash_source

# Apply flash to nearby players (with direction and LOS checks)
function {ns}:v{version}/grenade/flash_apply

# Remove flash source tag
tag @s remove {ns}.flash_source

# Signal: on_explosion (flash type)
data modify storage {ns}:signals on_explosion set value {{}}
data modify storage {ns}:signals on_explosion.config set from entity @s data.config
data modify storage {ns}:signals on_explosion.position set from entity @s Pos
data modify storage {ns}:signals on_explosion.grenade set value true
function #{ns}:signals/on_explosion

# Delete the grenade
function {ns}:v{version}/grenade/delete
""")

	## Apply flash effect to nearby players (macro for configurable radius)
	write_versioned_function("grenade/flash_apply", f"""
# Apply blindness and darkness effects to all players within radius
execute store result storage {ns}:temp flash.radius_float float 1 run data get entity @s data.config.{GRENADE_EFFECT_RADIUS}
function {ns}:v{version}/grenade/flash_area with storage {ns}:temp flash
""")

	write_versioned_function("grenade/flash_area", f"""
$execute as @a[distance=..$(radius_float)] at @s run function {ns}:v{version}/grenade/flash_check
""")

	# Check if this player should be flashed (close range OR looking at grenade with LOS)
	write_versioned_function("grenade/flash_check", f"""
# @s = player, position = player's position (from at @s)
# Flash source grenade is tagged {ns}.flash_source

# Close range override: within 3 blocks, always flash (too close to avoid)
execute if entity @e[tag={ns}.flash_source,distance=..3] run return run function {ns}:v{version}/grenade/flash_player

# Direction check: is the grenade within the player's field of view? (110 degree cone)
execute at @n[tag={ns}.flash_source] store result score #in_fov {ns}.data run function #bs.view:in_view_ata {{angle:110}}
execute unless score #in_fov {ns}.data matches 1 run return 0

# Line-of-sight check: can the player see the grenade? (no blocks between)
scoreboard players set #can_see {ns}.data 0
execute at @n[tag={ns}.flash_source] store result score #can_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute unless score #can_see {ns}.data matches 1 run return 0

# Both checks passed: flash the player
function {ns}:v{version}/grenade/flash_player
""")

	write_versioned_function("grenade/flash_player", f"""
# Tactical Mask perk (MP): greatly reduced flash — short blindness, no darkness, brief screen
execute if score @s {ns}.mp.in_game matches 1 if score @s {ns}.special.tactical_mask matches 1 run return run function {ns}:v{version}/grenade/flash_player_masked

# Apply full blindness + darkness
effect give @s minecraft:blindness 5 0 true
effect give @s minecraft:darkness 3 0 true

# White screen flash using custom font (1x1 white pixel scaled to fill screen)
title @s times 5 40 20
title @s title {{"text":"F","font":"{ns}:flash"}}
""")

	write_versioned_function("grenade/flash_player_masked", f"""
# Reduced flash for Tactical Mask holders
effect give @s minecraft:blindness 1 0 true
title @s times 2 10 10
title @s title {{"text":"F","font":"{ns}:flash"}}
""")

