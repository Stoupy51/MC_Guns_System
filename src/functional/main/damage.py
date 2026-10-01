""" The bullet damage type, its signal function tags and the shared damage handoff. """
# Imports
from stewbeet import (
	DamageType,
	LootTable,
	Mem,
	set_json_encoder,
	write_tag,
	write_versioned_function,
)

from ...config.blocks import main as write_block_tags


# Functions
def write_damage_and_signals() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_block_tags()

	# Ignored by shots.
	write_tag(f"{ns}:ignore", Mem.ctx.data.entity_type_tags, ["#bs.hitbox:intangible", "minecraft:interaction", "minecraft:experience_orb"])

	# Gives a player_head with the player's profile, for usernames.
	Mem.ctx.data[ns].loot_tables["get_username"] = set_json_encoder(LootTable({
		"type": "minecraft:chest",
		"pools": [
			{
				"rolls": 1,
				"bonus_rolls": 0,
				"entries": [
					{
						"type": "minecraft:item",
						"name": "minecraft:player_head",
						"modifier": [
							{
								"type": "minecraft:fill_player_head",
								"entity": "this"
							}
						]
					}
				]
			}
		]
	}))

	## Signal tags, empty by default for other datapacks to add listeners; event data goes to mgs:signals.
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

	## Bullet damage type.
	Mem.ctx.data[ns].damage_type["bullet"] = set_json_encoder(DamageType({"exhaustion": 0, "message_id": "player", "scaling": "when_caused_by_living_non_player"}))
	for tag in ["bypasses_cooldown", "no_knockback"]:
		write_tag(tag, Mem.ctx.data["minecraft"].damage_type_tags, [f"{ns}:bullet"])
	write_versioned_function("utils/damage", f"$damage $(target) $(amount) {ns}:bullet by $(attacker)")
	# Unattributed, so team friendlyFire=false cannot cancel it (self-inflicted explosions, where shooter and victim share a team).
	write_versioned_function("utils/damage_plain", "$damage $(target) $(amount) minecraft:explosion")
	# A hit that would kill a player in an active game hands off to that mode's simulated death instead.
	lethal_hit: str = f"if score #incoming_dmg {ns}.data >= #victim_hp {ns}.data run return run function {ns}:v{version}"
	lethal_handoff: str = f"""
# Missions needs the state check: mi.in_game is an opt-in flag already set in the lobby.
execute store result score #incoming_dmg {ns}.data run data get storage {ns}:input with.amount 10
execute store result score #victim_hp {ns}.data run data get entity @s Health 10
execute if entity @s[type=player,scores={{{ns}.mp.in_game=1..}}] {lethal_hit}/multiplayer/simulate_death
execute if data storage {ns}:missions game{{state:"active"}} if entity @s[type=player,scores={{{ns}.mi.in_game=1..}}] {lethal_hit}/missions/simulate_death
""".strip()

	write_versioned_function("utils/signal_and_damage", f"""
{lethal_handoff}

# Otherwise normal damage and signals.
function {ns}:v{version}/utils/damage with storage {ns}:input with
function #{ns}:signals/damage with storage {ns}:input with
""")
	# Same flow with plain, unattributed damage.
	write_versioned_function("utils/signal_and_damage_plain", f"""
{lethal_handoff}

# Otherwise plain damage and signals.
function {ns}:v{version}/utils/damage_plain with storage {ns}:input with
function #{ns}:signals/damage with storage {ns}:input with
""")

