""" Per-type enemy setup and the Treyarch health curve behind it. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_enemy_types() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Enemy types; each type function receives {level:"1"|"2"|"3"|"4"} as its macro argument.
	# All types call the shared scale logic; stubs fall through to normal scaling.

	## Normal zombie: scale health/speed by level + start rise animation
	write_versioned_function("zombies/types/normal", f"""
# Add scaled tag, and few data
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# Compute round-scaled HP (BO1 curve: +100 BO-HP per round until R9, then x1.1 per round) and apply it to this zombie
function {ns}:v{version}/zombies/calc_zombie_hp
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_zombie_hp with storage {ns}:temp _zb_hp

# Explicit speed per round, capped at 0.32 from round 13+
execute if score #zb_round {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round {ns}.data matches 2 run attribute @s minecraft:movement_speed base set 0.21
execute if score #zb_round {ns}.data matches 3 run attribute @s minecraft:movement_speed base set 0.22
execute if score #zb_round {ns}.data matches 4 run attribute @s minecraft:movement_speed base set 0.23
execute if score #zb_round {ns}.data matches 5 run attribute @s minecraft:movement_speed base set 0.24
execute if score #zb_round {ns}.data matches 6 run attribute @s minecraft:movement_speed base set 0.25
execute if score #zb_round {ns}.data matches 7 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_round {ns}.data matches 8 run attribute @s minecraft:movement_speed base set 0.27
execute if score #zb_round {ns}.data matches 9 run attribute @s minecraft:movement_speed base set 0.28
execute if score #zb_round {ns}.data matches 10 run attribute @s minecraft:movement_speed base set 0.29
execute if score #zb_round {ns}.data matches 11 run attribute @s minecraft:movement_speed base set 0.30
execute if score #zb_round {ns}.data matches 12 run attribute @s minecraft:movement_speed base set 0.31
execute if score #zb_round {ns}.data matches 13.. run attribute @s minecraft:movement_speed base set 0.32

# Gait picks the vocal set (enemies/vocals.py): 0.29+ is the Black Ops 2 sprint gait, which screams
# (3-5s clips) instead of groaning. Rounds 1-9 walk or run and stay on the short groan set.
execute if score #zb_round {ns}.data matches 10.. run tag @s add {ns}.zb_sprint

# For round 15+, 10% walkers (0.20 speed)
execute if score #zb_round {ns}.data matches 15.. store result score #zb_speed_roll {ns}.data run random value 1..10
execute if score #zb_round {ns}.data matches 15.. if score #zb_speed_roll {ns}.data matches 1 run attribute @s minecraft:movement_speed base set 0.20
execute if score #zb_round {ns}.data matches 15.. if score #zb_speed_roll {ns}.data matches 1 run tag @s remove {ns}.zb_sprint

# Fixed melee damage: 15.0 HP = 7.5 hearts and no knockback
attribute @s minecraft:attack_damage base set 15.0
attribute @s minecraft:knockback_resistance base set 1024

# Start rise animation (20 ticks to rise 2 blocks)
scoreboard players set @s {ns}.zb.rise_tick 20
""")

	## Compute zombie HP for current round, using the classic Treyarch (BO1) two-phase curve:
	## Rounds 1-9:  bo_hp = 50 + 100 * round        (R1=150, R2=250, ..., R9=950)
	## Round 10+:   bo_hp = 950 * 1.1^(round - 9)   (R10=1045, R11=1150, ...)
	## BO HP is then converted to Minecraft scale with a 2/15 factor (BO 150 HP = MC 20 HP, vanilla zombie)
	write_versioned_function("zombies/calc_zombie_hp", f"""
# Rounds 1-9: bo_hp = 50 + 100 * round
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data *= #100 {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players add #zb_hp {ns}.data 50

# Round 10+: exponent = round - 9
execute if score #zb_round {ns}.data matches 10.. run scoreboard players operation #zb_exp_round {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run scoreboard players remove #zb_exp_round {ns}.data 9

# Round 10+: bo_hp = 950 * 1.1^(round - 9)
execute if score #zb_round {ns}.data matches 10.. run data modify storage bs:in math.pow.x set value 1.1f
execute if score #zb_round {ns}.data matches 10.. store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run function #bs.math:pow
execute if score #zb_round {ns}.data matches 10.. store result score #zb_hp {ns}.data run data get storage bs:out math.pow 950

# Convert BO HP to Minecraft scale: hp = bo_hp * 2 / 15 (R1: 150 -> 20 HP)
scoreboard players operation #zb_hp {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #15 {ns}.data

# Cap at Minecraft-safe gameplay max (also catches int overflow on very high rounds)
execute unless score #zb_hp {ns}.data matches 15..2048 run scoreboard players set #zb_hp {ns}.data 2048
""")

	## Apply computed HP to the current zombie (@s)
	write_versioned_function("zombies/apply_zombie_hp", """
$attribute @s minecraft:max_health base set $(val)
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
""")

	## Same, for dogs: $(val) is the amount ABOVE a wolf's base 8, added as a modifier the taming side-effect reset can't clear (see types/dog).
	## Health is filled from the resulting effective max.
	write_versioned_function("zombies/apply_dog_hp", f"""
$attribute @s minecraft:max_health modifier add {ns}:dog_hp $(val) add_value
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
""")

	## Dog: fast, hits hard, same HP as the round's zombie.
	write_versioned_function("zombies/types/dog", f"""
# Add scaled tag, and few data
tag @s add {ns}.zb_scaled
data modify entity @s DeathTime set value -16s

# Same HP as the round's zombie — dogs get their threat from speed and damage, not durability
function {ns}:v{version}/zombies/calc_zombie_hp

# Carried as a MODIFIER, not a base value. Wolf extends TamableAnimal, whose readAdditionalSaveData
# calls setTame(false, true) on any untamed wolf -> applyTamingSideEffects() -> MAX_HEALTH base is
# hard-reset to 8.0. Every /data modify entity and every `store result entity` round-trips the entity
# through save/load, so the angry_at retarget silently reset each dog's base to 8 and Health then
# clamped to it — hence the one-hit kills. Modifiers survive that reset; base values cannot.
scoreboard players remove #zb_hp {ns}.data 8
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp {ns}.data
function {ns}:v{version}/zombies/apply_dog_hp with storage {ns}:temp _zb_hp

# Always faster than the zombie cap (0.32) — outrunning a dog pack should not be an option
execute if score #zb_round {ns}.data matches ..9 run attribute @s minecraft:movement_speed base set 0.36
execute if score #zb_round {ns}.data matches 10..19 run attribute @s minecraft:movement_speed base set 0.40
execute if score #zb_round {ns}.data matches 20.. run attribute @s minecraft:movement_speed base set 0.44

# Slightly below zombie melee (15.0), because dogs reach you far more often
attribute @s minecraft:attack_damage base set 12.0
attribute @s minecraft:knockback_resistance base set 1024

# Hellhound build: 1.5x a vanilla wolf, which also scales the hitbox so they're easier to hit
attribute @s minecraft:scale base set 1.5
""")

	## Armed zombie stub (TODO: carries weapon, drops ammo on death)
	write_versioned_function("zombies/types/armed", f"""
# TODO: armed zombie — unique AI goal: ranged attack, drops ammo powerup on death
# Falls through to normal scaling until implemented
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	## Fast zombie stub (TODO: higher movement speed, less health)
	write_versioned_function("zombies/types/fast", f"""
# TODO: fast zombie — higher base movement speed, reduced health pool
# Falls through to normal scaling until implemented
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

	## Tank zombie stub (TODO: very high health, slow movement)
	write_versioned_function("zombies/types/tank", f"""
# TODO: tank zombie — very high health, reduced movement speed
# Falls through to normal scaling until implemented
$function {ns}:v{version}/zombies/types/normal {{level:"$(level)"}}
""")

