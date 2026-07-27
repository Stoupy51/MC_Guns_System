""" Shared primitives for "roaming" machines: placeables existing at several map positions that keep
only ONE active at a time and travel after a few uses.

The Mystery Box (mystery_box.py) and Der Wunderfizz (wunderfizz.py) each keep their own move
animation but share the teddy-bear head loot table, the ±512 interaction hide/show trick, and the
"should this use move the box?" roll. Grayed-out disabled models live in src/database/items.py.
"""
# ruff: noqa: E501
from stewbeet import LootTable, Mem, set_json_encoder, write_versioned_function

BEAR_HEAD_TEXTURE: str = "eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvY2RiNjZjZjlmMTdlMTQ4OTMxMGM3YWNjNjgxMDE2MDUxMTk2YTg0OGUwNzZkYjZmYzA5MzkxYjkyODcyYTc3NyJ9fX0="
""" Teddy bear player head (Black Ops easter egg): the head that rises out of a box before it roams. """

def generate_roaming() -> None:
	ns: str = Mem.ctx.project_id

	# Teddy bear loot table, referenced as mgs:zombies/roaming_bear
	Mem.ctx.data[ns].loot_tables["zombies/roaming_bear"] = set_json_encoder(LootTable({
		"pools": [{
			"rolls": 1,
			"entries": [{
				"type": "minecraft:item",
				"name": "minecraft:player_head",
				"functions": [{
					"function": "minecraft:set_components",
					"components": {
						"minecraft:profile": {
							"properties": [{
								"name": "textures",
								"value": BEAR_HEAD_TEXTURE,
							}],
						},
					},
				}],
			}],
		}],
	}))

	# Park an interaction entity out of reach and back (@s = the interaction entity).
	# Exactly ±512 blocks so its real position stays exact; hidden ones can't be clicked or eat a gun click.
	write_versioned_function("zombies/roaming/interaction_hide", f"""
tp @s ~ ~-512 ~
tag @s add {ns}.roam_hidden
""")
	write_versioned_function("zombies/roaming/interaction_show", f"""
tp @s ~ ~512 ~
tag @s remove {ns}.roam_hidden
""")

	# Roll 1-in-3 once #roam_uses reaches #roam_threshold; result in #roam_will_move (0/1).
	# The caller sets both scores, does its own extra gating, and resets its use counter on a move.
	write_versioned_function("zombies/roaming/roll_move", f"""
scoreboard players set #roam_will_move {ns}.data 0
execute if score #roam_uses {ns}.data >= #roam_threshold {ns}.data store result score #roam_move_roll {ns}.data run random value 0..2
execute if score #roam_uses {ns}.data >= #roam_threshold {ns}.data if score #roam_move_roll {ns}.data matches 0 run scoreboard players set #roam_will_move {ns}.data 1
""")

