""" Search & Destroy: round-based bomb carry, plant and defuse, no respawns.

Modelled on Call of Duty's Search & Destroy, not on Counter-Strike's defusal.
CoD spawns one bomb in front of the attacking team; an attacker picks it up and carries it, and it drops where they die for another to retrieve.
Only the carrier can plant, and only at a marked site; Counter-Strike's economy, plant-anywhere zones and per-player bombs are absent.
"""
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

		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Search & Destroy! Carry the bomb to a site, or defend both!","color":"yellow"}}]

function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Round wins are the shared team score (#red, #blue on mp.team), which the sidebar and the Final Score line read.
# multiplayer/start already zeroes them.
scoreboard players set #snd_round {ns}.data 1
scoreboard players set #snd_win_threshold {ns}.data {WIN_ROUNDS}

# 0 loose or carried, 2 planted (bomb_timer is the fuse); plant and defuse progress are separate, so the fuse is never overwritten.
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0
scoreboard players set #snd_plant_progress {ns}.data 0
scoreboard players set #snd_defuse_progress {ns}.data 0

# 0 between rounds, when nobody carries snd_alive and the wipe checks would fire (see next_round).
scoreboard players set #snd_round_active {ns}.data 0

# The round timer also drives the HUD clock: claiming #mp_timer stops multiplayer/game_tick from counting it down and ending the match on it,
# since a 10-minute match limit cannot judge up to seven 2:30 rounds. start_round seeds the display.
scoreboard players set #snd_round_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_mode_owns_timer {ns}.data 1

{BombSites.setup_lines(self, "search_and_destroy")}

# Sides depend on the map geometry; multiplayer/start summons the spawns before this setup.
function {ns}:v{version}/multiplayer/gamemodes/snd/pick_sides

function {ns}:v{version}/multiplayer/gamemodes/snd/start_round
""")

		BombSites.write_side_picking(self)
		BombSites.write_summoning(self)
		SndRounds.write(self)
		SndCarry.write(self)

		self.sub("tick", f"""
# Rebuilt once a second: the attacking side and the bomb state are text, which no score component can show.
# Above the round gate, so the new round and swapped sides show during the 3 s gap.
execute store result score #snd_sb_tick {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #snd_sb_tick {ns}.data %= #20 {ns}.data
execute if score #snd_sb_tick {ns}.data matches 0 run function {ns}:v{version}/multiplayer/refresh_sidebar_snd

# Nothing to judge between rounds: next_round clears snd_alive, so every side would read as wiped.
execute unless score #snd_round_active {ns}.data matches 1 run return 0

scoreboard players operation #snd_round_timer {ns}.data -= #tick_delta {ns}.data

# Time out before a plant: defenders win.
execute if score #snd_round_timer {ns}.data matches ..0 if score #snd_bomb_state {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_timer {ns}.data -= #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_bomb_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_explodes

# The HUD shows the round clock, then the fuse once the bomb is down (the round timer stops mattering then).
# A plant with 20 s left therefore raises the displayed time to the 45 s fuse.
scoreboard players operation #mp_timer {ns}.data = #snd_round_timer {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #mp_timer {ns}.data = #snd_bomb_timer {ns}.data
execute if score #mp_timer {ns}.data matches ..0 run scoreboard players set #mp_timer {ns}.data 0

# A text_display resolves score components when its data is sent, so it would freeze at the planted value;
# rewriting on each whole second costs one NBT write a second.
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_sec {ns}.data = #snd_bomb_timer {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_sec {ns}.data /= #20 {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 unless score #snd_bomb_sec {ns}.data = #snd_bomb_sec_shown {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/snd/update_bomb_hud

# Attackers wiped before the plant: defenders win. After the plant someone still has to defuse.
execute store result score #snd_atk_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=1}}]
execute if score #snd_attackers {ns}.data matches 2 store result score #snd_atk_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=2}}]
execute if score #snd_atk_alive {ns}.data matches 0 if score #snd_bomb_state {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

# Defenders wiped: attackers win, planted or not, since nobody is left to defuse.
execute store result score #snd_def_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=2}}]
execute if score #snd_attackers {ns}.data matches 2 store result score #snd_def_alive {ns}.data if entity @a[tag={ns}.snd_alive,scores={{{ns}.mp.team=1}}]
execute if score #snd_def_alive {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/attackers_win

execute at @e[tag={ns}.snd_obj] run particle dust{{color:[1.0,0.6,0.0],scale:1.0}} ~ ~1 ~ 1.0 0.5 1.0 0 5

# The carrier's label follows them; see_through is off, so it does not reveal the carrier through walls (as in CoD).
execute as @a[tag={ns}.snd_carrier] at @s run tp @e[tag={ns}.snd_carrier_label,limit=1] ~ ~2.2 ~
title @a[tag={ns}.snd_carrier] actionbar [{{"text":"💣 ","color":"white"}},{{"text":"You have the bomb — plant at a site","color":"gold"}}]

# A carrier who disconnects leaves no bomb and no carrier, which would end the attack for the round; their label stays, so the bomb drops there.
execute if score #snd_bomb_state {ns}.data matches 0 unless entity @a[tag={ns}.snd_carrier] if entity @e[tag={ns}.snd_carrier_label] run function {ns}:v{version}/multiplayer/gamemodes/snd/recover_bomb

# Any living attacker walking over a loose bomb collects it.
execute if score #snd_bomb_state {ns}.data matches 0 unless entity @a[tag={ns}.snd_carrier] as @a[tag={ns}.snd_alive,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_loose_at,distance=..{PICKUP_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_pickup

# Only the carrier, sneaking at a site. The channeler only raises a flag; progress advances once here (see defuse).
scoreboard players set #snd_channeling {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 0 as @a[tag={ns}.snd_carrier,tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_obj,distance=..{SITE_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_plant
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_plant_progress {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_channeling {ns}.data matches 1 run scoreboard players operation #snd_plant_progress {ns}.data += #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_plant_progress {ns}.data matches {PLANT_TICKS}.. as @a[tag={ns}.snd_carrier,limit=1] at @s run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_planted

# Defender sneaking at the bomb; progress resets when nobody channels. The += lives here, not in try_defuse:
# per player, two defenders halved the defuse time. try_defuse marks the channelers, so bomb_defused knows who to pay.
scoreboard players set #snd_channeling {ns}.data 0
tag @a remove {ns}.{EARNER_TAG}
execute if score #snd_bomb_state {ns}.data matches 2 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_bomb,distance=..{SITE_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_defuse
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_defuse_progress {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 1 run scoreboard players operation #snd_defuse_progress {ns}.data += #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_defuse_progress {ns}.data matches {DEFUSE_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_defused
""")

		SndBomb.write(self)

		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
# No team score from kills, only round wins.
""")

		self.sub("on_death", f"""
# First, while the carrier tag and its label still exist.
execute if entity @s[tag={ns}.snd_carrier] run function {ns}:v{version}/multiplayer/gamemodes/snd/drop_bomb

# No respawn in S&D.
tag @s remove {ns}.snd_alive
gamemode spectator @s
""")

		## Runs before the gm_entity sweep of multiplayer/stop: the world is restored from the marker positions, so the markers must still exist.
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

