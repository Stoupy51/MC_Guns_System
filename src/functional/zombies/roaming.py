
# ruff: noqa: E501
# Shared primitives for "roaming" machines — placeables that exist at several map positions but keep
# only ONE active at a time and travel to another spot after a few uses (teddy-bear move animation).
# Both the Mystery Box (mystery_box.py) and Der Wunderfizz (wunderfizz.py) reuse these; each keeps its
# own move *animation* (a two-piece chest vs a single machine display) but shares the supporting bits:
#   - the teddy-bear head loot table (the Black-Ops move easter egg),
#   - the ±512 interaction hide/show trick (park a non-active box's interaction entity out of reach),
#   - the "should this use move the box?" roll (after N uses, 1-in-3 chance).
# Grayed-out "disabled" models for the inactive spots live in src/database/others.py; each machine
# summons its own disabled display (different transforms) using those shared models.
from stewbeet import LootTable, Mem, set_json_encoder, write_versioned_function

# Teddy bear player head texture (Black Ops easter egg) — the head that rises out of a box before it
# roams away. Shared by every roaming machine's move animation.
BEAR_HEAD_TEXTURE: str = "eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvY2RiNjZjZjlmMTdlMTQ4OTMxMGM3YWNjNjgxMDE2MDUxMTk2YTg0OGUwNzZkYjZmYzA5MzkxYjkyODcyYTc3NyJ9fX0="


def generate_roaming() -> None:
	ns: str = Mem.ctx.project_id

	# Teddy bear loot table (shared move easter egg). Referenced as mgs:zombies/roaming_bear.
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

	## Park an interaction entity out of reach / bring it back (@s = the interaction entity). Offset by
	## exactly ±512 blocks so its real position stays exact across moves. A hidden interaction entity
	## can't be hovered/clicked and can't eat a gun click at a dead box position.
	write_versioned_function("zombies/roaming/interaction_hide", f"""
tp @s ~ ~-512 ~
tag @s add {ns}.roam_hidden
""")
	write_versioned_function("zombies/roaming/interaction_show", f"""
tp @s ~ ~512 ~
tag @s remove {ns}.roam_hidden
""")

	## "Should this use move the box?" — after #roam_uses reaches #roam_threshold, roll 1-in-3.
	## Caller sets #roam_uses and #roam_threshold on {ns}.data beforehand; result in #roam_will_move
	## (0/1). Caller is responsible for any extra gating (active box only, not during a Fire Sale) and
	## for resetting its own use counter when a move happens.
	write_versioned_function("zombies/roaming/roll_move", f"""
scoreboard players set #roam_will_move {ns}.data 0
execute if score #roam_uses {ns}.data >= #roam_threshold {ns}.data store result score #roam_move_roll {ns}.data run random value 0..2
execute if score #roam_uses {ns}.data >= #roam_threshold {ns}.data if score #roam_move_roll {ns}.data matches 0 run scoreboard players set #roam_will_move {ns}.data 1
""")
