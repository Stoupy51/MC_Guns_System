""" Demolition: two bomb sites, both must fall, everyone respawns.

Modelled on Call of Duty's Demolition ([CoD Wiki](https://callofduty.fandom.com/wiki/Demolition_(Game_Mode))),
which differs from Search & Destroy on every axis that matters:

- every attacker carries a bomb, at spawn and on every respawn, so there is nothing to pick up or drop
- respawns are unlimited, so a wipe never wins a round and there is no "alive" bookkeeping
- **both** sites must be destroyed, and a defuse does not end the round — attackers replant as often as needed
- destroying a site adds time to the clock, and the clock stops entirely while a bomb is down
- each side attacks once; a 1-1 (or 0-0) match is decided by a sudden-death round on one neutral site

The map data is Search & Destroy's: both modes want exactly two marked objectives, and every shipped map
already defines them. Only the map editor's item label mentions both modes.
"""
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from ..sites import BombSites
from .rounds import OVERTIME_ROUND, ROUND_TICKS, ROUNDS_PER_MATCH, DemoRounds
from .sites_state import DemoSites


# Classes
class Demolition(GameModeVariant):
	""" Demolition: attackers must destroy both bomb sites within the round clock; defenders hold them.
	Unlimited respawns, two halves, sudden death on a neutral site if the halves split. """

	key = "demo"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## Demolition Setup
		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Demolition! Destroy BOTH bomb sites, or hold them until time runs out.","color":"yellow"}}]

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Round wins ARE the shared team score (#red / #blue on mp.team), which is what the sidebar and the
# end-of-game "Final Score" line read. multiplayer/start already zeroes both.
scoreboard players set #demo_round {ns}.data 1

# Round gate. 0 means "no round in progress", so the 3s gap between rounds judges nothing.
scoreboard players set #demo_round_active {ns}.data 0

# Claiming #mp_timer stops multiplayer/game_tick from decrementing it or ending the match on it: this
# mode's clock stops on a plant and grows on a destroy, neither of which a match time limit can express.
scoreboard players set #demo_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_mode_owns_timer {ns}.data 1

# Summon objective markers (relative → absolute), from the same map points Search & Destroy uses
{BombSites.setup_lines(self, "search_and_destroy")}

# Decide sides from the map geometry, now that both the sites and the spawns exist
# (multiplayer/start runs summon_spawns before dispatching this setup)
function {ns}:v{version}/multiplayer/gamemodes/demo/pick_sides

# Start round
function {ns}:v{version}/multiplayer/gamemodes/demo/start_round
""")

		BombSites.write_side_picking(self)
		BombSites.write_summoning(self)
		DemoRounds.write(self)
		DemoSites.write(self)

		## Demolition Tick
		self.sub("tick", f"""
# Sidebar: rebuilt once a second because the attacking side and each site's state are text, which no score
# component can express. Above the round gate so the new round and the swapped sides show during the gap.
execute store result score #demo_sb_tick {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #demo_sb_tick {ns}.data %= #20 {ns}.data
execute if score #demo_sb_tick {ns}.data matches 0 run function {ns}:v{version}/multiplayer/refresh_sidebar_demo

# Nothing to tick, and nothing to judge, between rounds
execute unless score #demo_round_active {ns}.data matches 1 run return 0

{DemoSites.tick_lines(self)}

# The clock stops dead while any site is planted — that is the rule that gives the attackers room to
# defend their own plant, and it also means the expiry below can never fire on a bomb already down.
execute unless entity @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] run scoreboard players operation #demo_timer {ns}.data -= #tick_delta {ns}.data

# Expiry means a defensive hold in regulation — but overtime has no defenders, so there is nobody to award
# it to: #demo_attackers still names whoever attacked in the second half, and crediting that side would
# have put a phantom round win in the final score of what is really a draw.
execute if score #demo_timer {ns}.data matches ..0 if score #demo_round {ns}.data matches ..{ROUNDS_PER_MATCH} run function {ns}:v{version}/multiplayer/gamemodes/demo/defenders_win
execute if score #demo_timer {ns}.data matches ..0 if score #demo_round {ns}.data matches {OVERTIME_ROUND}.. run function {ns}:v{version}/multiplayer/gamemodes/demo/overtime_expired

# Mirror the round clock onto the HUD score this mode claimed
scoreboard players operation #mp_timer {ns}.data = #demo_timer {ns}.data
execute if score #mp_timer {ns}.data matches ..0 run scoreboard players set #mp_timer {ns}.data 0

# Remind the armed side what they are holding
title @a[tag={ns}.demo_atk,gamemode=!spectator] actionbar [{{"text":"💣 You are carrying a bomb — plant at a site","color":"gold"}}]
""")

		## Demolition Kill Hook: no team scoring from kills, only round wins
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
""")

		## Demolition Cleanup.
		## Runs BEFORE multiplayer/stop's gm_entity sweep (see game/stop.py) so the fill can restore the
		## world from the site markers while they are still alive.
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
