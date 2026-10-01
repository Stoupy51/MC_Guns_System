""" Demolition: two bomb sites, both must fall, everyone respawns.

Modelled on Call of Duty's Demolition ([CoD Wiki](https://callofduty.fandom.com/wiki/Demolition_(Game_Mode))), which differs from Search & Destroy on every axis that matters:

- every attacker carries a bomb, at spawn and on every respawn, so there is nothing to pick up or drop;
- respawns are unlimited, so a wipe never wins a round and there is no "alive" bookkeeping;
- **both** sites must be destroyed, and a defuse does not end the round: attackers replant as often as needed;
- destroying a site adds time to the clock, and the clock stops while a bomb is down;
- each side attacks once; a 1-1 match is decided by a third round in which the top-killing side defends.

The map data is Search & Destroy's: both modes want exactly two marked objectives, and every shipped map defines them.
"""
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from ..sites import BombSites
from .rounds import ROUND_TICKS, DemoRounds
from .sites_state import DemoSites


# Classes
class Demolition(GameModeVariant):
	""" Demolition: attackers must destroy both bomb sites within the round clock; defenders hold them.
	Unlimited respawns, one attack per side, and a kill-seeded third round if the two halves split. """

	key = "demo"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Demolition! Destroy BOTH bomb sites, or hold them until time runs out.","color":"yellow"}}]

function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Round wins are the shared team score (#red, #blue on mp.team), which the sidebar and Final Score line read; multiplayer/start zeroes them.
scoreboard players set #demo_round {ns}.data 1

# 0 between rounds, so the 3 s gap judges nothing.
scoreboard players set #demo_round_active {ns}.data 0

# Claiming #mp_timer stops multiplayer/game_tick from counting it down or ending the match on it:
# this clock stops on a plant and grows on a destroy.
scoreboard players set #demo_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_mode_owns_timer {ns}.data 1

# From the same map points as Search & Destroy.
{BombSites.setup_lines(self, "search_and_destroy")}

# Sides depend on the map geometry; multiplayer/start summons the spawns before this setup.
function {ns}:v{version}/multiplayer/gamemodes/demo/pick_sides

function {ns}:v{version}/multiplayer/gamemodes/demo/start_round
""")

		BombSites.write_side_picking(self)
		BombSites.write_summoning(self)
		DemoRounds.write(self)
		DemoSites.write(self)

		self.sub("tick", f"""
# Rebuilt once a second: the attacking side and each site's state are text. Above the round gate, so the gap shows the new round.
execute store result score #demo_sb_tick {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #demo_sb_tick {ns}.data %= #20 {ns}.data
execute if score #demo_sb_tick {ns}.data matches 0 run function {ns}:v{version}/multiplayer/refresh_sidebar_demo

execute unless score #demo_round_active {ns}.data matches 1 run return 0

# Before the site channels, so a plant in progress overwrites it with its progress.
title @a[tag={ns}.demo_atk,gamemode=!spectator] actionbar [{{"text":"💣 ","color":"white"}},{{"text":"You are carrying a bomb - sneak at a site to plant","color":"gold"}}]

{DemoSites.tick_lines(self)}

# The clock stops while a site is planted: the attackers get room to defend their plant, and expiry never fires on a bomb already down.
execute unless entity @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] run scoreboard players operation #demo_timer {ns}.data -= #tick_delta {ns}.data

# Expiry with anything standing is a defensive hold, decider included, so every round awards a point.
execute if score #demo_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/demo/defenders_win

# The HUD score this mode claimed.
scoreboard players operation #mp_timer {ns}.data = #demo_timer {ns}.data
execute if score #mp_timer {ns}.data matches ..0 run scoreboard players set #mp_timer {ns}.data 0
""")

		## No team score from kills, only round wins.
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
""")

		## Runs before the gm_entity sweep of multiplayer/stop, so the world is restored from the site markers while they exist.
		self.sub("cleanup", f"""
schedule clear {ns}:v{version}/multiplayer/gamemodes/demo/start_round
{BombSites.cleanup_lines(self)}
kill @e[tag={ns}.demo_bomb]
kill @e[tag={ns}.demo_bomb_vis]
kill @e[tag={ns}.demo_bomb_hud]
kill @e[tag={ns}.demo_wreck]
kill @e[tag={ns}.demo_rubble]
tag @a remove {ns}.demo_atk
scoreboard players set #demo_round_active {ns}.data 0
""")


# Functions
def generate_demolition() -> None:
	""" Module-level entry point, mirroring the other gamemodes. """
	Demolition()()

