""" The bullet damage type, its signal function tags and the shared damage handoff. """
# Imports
from stewbeet import DamageType, LootTable, Mem, set_json_encoder, write_tag, write_versioned_function

from ...config.blocks import main as write_block_tags


# Functions
def write_damage_and_signals() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Add block tags
	write_block_tags()

	# Entity tags to ignore when shooting
	write_tag(f"{ns}:ignore", Mem.ctx.data.entity_type_tags, ["#bs.hitbox:intangible", "minecraft:interaction", "minecraft:experience_orb"])

	# Loot table for getting username
	Mem.ctx.data[ns].loot_tables["get_username"] = set_json_encoder(LootTable({
		"type": "minecraft:block",
		"pools": [
			{
				"rolls": 1,
				"bonus_rolls": 0,
				"entries": [
					{
						"type": "minecraft:item",
						"name": "minecraft:player_head",
						"functions": [
							{
								"function": "minecraft:fill_player_head",
								"entity": "this"
							}
						]
					}
				]
			}
		]
	}))

	## Register signal function tags (empty by default, other datapacks can add listeners) These are called at various events in the system, with relevant data stored in mgs:signals storage
	signal_events: list[str] = [
		"on_shoot",             # @s = shooter player, weapon data in mgs:signals
		"on_hit_block",         # @s = raycast marker, block/position/weapon in mgs:signals
		"on_reload",            # @s = reloading player, weapon data in mgs:signals
		"on_zoom",              # @s = zooming player, weapon data in mgs:signals
		"on_unzoom",            # @s = unzooming player, weapon data in mgs:signals
		"on_switch",            # @s = player, weapon data in mgs:signals
		"on_kill",              # @s = killer player, victim/weapon data in mgs:signals
		"damage",           # @s = damaged entity, damage/weapon/attacker in mgs:input with
		"on_explosion",         # @s = projectile entity, explosion data in mgs:signals
		"on_headshot",          # @s = hit entity, damage/weapon in mgs:signals
		"on_fire_mode_change",  # @s = player, weapon/new fire mode in mgs:signals
	]
	for event in signal_events:
		write_tag(f"signals/{event}", Mem.ctx.data[ns].function_tags, [])

	## Setup special damage type
	Mem.ctx.data[ns].damage_type["bullet"] = set_json_encoder(DamageType({"exhaustion": 0, "message_id": "player", "scaling": "when_caused_by_living_non_player"}))
	for tag in ["bypasses_cooldown", "no_knockback"]:
		write_tag(tag, Mem.ctx.data["minecraft"].damage_type_tags, [f"{ns}:bullet"])
	write_versioned_function("utils/damage", f"$damage $(target) $(amount) {ns}:bullet by $(attacker)")
	# Unattributed variant: no "by <attacker>", so team friendlyFire=false can't cancel it (used for self-inflicted explosion damage, where the shooter and victim share a team).
	write_versioned_function("utils/damage_plain", "$damage $(target) $(amount) minecraft:explosion")
	# Both signal_and_damage variants open with this: if the hit would kill a player who is in an active game, hand off to that mode's simulated death instead of letting the damage land.
	lethal_hit: str = f"if score #incoming_dmg {ns}.data >= #victim_hp {ns}.data run return run function {ns}:v{version}"
	lethal_handoff: str = f"""
# Check if target is a player in an active game and damage would be lethal -> simulate death
# (missions needs the state check: mi.in_game is an opt-in flag that is already set in the lobby)
execute store result score #incoming_dmg {ns}.data run data get storage {ns}:input with.amount 10
execute store result score #victim_hp {ns}.data run data get entity @s Health 10
execute if entity @s[type=player,scores={{{ns}.mp.in_game=1..}}] {lethal_hit}/multiplayer/simulate_death
execute if data storage {ns}:missions game{{state:"active"}} if entity @s[type=player,scores={{{ns}.mi.in_game=1..}}] {lethal_hit}/missions/simulate_death
""".strip()

	write_versioned_function("utils/signal_and_damage", f"""
{lethal_handoff}

# Non-lethal or non-MP: normal damage + signals
function {ns}:v{version}/utils/damage with storage {ns}:input with
function #{ns}:signals/damage with storage {ns}:input with
""")
	# Same flow as signal_and_damage but applies plain (unattributed) damage.
	write_versioned_function("utils/signal_and_damage_plain", f"""
{lethal_handoff}

# Non-lethal or non-MP: plain damage + signals
function {ns}:v{version}/utils/damage_plain with storage {ns}:input with
function #{ns}:signals/damage with storage {ns}:input with
""")

