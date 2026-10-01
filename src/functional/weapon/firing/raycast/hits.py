""" Ray entry and exit points, block and entity hits, damage decay and the headshot bonus. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import DECAY


# Functions
def write_hit_resolution() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("raycast/on_exit_point", f"""
execute if score #is_entity_hit {ns}.data matches 1 as @e[tag={ns}.raycast_target] run function {ns}:v{version}/raycast/headshot_and_damage
scoreboard players set #is_entity_hit {ns}.data 0
""")

	write_versioned_function("raycast/on_entry_point", f"""
# Entity hit: no block particles.
execute if score #is_entity_hit {ns}.data matches 1 run return 0

# on_targeted_block runs first and sets the pass-through flag.
data modify storage {ns}:input with set value {{block:"minecraft:air"}}
data modify storage {ns}:input with.block set from storage {ns}:temp block.type
execute if score #is_pass_through {ns}.data matches 0 run return run function {ns}:v{version}/raycast/block_particles with storage {ns}:input with

execute if score #is_water {ns}.data matches 1 run data modify storage {ns}:input with.block set value "minecraft:bubble"
execute if score #is_water {ns}.data matches 0 run data modify storage {ns}:input with.block set value "minecraft:mycelium"

# Every third step, to thin the particles.
scoreboard players add #next_air_particle {ns}.data 1
execute if score #next_air_particle {ns}.data matches 2 run function {ns}:v{version}/raycast/air_particles with storage {ns}:input with
execute if score #next_air_particle {ns}.data matches 3.. run scoreboard players set #next_air_particle {ns}.data 0
""")
	write_versioned_function("raycast/block_particles", r"""$particle block{block_state:"$(block)"} ~ ~ ~ 0.1 0.1 0.1 1 10 force @a[distance=..128]""")
	write_versioned_function("raycast/air_particles", r"""$particle $(block) ~ ~ ~ 0 0 0 0 1 force @a[distance=..128]""")

	write_versioned_function("raycast/on_targeted_block", f"""
# https://docs.mcbookshelf.dev/en/latest/modules/block.html#get
scoreboard players set #is_entity_hit {ns}.data 0
scoreboard players set #is_water {ns}.data 0
scoreboard players set #is_pass_through {ns}.data 0
execute if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through {ns}.data 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/water run scoreboard players set #is_water {ns}.data 1
function #bs.block:get_type
data modify storage {ns}:temp block set from storage bs:out block

# Pass-through blocks give the piercing back; only water continues below.
execute if score #is_pass_through {ns}.data matches 1 run scoreboard players add $raycast.piercing bs.lambda 1
execute if score #is_pass_through {ns}.data matches 1 unless block ~ ~ ~ #{ns}:v{version}/sounds/water run return 1

# Water and pass-through blocks: -5% damage.
execute if score #is_pass_through {ns}.data matches 1 store result score #new_damage {ns}.data run data get storage {ns}:temp damage 1000
execute if score #is_pass_through {ns}.data matches 1 store result storage {ns}:temp damage float 0.00095 run scoreboard players get #new_damage {ns}.data

# Solid blocks: look up the hardness.
execute if score #is_pass_through {ns}.data matches 0 run function #bs.block:lookup_type with storage bs:out block
execute if score #is_pass_through {ns}.data matches 0 store result score #hardness {ns}.data run data get storage bs:out block.hardness 1000

# Indestructible (bedrock, hardness -1) stops the bullet; barrier is in the raycast's ignored_blocks, so bullets fly through it.
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches ..-1 run data modify storage {ns}:temp damage set value 0.0d
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches ..-1 run return 0

# The first solid block caps piercing at 6 (it starts at 10).
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 0.. if score $raycast.piercing bs.lambda matches 7.. run scoreboard players set $raycast.piercing bs.lambda 6
# In the callback, where the lambda score is reachable.
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 0..299 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 300..999 run scoreboard players remove $raycast.piercing bs.lambda 2
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 1000..2999 run scoreboard players remove $raycast.piercing bs.lambda 3
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 3000.. run scoreboard players set $raycast.piercing bs.lambda 0

# Bookshelf only stops at exactly 0, not below.
execute if score #is_pass_through {ns}.data matches 0 if score $raycast.piercing bs.lambda matches ..-1 run scoreboard players set $raycast.piercing bs.lambda 0

execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 0.. run function {ns}:v{version}/raycast/apply_block_hardness

# Solid blocks only; run as the raycast marker, at the block.
execute if score #is_pass_through {ns}.data matches 0 run data modify storage {ns}:signals on_hit_block set value {{}}
execute if score #is_pass_through {ns}.data matches 0 run data modify storage {ns}:signals on_hit_block.block set from storage {ns}:temp block
execute if score #is_pass_through {ns}.data matches 0 run data modify storage {ns}:signals on_hit_block.weapon set from storage {ns}:gun all
execute if score #is_pass_through {ns}.data matches 0 run function #{ns}:signals/on_hit_block

# Hardness 1.0+: impact sound, and the ray stops.
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 1000.. if score #played_solid {ns}.data matches 0 store success score #played_solid {ns}.data run playsound {ns}:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #is_pass_through {ns}.data matches 0 if score #hardness {ns}.data matches 1000.. run return 0

## Each sound plays once per shot (#played_* set to 1); `return run` tries only one sound per block hit.
execute if score #is_pass_through {ns}.data matches 1 run return run execute if score #played_water {ns}.data matches 0 store success score #played_water {ns}.data run playsound minecraft:entity.axolotl.splash block @a[distance=..24] ~ ~ ~ 0.8 1.5
execute if block ~ ~ ~ #{ns}:v{version}/sounds/glass run return run execute if score #played_glass {ns}.data matches 0 store success score #played_glass {ns}.data run playsound minecraft:block.glass.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/cloth run return run execute if score #played_cloth {ns}.data matches 0 store success score #played_cloth {ns}.data run playsound {ns}:common/cloth_bullet_impact block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/sounds/dirt run return run execute if score #played_dirt {ns}.data matches 0 store success score #played_dirt {ns}.data run playsound {ns}:common/dirt_bullet_impact block @a[distance=..24] ~ ~ ~ 0.3
execute if block ~ ~ ~ #{ns}:v{version}/sounds/mud run return run execute if score #played_mud {ns}.data matches 0 store success score #played_mud {ns}.data run playsound {ns}:common/mud_bullet_impact block @a[distance=..24] ~ ~ ~ 0.4
execute if block ~ ~ ~ #{ns}:v{version}/sounds/wood run return run execute if score #played_wood {ns}.data matches 0 store success score #played_wood {ns}.data run playsound {ns}:common/wood_bullet_impact block @a[distance=..24] ~ ~ ~ 0.5
execute if block ~ ~ ~ #{ns}:v{version}/plant run return run execute if score #played_plant {ns}.data matches 0 store success score #played_plant {ns}.data run playsound minecraft:block.azalea_leaves.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #{ns}:v{version}/solid run return run execute if score #played_solid {ns}.data matches 0 store success score #played_solid {ns}.data run playsound {ns}:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #played_soft {ns}.data matches 0 store success score #played_soft {ns}.data run playsound {ns}:common/soft_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
""")

	write_versioned_function("raycast/apply_block_hardness", f"""

# reduction = hardness x 400 / 1000, capped at 950.
scoreboard players operation #reduction {ns}.data = #hardness {ns}.data
scoreboard players operation #reduction {ns}.data /= #10 {ns}.data
scoreboard players operation #reduction {ns}.data *= #2 {ns}.data
scoreboard players operation #reduction {ns}.data *= #2 {ns}.data
execute if score #reduction {ns}.data matches 951.. run scoreboard players set #reduction {ns}.data 950

# damage = damage x (1000 - reduction) / 1000.
execute store result score #new_damage {ns}.data run data get storage {ns}:temp damage 1000
scoreboard players set #remaining_pct {ns}.data 1000
scoreboard players operation #remaining_pct {ns}.data -= #reduction {ns}.data
scoreboard players operation #new_damage {ns}.data *= #remaining_pct {ns}.data
scoreboard players operation #new_damage {ns}.data /= #1000 {ns}.data
execute store result storage {ns}:temp damage float 0.001 run scoreboard players get #new_damage {ns}.data
""")

	write_versioned_function("raycast/on_targeted_entity", f"""
# Teammates are skipped, the shooter is not.
execute if entity @s[type=player,gamemode=spectator] run return 0
execute if entity @s[type=player] unless entity @s[tag={ns}.ticking] store result score #shooter_team {ns}.data run scoreboard players get @n[tag={ns}.ticking] {ns}.mp.team
execute if entity @s[type=player] unless entity @s[tag={ns}.ticking] if score #shooter_team {ns}.data matches 1.. if score @s {ns}.mp.team = #shooter_team {ns}.data run return fail

scoreboard players set #is_entity_hit {ns}.data 1
tag @s add {ns}.raycast_target

# Only the first 3 entities hit per shot bleed.
execute if score #hit_particles_left {ns}.data matches 1.. at @s run particle block{{block_state:"redstone_wire"}} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]
scoreboard players remove #hit_particles_left {ns}.data 1

data modify storage {ns}:input with set value {{target:"@s", amount:0.0f, attacker:"@n[tag={ns}.ticking]"}}
execute if entity @n[tag={ns}.ticking,type=player] run data modify storage {ns}:input with.attacker set value "@p[tag={ns}.ticking]"
execute store result score #damage {ns}.data run data get storage {ns}:temp damage 10
execute if score @n[tag={ns}.ticking] {ns}.special.double_tap matches 1.. run scoreboard players operation #damage {ns}.data *= #2 {ns}.data
function {ns}:v{version}/raycast/apply_decay
""")

	write_versioned_function("raycast/apply_decay", f"""
## damage *= pow(decay, distance / 10)
data modify storage bs:in math.pow.x set from storage {ns}:gun all.stats.{DECAY}

execute store result score #raycast_distance {ns}.data run scoreboard players get $raycast.entry_distance bs.lambda
scoreboard players operation #raycast_distance {ns}.data /= #10 {ns}.data
execute store result storage bs:in math.pow.y float 0.001 run scoreboard players get #raycast_distance {ns}.data

# https://docs.mcbookshelf.dev/en/latest/modules/math.html#power
function #bs.math:pow

execute store result score #pow_decay_distance {ns}.data run data get storage bs:out math.pow 1000
scoreboard players operation #damage {ns}.data *= #pow_decay_distance {ns}.data

# Two values scaled by 1000 were multiplied.
scoreboard players operation #damage {ns}.data /= #1000 {ns}.data
""")

	write_versioned_function("raycast/headshot_and_damage", f"""
tag @s remove {ns}.raycast_target

# Head zone: Y above 1400, relative to the entity.
scoreboard players set #is_headshot {ns}.data 0
scoreboard players set #headshot_multiplier {ns}.data 1000
execute unless score $raycast.entry_point.y bs.lambda matches 1400.. at @s run return run function {ns}:v{version}/raycast/apply_damage

# Centre of the trajectory through the head: ((entry_x + exit_x) / 2, (entry_z + exit_z) / 2).
execute store result score #entry_x {ns}.data run scoreboard players get $raycast.entry_point.x bs.lambda
execute store result score #entry_z {ns}.data run scoreboard players get $raycast.entry_point.z bs.lambda
execute store result score #exit_x {ns}.data run scoreboard players get $raycast.exit_point.x bs.lambda
execute store result score #exit_z {ns}.data run scoreboard players get $raycast.exit_point.z bs.lambda

scoreboard players operation #exit_x {ns}.data += #entry_x {ns}.data
scoreboard players operation #exit_z {ns}.data += #entry_z {ns}.data
scoreboard players operation #exit_x {ns}.data /= #2 {ns}.data
scoreboard players operation #exit_z {ns}.data /= #2 {ns}.data

scoreboard players set #dist_sq {ns}.data 0
scoreboard players operation #dist_sq {ns}.data = #exit_x {ns}.data
scoreboard players operation #dist_sq {ns}.data *= #exit_x {ns}.data
scoreboard players operation #exit_z {ns}.data *= #exit_z {ns}.data
scoreboard players operation #dist_sq {ns}.data += #exit_z {ns}.data

# https://docs.mcbookshelf.dev/en/latest/modules/math/#square-root
scoreboard players operation $math.isqrt.x bs.in = #dist_sq {ns}.data
function #bs.math:isqrt
scoreboard players operation #distance {ns}.data = $math.isqrt bs.out

# 0.5 block.
execute if score #distance {ns}.data matches 501.. run scoreboard players set #distance {ns}.data 500

# 2000 - distance x 2.
scoreboard players set #headshot_multiplier {ns}.data 2000
scoreboard players operation #distance {ns}.data *= #2 {ns}.data
scoreboard players operation #headshot_multiplier {ns}.data -= #distance {ns}.data

scoreboard players operation #damage {ns}.data *= #headshot_multiplier {ns}.data
scoreboard players operation #damage {ns}.data /= #1000 {ns}.data

scoreboard players set #is_headshot {ns}.data 1
execute at @s run function {ns}:v{version}/raycast/apply_damage
""")

	write_versioned_function("raycast/apply_damage", f"""
execute as @n[tag={ns}.ticking] if score @s {ns}.special.instant_kill matches 1.. as @s[tag=!{ns}.no_instant_kill] run scoreboard players set #damage {ns}.data 99999

execute if score #is_headshot {ns}.data matches 1 run data modify storage {ns}:signals on_headshot set value {{}}
execute if score #is_headshot {ns}.data matches 1 run data modify storage {ns}:signals on_headshot.weapon set from storage {ns}:gun all
execute if score #is_headshot {ns}.data matches 1 store result storage {ns}:signals on_headshot.damage float 0.1 run scoreboard players get #damage {ns}.data
execute if score #is_headshot {ns}.data matches 1 run function #{ns}:signals/on_headshot

execute store result storage {ns}:input with.amount float 0.1 run scoreboard players get #damage {ns}.data
data modify storage {ns}:input with.weapon set from storage {ns}:gun all
execute store result storage {ns}:input with.headshot int 1 run scoreboard players get #is_headshot {ns}.data
function {ns}:v{version}/utils/signal_and_damage

# Guarded against firing twice on an already dying entity.
scoreboard players set #victim_hp {ns}.data 0
execute store result score #victim_hp {ns}.data run data get entity @s Health 100
scoreboard players set #is_new_kill {ns}.data 0
execute if score #victim_hp {ns}.data matches ..0 unless entity @s[tag={ns}.already_killed] run scoreboard players set #is_new_kill {ns}.data 1
execute if score #victim_hp {ns}.data matches ..0 unless entity @s[tag={ns}.already_killed] run tag @s add {ns}.already_killed

# The killing shot drops a mission enemy's gun while it still holds it; drop_enemy_weapon tags the mob, so the death watch cannot drop twice.
execute if score #is_new_kill {ns}.data matches 1 if entity @s[tag={ns}.mission_enemy] at @s run function {ns}:v{version}/missions/drop_enemy_weapon

execute if score #is_new_kill {ns}.data matches 1 run data modify storage {ns}:signals on_kill set value {{}}
execute if score #is_new_kill {ns}.data matches 1 run data modify storage {ns}:signals on_kill.weapon set from storage {ns}:gun all

# The headshot goes in the payload: the projectile path fires on_kill without resetting #is_headshot.
# Absent means "not a headshot", as that path's `on_kill set value {{}}` gives.
execute if score #is_new_kill {ns}.data matches 1 store result storage {ns}:signals on_kill.headshot int 1 run scoreboard players get #is_headshot {ns}.data

execute if score #is_new_kill {ns}.data matches 1 as @n[tag={ns}.ticking] run function #{ns}:signals/on_kill
""")

