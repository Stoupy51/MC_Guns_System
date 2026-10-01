""" Crawl input predicates, the downed-id predicate and the revive scoreboards. """
# Imports
from stewbeet import JsonDict, Mem, Predicate, set_json_encoder, write_load_file


# Functions
def write_revive_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Spectator inputs, which move the mannequin.
	def player_input(key: str) -> JsonDict:
		return {"type": "minecraft:entity_properties", "entity": "this", "predicate": {"minecraft:type_specific/player": {"input": {key: True}}}}
	Mem.ctx.data[ns].predicates[f"v{version}/input/forward"]  = set_json_encoder(Predicate(player_input("forward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/backward"] = set_json_encoder(Predicate(player_input("backward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/left"]     = set_json_encoder(Predicate(player_input("left")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/right"]    = set_json_encoder(Predicate(player_input("right")))

	## Matches the downed_id being processed, so one selector picks the mannequin, camera or HUD (as traps/turret_id_match).
	downed_id_ref: JsonDict = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#my_downed_id"}, "score": f"{ns}.data"}
	Mem.ctx.data[ns].predicates[f"v{version}/zombies/revive/downed_id_match"] = set_json_encoder(Predicate({
		"type": "minecraft:entity_scores",
		"entity": "this",
		"scores": {f"{ns}.zb.downed_id": {"min": downed_id_ref, "max": downed_id_ref}},
	}), max_level=-1)

	write_load_file(f"""
scoreboard objectives add {ns}.zb.downed dummy
scoreboard objectives add {ns}.zb.bleed dummy
scoreboard objectives add {ns}.zb.revive_p dummy

scoreboard objectives add {ns}.zb.qr_uses dummy

# Links a player to their mannequin.
scoreboard objectives add {ns}.zb.downed_id dummy
""")

