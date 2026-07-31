""" Search & Destroy: round-based bomb carry, plant and defuse, no respawns.

Modelled on Call of Duty's Search & Destroy, NOT on Counter-Strike's defusal. The difference that shapes
everything is the bomb: CoD spawns a single bomb in front of the attacking team, one attacker has to pick
it up and carry it, and it drops where they die for another attacker to retrieve. Only the carrier can
plant, and only at one of the marked sites. Counter-Strike's economy, its plant-anywhere-in-a-zone rule
and its per-player bomb spawns are all deliberately absent.
"""
# ruff: noqa: E501
# Imports
from .....helpers import MGS_TAG
from .....progression import EARNER_TAG
from ...base import GameModeVariant
from ..sites import BombSites
from .bomb import DEFUSE_TICKS, PLANT_TICKS, SITE_RANGE, SndBomb
from .carry import PICKUP_RANGE, SndCarry
from .rounds import ROUND_TICKS, WIN_ROUNDS, SndRounds


# Classes
class SearchAndDestroy(GameModeVariant):
	""" Search & Destroy: round-based; attackers carry a bomb to a site, defenders defuse it.
	No respawns within a round; first to WIN_ROUNDS round wins, with a side swap at halftime. """

	key = "snd"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## S&D Setup
		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Search & Destroy! Carry the bomb to a site, or defend both!","color":"yellow"}}]

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Round tracking. Round wins ARE the shared team score (#red / #blue on mp.team): the sidebar and the
# end-of-game "Final Score" line both read those, so keeping private win counters here meant S&D showed
# an empty sidebar all match and then announced a winner with "Red: 0 vs Blue: 0". multiplayer/start
# already zeroes both, so they are only read from here on.
scoreboard players set #snd_round {ns}.data 1
scoreboard players set #snd_win_threshold {ns}.data {WIN_ROUNDS}

# Bomb state: 0=loose or carried, 2=planted (bomb_timer = explosion countdown)
# Plant/defuse channel progress are tracked separately so the countdown is never clobbered
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0
scoreboard players set #snd_plant_progress {ns}.data 0
scoreboard players set #snd_defuse_progress {ns}.data 0

# Round gate. 0 means "no round in progress": between rounds nobody carries snd_alive, which makes the
# tick's "one whole side is dead" checks read as a wipe. See next_round.
scoreboard players set #snd_round_active {ns}.data 0

# Round timer. It also drives the HUD clock: claiming #mp_timer stops multiplayer/game_tick from both
# decrementing it and ending the match on it, because a 10-minute match limit cannot arbitrate a format
# that runs up to seven 2:30 rounds. start_round seeds the display.
scoreboard players set #snd_round_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_mode_owns_timer {ns}.data 1

# Summon objective markers (relative → absolute)
{BombSites.setup_lines(self, "search_and_destroy")}

# Decide sides from the map geometry, now that both the sites and the spawns exist
# (multiplayer/start runs summon_spawns before dispatching this setup)
function {ns}:v{version}/multiplayer/gamemodes/snd/pick_sides

# Start round
function {ns}:v{version}/multiplayer/gamemodes/snd/start_round
""")

		BombSites.write_side_picking(self)
		BombSites.write_summoning(self)
		SndRounds.write(self)
		SndCarry.write(self)

		## S&D Tick
		self.sub("tick", f"""
# Sidebar: rebuilt once a second because the attacking side and the bomb state are text, which no score
# component can express (same reason domination rebuilds instead of refreshing). Above the round gate on
# purpose, so the new round number and the swapped sides are on screen during the 3s gap that announces them.
execute store result score #snd_sb_tick {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #snd_sb_tick {ns}.data %= #20 {ns}.data
execute if score #snd_sb_tick {ns}.data matches 0 run function {ns}:v{version}/multiplayer/refresh_sidebar_snd

# Nothing to tick between rounds, and critically nothing to JUDGE: next_round clears snd_alive, so every
# check below would read one side as wiped during the 60-tick gap before start_round.
execute unless score #snd_round_active {ns}.data matches 1 run return 0

# Round timer
scoreboard players operation #snd_round_timer {ns}.data -= #tick_delta {ns}.data

# If timer runs out before the bomb is planted, defenders win
execute if score #snd_round_timer {ns}.data matches ..0 if score #snd_bomb_state {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

# If bomb planted, tick bomb timer
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_timer {ns}.data -= #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_bomb_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_explodes

# The HUD clock is the ROUND clock, and the bomb fuse from the moment the bomb goes down. The two can
# never fight over it: the plant stops the round timer from meaning anything (its expiry check above is
# gated on state 0), so whichever clock is authoritative is also the one being shown. A plant with 20s
# left therefore raises the displayed time to the 45s fuse, which is the point.
scoreboard players operation #mp_timer {ns}.data = #snd_round_timer {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #mp_timer {ns}.data = #snd_bomb_timer {ns}.data
execute if score #mp_timer {ns}.data matches ..0 run scoreboard players set #mp_timer {ns}.data 0

# Live countdown on the planted bomb. A score component would be wrong here: a text_display resolves its
# components when the entity data is sent, not continuously, so it would freeze at the planted value.
# Rewriting only when the whole second changes keeps that to one NBT write a second.
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_sec {ns}.data = #snd_bomb_timer {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_sec {ns}.data /= #20 {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 unless score #snd_bomb_sec {ns}.data = #snd_bomb_sec_shown {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/snd/update_bomb_hud

# Check if all attackers are dead (defenders win). Only BEFORE the plant: once the bomb is down, wiping
# the attackers is not enough on its own — someone still has to walk up and defuse it.
execute store result score #snd_atk_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=1}}]
execute if score #snd_attackers {ns}.data matches 2 store result score #snd_atk_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=2}}]
execute if score #snd_atk_alive {ns}.data matches 0 if score #snd_bomb_state {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

# Check if all defenders are dead (attackers win). Deliberately NOT gated on the bomb state: wiping the
# defenders wins the round outright, planted or not, because nobody is left who could ever defuse.
execute store result score #snd_def_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=2}}]
execute if score #snd_attackers {ns}.data matches 2 store result score #snd_def_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=1}}]
execute if score #snd_def_alive {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/attackers_win

# Particles at objectives
execute at @e[tag={ns}.snd_obj] run particle dust{{color:[1.0,0.6,0.0],scale:1.0}} ~ ~1 ~ 1.0 0.5 1.0 0 5

# Keep the carrier's bomb marker on their back, and remind them they are the one holding it.
# see_through is false on that label so it does NOT wallhack the carrier to the defenders: in CoD you spot
# the bomb on their model when you can already see them, you are not handed their position.
execute as @a[tag={ns}.snd_carrier] at @s run tp @e[tag={ns}.snd_carrier_label,limit=1] ~ ~2.2 ~
title @a[tag={ns}.snd_carrier] actionbar [{{"text":"💣 You have the bomb — plant at a site","color":"gold"}}]

# A carrier who disconnects takes the tag out of @a with them but leaves the bomb nowhere: no loose
# entity (pickup killed it) and no carrier to plant it, which silently ended the attack for the round.
# Their label is still standing where they logged out, so drop it there.
execute if score #snd_bomb_state {ns}.data matches 0 unless entity @a[tag={ns}.snd_carrier] if entity @e[tag={ns}.snd_carrier_label] run function {ns}:v{version}/multiplayer/gamemodes/snd/recover_bomb

# Loose bomb: any living attacker who walks over it collects it. No channel, no keypress.
execute if score #snd_bomb_state {ns}.data matches 0 unless entity @a[tag={ns}.snd_carrier] as @a[tag={ns}.snd_alive,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_loose_at,distance=..{PICKUP_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_pickup

# Planting (the CARRIER only, sneaking at a site). The channeler only raises a flag; the progress is
# advanced ONCE here, never inside the per-player function — see the defuse block below.
scoreboard players set #snd_channeling {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 0 as @a[tag={ns}.snd_carrier,tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_obj,distance=..{SITE_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_plant
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_plant_progress {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_channeling {ns}.data matches 1 run scoreboard players operation #snd_plant_progress {ns}.data += #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_plant_progress {ns}.data matches {PLANT_TICKS}.. as @a[tag={ns}.snd_carrier,limit=1] at @s run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_planted

# Defusing (defender near bomb and sneaking); progress resets if nobody is channeling.
# The += lives HERE and not in try_defuse on purpose: run per player, two defenders on the same bomb each
# added a tick_delta to the one shared progress score and halved the defuse time.
# try_defuse also marks each channeler, so bomb_defused knows who to pay without re-deriving the set.
scoreboard players set #snd_channeling {ns}.data 0
tag @a remove {ns}.{EARNER_TAG}
execute if score #snd_bomb_state {ns}.data matches 2 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_bomb,distance=..{SITE_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_defuse
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_defuse_progress {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 1 run scoreboard players operation #snd_defuse_progress {ns}.data += #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_defuse_progress {ns}.data matches {DEFUSE_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_defused
""")

		SndBomb.write(self)

		## S&D Kill Hook: No team scoring from kills, only round wins
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
# Remove snd_alive from dead player (dead players detected by death_count in on_respawn)
""")

		## S&D Death Hook: Mark dead (called from on_respawn override)
		self.sub("on_death", f"""
# Drop the bomb before anything else, while the carrier tag and its label are still around
execute if entity @s[tag={ns}.snd_carrier] run function {ns}:v{version}/multiplayer/gamemodes/snd/drop_bomb

# Remove alive tag (no respawn in S&D)
tag @s remove {ns}.snd_alive
# Set to spectator mode
gamemode spectator @s
""")

		## S&D Cleanup.
		## Runs BEFORE multiplayer/stop's gm_entity sweep (see game/stop.py), which is what the fill depends
		## on: it restores the world from the marker positions, so the markers have to still be alive here.
		self.sub("cleanup", f"""
schedule clear {ns}:v{version}/multiplayer/gamemodes/snd/start_round
{BombSites.cleanup_lines(self)}
kill @e[tag={ns}.snd_bomb]
kill @e[tag={ns}.snd_bomb_vis]
kill @e[tag={ns}.snd_bomb_hud]
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
tag @a remove {ns}.snd_carrier
tag @a remove {ns}.snd_alive
scoreboard players set #snd_round_active {ns}.data 0
""")


# Functions
def generate_search_and_destroy() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`SearchAndDestroy`. """
	SearchAndDestroy()()
