""" The Treyarch BO1 health curve every enemy scales from. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_health_curve() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Treyarch BO1 HP curve: 50 + 100 x round up to round 9 (150 to 950), then 950 x 1.1^(round - 9),
	## converted with 2/15 (BO 150 HP = 20 HP, a vanilla zombie).
	write_versioned_function("zombies/calc_zombie_hp", f"""
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players operation #zb_hp {ns}.data *= #100 {ns}.data
execute if score #zb_round {ns}.data matches ..9 run scoreboard players add #zb_hp {ns}.data 50

execute if score #zb_round {ns}.data matches 10.. run scoreboard players operation #zb_exp_round {ns}.data = #zb_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run scoreboard players remove #zb_exp_round {ns}.data 9

execute if score #zb_round {ns}.data matches 10.. run data modify storage bs:in math.pow.x set value 1.1f
execute if score #zb_round {ns}.data matches 10.. store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round {ns}.data
execute if score #zb_round {ns}.data matches 10.. run function #bs.math:pow
execute if score #zb_round {ns}.data matches 10.. store result score #zb_hp {ns}.data run data get storage bs:out math.pow 950

scoreboard players operation #zb_hp {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_hp {ns}.data /= #15 {ns}.data

# Also catches int overflow on very high rounds.
execute unless score #zb_hp {ns}.data matches 15..3072 run scoreboard players set #zb_hp {ns}.data 3072
""")

	## Gives @s #zb_hp health: max_health stops at 1024, so the rest becomes absorption, and zb.max_hp keeps the whole
	## for damage dealt as a share of it.
	write_versioned_function("zombies/apply_zombie_hp", f"""
scoreboard players operation @s {ns}.zb.max_hp = #zb_hp {ns}.data

# A modifier over the type's default base: any NBT write on a wolf (a rise ending, an escort freezing it) puts its base back to 8.
attribute @s minecraft:max_health base reset
attribute @s minecraft:max_health modifier remove {ns}:round_hp
execute store result score #zb_hp_base {ns}.data run attribute @s minecraft:max_health base get
scoreboard players operation #zb_hp_add {ns}.data = #zb_hp {ns}.data
scoreboard players operation #zb_hp_add {ns}.data -= #zb_hp_base {ns}.data
execute store result storage {ns}:temp _zb_hp.val int 1 run scoreboard players get #zb_hp_add {ns}.data
function {ns}:v{version}/zombies/add_hp_modifier with storage {ns}:temp _zb_hp
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
function {ns}:v{version}/zombies/absorb_above_cap
""")
	write_versioned_function("zombies/add_hp_modifier", f"""
$attribute @s minecraft:max_health modifier add {ns}:round_hp $(val) add_value
""")

	## Run as an enemy whose zb.max_hp is set.
	write_versioned_function("zombies/absorb_above_cap", f"""
scoreboard players operation #zb_absorb {ns}.data = @s {ns}.zb.max_hp
scoreboard players remove #zb_absorb {ns}.data 1024
execute unless score #zb_absorb {ns}.data matches 1.. run return 0
execute store result storage {ns}:temp _zb_absorb.val int 1 run scoreboard players get #zb_absorb {ns}.data
function {ns}:v{version}/zombies/apply_zombie_absorption with storage {ns}:temp _zb_absorb
""")
	write_versioned_function("zombies/apply_zombie_absorption", """
$attribute @s minecraft:max_absorption base set $(val)
$data modify entity @s AbsorptionAmount set value $(val)f
""")

