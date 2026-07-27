""" Losing every perk, the hover actionbar, solo Quick Revive pricing and the game hooks. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from .definitions import PERK_DEFINITIONS, perk_effects_teardown


# Functions
def write_perk_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	perk_reset_all_players: str = "\n".join(
		f"scoreboard players reset * {ns}.zb.perk.{perk_id}"
		for perk_id in PERK_DEFINITIONS
	)

	perkpaid_reset_all_players: str = "\n".join(
		f"scoreboard players reset * {ns}.zb.perkpaid.{perk_id}"
		for perk_id in PERK_DEFINITIONS
	)

	## Lose all perks: called when a player goes down
	lose_all_lines: list[str] = []
	for perk_id, perk_data in PERK_DEFINITIONS.items():
		removal = perk_data.removal_commands
		if removal:
			for cmd in removal:
				lose_all_lines.append(
					f"execute if score @s {ns}.zb.perk.{perk_id} matches 1 run {cmd.replace('{ns}', ns)}"
				)
		# Skip score reset for perks with persistent_score=True (e.g. quick_revive manages its own score)
		if not perk_data.persistent_score:
			lose_all_lines.append(f"scoreboard players set @s {ns}.zb.perk.{perk_id} 0")
	lose_all_body = "\n".join(lose_all_lines)
	write_versioned_function("zombies/perks/lose_all", f"""
# Remove all perk effects and reset scoreboard tracking
{lose_all_body}
tellraw @s [{MGS_TAG},{{"text":"All perks lost!","color":"red"}}]

# Remove the perk display items from the inventory right away
function {ns}:v{version}/zombies/inventory/refresh_perk_items
""")

	## Hover events (executor: "source" = player)
	perk_hover_message: str = (
		f'[{{"text":"🥤 ","color":"dark_purple"}},'
		f'{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#pk_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}}]'
	)
	# Chip-in machines show the next chunk plus the hovering player's own progress
	perk_hover_partial_message: str = (
		f'[{{"text":"🥤 ","color":"dark_purple"}},'
		f'{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},'
		f'{{"text":" - Chip in: ","color":"gray"}},'
		f'{{"score":{{"name":"#pk_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points (","color":"gray"}},'
		f'{{"score":{{"name":"#pk_paid","objective":"{ns}.data"}},"color":"green"}},'
		f'{{"text":"/","color":"gray"}},'
		f'{{"score":{{"name":"#pk_total","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":")","color":"gray"}}]'
	)
	write_versioned_function("zombies/perks/on_hover", f"""
execute store result storage {ns}:temp _pk_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_hover
function {ns}:v{version}/zombies/perks/get_hover_name
function {ns}:v{version}/zombies/perks/read_price with storage {ns}:temp _pk_data
execute unless score #pk_partial {ns}.data matches 1.. run data modify storage smithed.actionbar:input message set value {{json:{perk_hover_message},priority:"conditional",freeze:5}}
execute if score #pk_partial {ns}.data matches 1.. run data modify storage smithed.actionbar:input message set value {{json:{perk_hover_partial_message},priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	## Hook into game start: reset perk scoreboards
	map_pool_reset: str = "\n".join(
		f"scoreboard players set #map_perk_{perk_id} {ns}.data 0"
		for perk_id in PERK_DEFINITIONS
	)
	write_versioned_function("zombies/start", f"""
# Reset perk scoreboards for all known score holders (including offline players).
{perk_reset_all_players}

# Chip-in progress never carries between games
{perkpaid_reset_all_players}

# Shared random-perk pool: clear the "perk present on map" flags (repopulated by perks/setup)
{map_pool_reset}

# Clean slate for the joining players: perk effects survive a game that ended without a proper stop,
# and the special.* scores can just as well have come from a multiplayer class or the debug menu.
{perk_effects_teardown(ns, f"@a[scores={{{ns}.zb.in_game=1}}]")}
""")

	## Quick Revive solo pricing: 500 when alone, map price otherwise. Re-checked on join/leave.
	write_versioned_function("zombies/perks/update_quick_revive_price", f"""
# Count alive in-game players
execute store result score #qr_players {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]

# Solo (or none): discounted to 500
execute if score #qr_players {ns}.data matches ..1 run scoreboard players set @e[tag={ns}.pk_quick_revive] {ns}.zb.perk.price 500

# Two or more: restore each machine's map-defined price
execute if score #qr_players {ns}.data matches 2.. as @e[tag={ns}.pk_quick_revive] run scoreboard players operation @s {ns}.zb.perk.price = @s {ns}.zb.perk.base_price
""")

	## Hook into preload_complete: setup perk machines
	write_versioned_function("zombies/preload_complete", f"""
# Setup perk machines
execute if data storage {ns}:zombies game.map.perks[0] run function {ns}:v{version}/zombies/perks/setup

# Apply initial Quick Revive solo pricing
execute if data storage {ns}:zombies game.map.perks[0] run function {ns}:v{version}/zombies/perks/update_quick_revive_price
""")

	## Hook into game tick: keep Quick Revive solo price in sync as players join/leave (every ~1s)
	write_versioned_function("zombies/game_tick", f"""
scoreboard players add #qr_price_tick {ns}.data 1
execute if score #qr_price_tick {ns}.data matches 20.. run scoreboard players set #qr_price_tick {ns}.data 0
execute if score #qr_price_tick {ns}.data matches 0 run function {ns}:v{version}/zombies/perks/update_quick_revive_price
""")

	# Remove perk effects on stop. game.py's stop hook has already zeroed zb.in_game, so a score selector here matches nobody.
	# The zombies team is never left, so it is what still identifies the torn-down game's players.
	write_versioned_function("zombies/stop", f"""
# Reset perk effects
{perk_effects_teardown(ns, f"@a[team={ns}.zombies]")}

# Reset perk scoreboards for all known score holders (including offline players).
{perk_reset_all_players}
{perkpaid_reset_all_players}
""")

