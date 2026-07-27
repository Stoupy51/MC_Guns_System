""" Crawl input predicates, the downed-id predicate and the revive scoreboards. """
# ruff: noqa: E501
# Imports
from stewbeet import JsonDict, Mem, Predicate, set_json_encoder, write_load_file


# Functions
def write_revive_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Input predicates (used to move the mannequin via spectator player input)
	def player_input(key: str) -> JsonDict:
		return {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"minecraft:type_specific/player": {"input": {key: True}}}}
	Mem.ctx.data[ns].predicates[f"v{version}/input/forward"]  = set_json_encoder(Predicate(player_input("forward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/backward"] = set_json_encoder(Predicate(player_input("backward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/left"]     = set_json_encoder(Predicate(player_input("left")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/right"]    = set_json_encoder(Predicate(player_input("right")))

	## Predicate: does `this` entity's downed_id match the downed player currently being processed?
	## Lets a selector pick the matching mannequin/cam/hud directly via predicate=... instead of `as @e[tag=...] if score @s {ns}.zb.downed_id = #my_downed_id ...` — one selector pass, the id test folded into selection (same trick as zombies/traps/turret_id_match).
	downed_id_ref: JsonDict = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#my_downed_id"}, "score": f"{ns}.data"}
	Mem.ctx.data[ns].predicates[f"v{version}/zombies/revive/downed_id_match"] = set_json_encoder(Predicate({
		"condition": "minecraft:entity_scores",
		"entity": "this",
		"scores": {f"{ns}.zb.downed_id": {"min": downed_id_ref, "max": downed_id_ref}},
	}), max_level=-1)
	Mem.ctx.data[ns].predicates[f"v{version}/input/any"]      = set_json_encoder(Predicate({"condition": "minecraft:any_of", "terms": [player_input("forward"), player_input("backward"), player_input("left"), player_input("right")]}))

	## Scoreboards
	write_load_file(f"""
# Revive system scoreboards
scoreboard objectives add {ns}.zb.downed dummy
scoreboard objectives add {ns}.zb.bleed dummy
scoreboard objectives add {ns}.zb.revive_p dummy

# Solo Quick Revive uses remaining
scoreboard objectives add {ns}.zb.qr_uses dummy

# Unique downed ID: links player to their specific mannequin
scoreboard objectives add {ns}.zb.downed_id dummy
""")

