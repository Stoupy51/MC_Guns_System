""" Search & Destroy: round-based bomb plant and defuse, no respawns. """
# ruff: noqa: E501
# Imports
from ...helpers import MGS_TAG
from .base import GameModeVariant


# Classes
class SearchAndDestroy(GameModeVariant):
	""" Search & Destroy: round-based; attackers plant a bomb, defenders defuse it.
	No respawns within a round; best-of-six with a side swap at halftime. """

	key = "snd"

	def generate(self) -> None:
		ns: str = self.ns
		version: str = self.version

		## S&D Setup
		self.sub("setup", f"""
tellraw @a [{MGS_TAG},{{"text":"Search & Destroy! Attackers plant, defenders defuse!","color":"yellow"}}]

# Store base coordinates for offset
function {ns}:v{version}/shared/load_base_coordinates {{mode:"multiplayer"}}

# Round tracking. Round wins ARE the shared team score (#red / #blue on mp.team): the sidebar and the
# end-of-game "Final Score" line both read those, so keeping private win counters here meant S&D showed
# an empty sidebar all match and then announced a winner with "Red: 0 vs Blue: 0". multiplayer/start
# already zeroes both, so they are only read from here on.
scoreboard players set #snd_round {ns}.data 1
scoreboard players set #snd_max_rounds {ns}.data 6

# Bomb state: 0=not planted, 2=planted (bomb_timer = explosion countdown)
# Plant/defuse channel progress are tracked separately so the countdown is never clobbered
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0
scoreboard players set #snd_plant_progress {ns}.data 0
scoreboard players set #snd_defuse_progress {ns}.data 0

# Round gate. 0 means "no round in progress": between rounds nobody carries snd_alive, which makes the
# tick's "one whole side is dead" checks read as a wipe. See next_round.
scoreboard players set #snd_round_active {ns}.data 0

# Round timer (90 seconds = 1800 ticks)
scoreboard players set #snd_round_timer {ns}.data 1800

# Summon objective markers (relative → absolute)
scoreboard players set #snd_site_idx {ns}.data 0
data modify storage {ns}:temp _snd_iter set from storage {ns}:multiplayer game.map.search_and_destroy
execute if data storage {ns}:temp _snd_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/snd/summon_obj

# Decide sides from the map geometry, now that both the sites and the spawns exist
# (multiplayer/start runs summon_spawns before dispatching this setup)
function {ns}:v{version}/multiplayer/gamemodes/snd/pick_sides

# Start round
function {ns}:v{version}/multiplayer/gamemodes/snd/start_round
""")

		## S&D: Choose which side defends — whoever spawns closest to the bomb sites.
		## Hardcoding Red as attackers put the attackers on top of the objective on roughly half of all
		## maps, which removes the entire point of the mode: the defenders are supposed to hold ground they
		## start next to, and the attackers are supposed to cross the map to reach it.
		self.sub("pick_sides", f"""
# Tally, per bomb site, which team owns the spawn point closest to it.
scoreboard players set #snd_near_red {ns}.data 0
scoreboard players set #snd_near_blue {ns}.data 0
execute as @e[tag={ns}.snd_obj] at @s run function {ns}:v{version}/multiplayer/gamemodes/snd/tally_site

# Attackers are whichever side did NOT win that tally. A tie keeps Red attacking, the CoD default.
scoreboard players set #snd_attackers {ns}.data 1
execute if score #snd_near_red {ns}.data > #snd_near_blue {ns}.data run scoreboard players set #snd_attackers {ns}.data 2
""")

		## S&D: @s = one bomb site, at it. Credit the site to the team owning the nearest spawn point.
		## General spawns are excluded: they say nothing about which side holds this ground.
		self.sub("tally_site", f"""
execute as @e[tag={ns}.spawn_point,tag=!{ns}.spawn_general,limit=1,sort=nearest] run function {ns}:v{version}/multiplayer/gamemodes/snd/tally_site_spawn
""")

		self.sub("tally_site_spawn", f"""
execute if entity @s[tag={ns}.spawn_red] run scoreboard players add #snd_near_red {ns}.data 1
execute if entity @s[tag={ns}.spawn_blue] run scoreboard players add #snd_near_blue {ns}.data 1
""")

		## S&D: Summon objective markers (relative → absolute)
		self.sub("summon_obj", f"""
execute store result score #rx {ns}.data run data get storage {ns}:temp _snd_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _snd_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _snd_iter[0][2]
scoreboard players operation #rx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ry {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #rz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _snd_pos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _snd_pos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _snd_pos.z double 1 run scoreboard players get #rz {ns}.data

# Site letter, same scheme as domination's zone labels
execute if score #snd_site_idx {ns}.data matches 0 run data modify storage {ns}:temp _snd_pos.label set value "A"
execute if score #snd_site_idx {ns}.data matches 1 run data modify storage {ns}:temp _snd_pos.label set value "B"
execute if score #snd_site_idx {ns}.data matches 2 run data modify storage {ns}:temp _snd_pos.label set value "C"
execute if score #snd_site_idx {ns}.data matches 3 run data modify storage {ns}:temp _snd_pos.label set value "D"
scoreboard players add #snd_site_idx {ns}.data 1

function {ns}:v{version}/multiplayer/gamemodes/snd/summon_obj_at with storage {ns}:temp _snd_pos
data remove storage {ns}:temp _snd_iter[0]
execute if data storage {ns}:temp _snd_iter[0] run function {ns}:v{version}/multiplayer/gamemodes/snd/summon_obj
""")

		## The floating letter is what domination has and S&D did not: without it the sites are an unmarked
		## chest, so neither side can tell where the objective is without being told out of band.
		self.sub("summon_obj_at", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.snd_obj","{ns}.gm_entity","{ns}.snd_site_$(label)"]}}
$summon minecraft:text_display $(x) $(y) $(z) {{Tags:["{ns}.snd_label","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 ","color":"gold"}},{{"text":"$(label)","color":"yellow","bold":true}}],transformation:{{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ chest
$execute positioned $(x) $(y) $(z) run setblock ~ ~1 ~ barrier
""")

		## S&D: Start Round
		self.sub("start_round", f"""
# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage {ns}:multiplayer game{{state:"lobby"}} run return fail
execute if data storage {ns}:multiplayer game{{state:"ended"}} run return fail

# Announce round
tellraw @a [{MGS_TAG},{{"text":"────── Round ","color":"gold"}},{{"score":{{"name":"#snd_round","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" ──────","color":"gold"}}]

# Show which team attacks
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" attacks | "}},{{"text":"Blue","color":"blue"}},{{"text":" defends"}}]
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" attacks | "}},{{"text":"Red","color":"red"}},{{"text":" defends"}}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Reset bomb state and channel progress
scoreboard players set #snd_bomb_state {ns}.data 0
scoreboard players set #snd_bomb_timer {ns}.data 0
scoreboard players set #snd_plant_progress {ns}.data 0
scoreboard players set #snd_defuse_progress {ns}.data 0

# Reset round timer
scoreboard players set #snd_round_timer {ns}.data 1800

# Restore players who died last round (S&D deaths skip the respawn countdown)
execute as @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={{{ns}.mp.team=1..2}},gamemode=spectator]

# Tag alive players
tag @a[scores={{{ns}.mp.team=1..2}},gamemode=!spectator] add {ns}.snd_alive

# Teleport everyone to their team spawns and re-apply class loadouts
execute as @a[scores={{{ns}.mp.team=1}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"red"}}
execute as @a[scores={{{ns}.mp.team=2}}] at @s run function {ns}:v{version}/multiplayer/pick_spawn {{type:"blue"}}
tag @e[tag={ns}.spawn_used] remove {ns}.spawn_used
execute as @a[scores={{{ns}.mp.team=1..2}}] at @s run function {ns}:v{version}/multiplayer/apply_class

# Open the round LAST, once everyone is alive-tagged and placed. Until this is 1 the tick judges nothing,
# so the gap between rounds can never be mistaken for a team wipe.
scoreboard players set #snd_round_active {ns}.data 1
""")

		## S&D Tick
		self.sub("tick", f"""
# Nothing to tick between rounds, and critically nothing to JUDGE: next_round clears snd_alive, so every
# check below would read one side as wiped during the 60-tick gap before start_round.
execute unless score #snd_round_active {ns}.data matches 1 run return 0

# Round timer
scoreboard players operation #snd_round_timer {ns}.data -= #tick_delta {ns}.data

# If timer runs out before the bomb is planted, defenders win
execute if score #snd_round_timer {ns}.data matches ..0 if score #snd_bomb_state {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win

# If bomb planted, tick bomb timer (45 seconds = 900 ticks)
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_timer {ns}.data -= #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_bomb_timer {ns}.data matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_explodes

# Live countdown on the planted bomb. A score component would be wrong here: a text_display resolves its
# components when the entity data is sent, not continuously, so it would freeze at the planted value.
# Rewriting only when the whole second changes keeps that to one NBT write a second.
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_sec {ns}.data = #snd_bomb_timer {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 run scoreboard players operation #snd_bomb_sec {ns}.data /= #20 {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 unless score #snd_bomb_sec {ns}.data = #snd_bomb_sec_shown {ns}.data run function {ns}:v{version}/multiplayer/gamemodes/snd/update_bomb_hud

# Check if all attackers are dead (defenders win)
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

# Check planting (attacker near objective and sneaking); progress resets if nobody is channeling
scoreboard players set #snd_channeling {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 0 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_obj,distance=..3] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_plant
execute if score #snd_bomb_state {ns}.data matches 0 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_plant_progress {ns}.data 0

# Check defusing (defender near bomb and sneaking); progress resets if nobody is channeling
scoreboard players set #snd_channeling {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 2 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_bomb,distance=..3] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_defuse
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_defuse_progress {ns}.data 0
""")

		## S&D: Plant attempt
		self.sub("try_plant", f"""
# Only attackers can plant
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 1 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 2 run return fail

# Continue planting (5 seconds = 100 ticks)
scoreboard players set #snd_channeling {ns}.data 1
scoreboard players operation #snd_plant_progress {ns}.data += #tick_delta {ns}.data
title @s actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#snd_plant_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/100"}}]

# If planted
execute if score #snd_plant_progress {ns}.data matches 100.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_planted
""")

		## S&D: Bomb planted
		self.sub("bomb_planted", f"""
scoreboard players set #snd_bomb_state {ns}.data 2
scoreboard players set #snd_bomb_timer {ns}.data 900
scoreboard players set #snd_plant_progress {ns}.data 0

# Force the countdown label to be written on the very next tick
scoreboard players set #snd_bomb_sec_shown {ns}.data -1

# The marker is the logic anchor (defuse range, explosion origin) and is invisible, which is why planting
# used to change nothing on screen. The block_display is the bomb players actually see and the text
# display carries the countdown, so both sides can read the state of the round from across the room.
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.snd_bomb","{ns}.gm_entity"]}}
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.snd_bomb_vis","{ns}.gm_entity"],block_state:{{Name:"minecraft:tnt"}},transformation:{{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_bomb_hud","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 PLANTED","color":"red","bold":true}}],transformation:{{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}

tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB PLANTED!","color":"red","bold":true}}]
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5
""")

		## S&D: rewrite the bomb countdown label (only called when the displayed second changes)
		self.sub("update_bomb_hud", f"""
scoreboard players operation #snd_bomb_sec_shown {ns}.data = #snd_bomb_sec {ns}.data
execute store result storage {ns}:temp _snd_hud.sec int 1 run scoreboard players get #snd_bomb_sec {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/snd/set_bomb_hud with storage {ns}:temp _snd_hud
""")

		## Selected by tag rather than @n: this runs from the mode tick, which has no meaningful position.
		self.sub("set_bomb_hud", f"""
$data modify entity @e[tag={ns}.snd_bomb_hud,limit=1] text set value [{{"text":"💣 ","color":"red","bold":true}},{{"text":"$(sec)s","color":"white"}}]
""")

		## S&D: Defuse attempt
		self.sub("try_defuse", f"""
# Only defenders can defuse
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 2 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 1 run return fail

# Continue defusing (7.5 seconds = 150 ticks); the bomb countdown keeps running in parallel
scoreboard players set #snd_channeling {ns}.data 1
scoreboard players operation #snd_defuse_progress {ns}.data += #tick_delta {ns}.data
title @s actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#snd_defuse_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/150"}}]

execute if score #snd_defuse_progress {ns}.data matches 150.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_defused
""")

		## S&D: Bomb defused → defenders win
		self.sub("bomb_defused", f"""
tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB DEFUSED!","color":"aqua","bold":true}}]
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win
""")

		## S&D: Bomb explodes → attackers win
		self.sub("bomb_explodes", f"""
# Explosion effect at bomb
execute at @e[tag={ns}.snd_bomb] run particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
execute at @e[tag={ns}.snd_bomb] run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8

# Simulate death for any players near the bomb (10 block radius)
execute at @e[tag={ns}.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run data modify storage {ns}:input with set value {{}}
execute at @e[tag={ns}.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run function {ns}:v{version}/multiplayer/simulate_death

tellraw @a [{MGS_TAG},"💥 ",{{"text":"BOMB EXPLODED!","color":"red","bold":true}}]
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/attackers_win
""")

		## S&D: Attackers win round
		self.sub("attackers_win", f"""
# Close the round exactly once. Several end conditions can come true on the same tick (a defuse that
# also wipes a side, a timeout landing with the last kill), and each one calls in here.
execute unless score #snd_round_active {ns}.data matches 1 run return fail
scoreboard players set #snd_round_active {ns}.data 0

execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #red {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" (Attackers) win the round!","color":"yellow"}}]
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #blue {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" (Attackers) win the round!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

		## S&D: Defenders win round
		self.sub("defenders_win", f"""
# Same single-shot guard as attackers_win — this is the path the defuse takes, and the defuse used to be
# immediately followed by four attacker wins as the wiped-looking alive tags were judged tick after tick.
execute unless score #snd_round_active {ns}.data matches 1 run return fail
scoreboard players set #snd_round_active {ns}.data 0

execute if score #snd_attackers {ns}.data matches 1 run scoreboard players add #blue {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 1 run tellraw @a [{MGS_TAG},{{"text":"Blue","color":"blue"}},{{"text":" (Defenders) win the round!","color":"yellow"}}]
execute if score #snd_attackers {ns}.data matches 2 run scoreboard players add #red {ns}.mp.team 1
execute if score #snd_attackers {ns}.data matches 2 run tellraw @a [{MGS_TAG},{{"text":"Red","color":"red"}},{{"text":" (Defenders) win the round!","color":"yellow"}}]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function {ns}:v{version}/multiplayer/gamemodes/snd/next_round
""")

		## S&D: Next round or game over
		self.sub("next_round", f"""
# Clean round state. #snd_round_active was already cleared by the win function that got us here, which is
# what stops the tick from judging the cleared snd_alive tags below as a wipe.
kill @e[tag={ns}.snd_bomb]
kill @e[tag={ns}.snd_bomb_vis]
kill @e[tag={ns}.snd_bomb_hud]
tag @a remove {ns}.snd_alive

# Check if either team won enough rounds (best of max_rounds) — stop here on game win
scoreboard players set #snd_win_threshold {ns}.data 4
execute if score #red {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Swap sides at halftime (after round 3)
scoreboard players add #snd_round {ns}.data 1
execute if score #snd_round {ns}.data matches 4 if score #snd_attackers {ns}.data matches 1 run scoreboard players set #snd_attackers {ns}.data 2
execute if score #snd_round {ns}.data matches 4 if score #snd_attackers {ns}.data matches 2 run scoreboard players set #snd_attackers {ns}.data 1
execute if score #snd_round {ns}.data matches 4 run tellraw @a [{MGS_TAG},"⚔ ",{{"text":"Sides swapped!","color":"gold"}}]
execute if score #snd_round {ns}.data matches 4 run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# Start next round (delay 3 seconds = 60 ticks via schedule)
schedule function {ns}:v{version}/multiplayer/gamemodes/snd/start_round 60t
""")

		## S&D Kill Hook: No team scoring from kills, only round wins
		self.sub("on_kill", f"""
scoreboard players add @s {ns}.mp.kills 1
# Remove snd_alive from dead player (dead players detected by death_count in on_respawn)
""")

		## S&D Death Hook: Mark dead (called from on_respawn override)
		self.sub("on_death", f"""
# Remove alive tag (no respawn in S&D)
tag @s remove {ns}.snd_alive
# Set to spectator mode
gamemode spectator @s
""")

		## S&D Cleanup
		## Runs BEFORE multiplayer/stop's gm_entity sweep (see game/stop.py), which is what the fill depends
		## on: it restores the world from the marker positions, so the markers have to still be alive here.
		self.sub("cleanup", f"""
schedule clear {ns}:v{version}/multiplayer/gamemodes/snd/start_round
execute at @e[tag={ns}.snd_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag={ns}.snd_obj]
kill @e[tag={ns}.snd_label]
kill @e[tag={ns}.snd_bomb]
kill @e[tag={ns}.snd_bomb_vis]
kill @e[tag={ns}.snd_bomb_hud]
tag @a remove {ns}.snd_alive
scoreboard players set #snd_round_active {ns}.data 0
""")

# Functions
def generate_search_and_destroy() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`SearchAndDestroy`. """
	SearchAndDestroy()()

