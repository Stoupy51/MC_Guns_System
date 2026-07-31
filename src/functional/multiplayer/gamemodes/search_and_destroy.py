""" Search & Destroy: round-based bomb carry, plant and defuse, no respawns.

Modelled on Call of Duty's Search & Destroy, NOT on Counter-Strike's defusal. The difference that shapes
everything is the bomb: CoD spawns a single bomb in front of the attacking team, one attacker has to pick
it up and carry it, and it drops where they die for another attacker to retrieve. Only the carrier can
plant, and only at one of the marked sites. Counter-Strike's economy, its plant-anywhere-in-a-zone rule
and its per-player bomb spawns are all deliberately absent.
"""
# ruff: noqa: E501
# Imports
from ...helpers import MGS_TAG
from .base import GameModeVariant

# Constants
ROUND_TICKS: int = 3000
""" 2:30 to take the bomb across the map and plant it, the classic CoD round length.
Longer than a Counter-Strike round because the attackers start by walking to the bomb, not by buying. """
BOMB_FUSE_TICKS: int = 900
""" 45s from plant to detonation ([CoD Wiki](https://callofduty.fandom.com/wiki/Search_and_Destroy)),
matching Black Ops 2's competitive setting. """
PLANT_TICKS: int = 100
""" 5s to plant, the Black Ops 2 competitive value. """
DEFUSE_TICKS: int = 150
""" 7.5s to defuse, the Black Ops 2 competitive value: deliberately longer than the plant, so a defuse
has to be covered rather than stolen. """

PICKUP_RANGE: float = 2.0
""" Blocks from the loose bomb that pick it up. No channel and no key press — in CoD you collect it by
walking over it. """
SITE_RANGE: float = 3.0
""" Blocks from a site marker where the carrier can plant, and from the planted bomb where it can be defused. """

WIN_ROUNDS: int = 4
""" Round wins needed to take the match, so a match lasts between 4 and 7 rounds.
There is deliberately no cap on the round number: "first to 4" is the CoD rule, and a 3-3 match has to
play a seventh round to produce a winner. """
ROUNDS_PER_HALF: int = 3
""" Rounds a side spends attacking before the swap. """
HALFTIME_ROUND: int = ROUNDS_PER_HALF + 1
""" The round the sides swap on, i.e. the first round of the second half. """


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

# Round timer. It also drives the HUD clock: S&D owns #mp_timer outright (multiplayer/game_tick neither
# decrements it nor ends the match on it for this gamemode), because a 10-minute match limit cannot
# arbitrate a format that runs up to seven 2:30 rounds. start_round seeds the display.
scoreboard players set #snd_round_timer {ns}.data {ROUND_TICKS}

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
		## chest, so neither side can tell where the objective is without being told out of band. The letter
		## also names the site in chat when the bomb goes down there, which is how defenders rotate.
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

# Reset round timer (and the HUD clock it drives, so the 3s gap already shows the fresh 2:30)
scoreboard players set #snd_round_timer {ns}.data {ROUND_TICKS}
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}

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

# Drop a fresh bomb in front of the attacking team. There is exactly ONE bomb per round and nobody starts
# holding it, so the attackers' first job is to collect it — that walk is what gives the defenders time
# to set up, and it is the main thing that separates this from a Counter-Strike round.
tag @a remove {ns}.snd_carrier
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
execute if score #snd_attackers {ns}.data matches 1 at @e[tag={ns}.spawn_red,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
execute if score #snd_attackers {ns}.data matches 2 at @e[tag={ns}.spawn_blue,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb

# Safety net: a map defining only general spawns would otherwise open the round with no bomb anywhere,
# which the attackers could never win. Any spawn point is better than none.
execute unless entity @e[tag={ns}.snd_loose_at] at @e[tag={ns}.spawn_point,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb

# Open the round LAST, once everyone is alive-tagged and placed. Until this is 1 the tick judges nothing,
# so the gap between rounds can never be mistaken for a team wipe.
scoreboard players set #snd_round_active {ns}.data 1
""")

		## S&D: put the bomb on the ground below the current position, free for any attacker to collect.
		## Used both for the round-start bomb and for the drop when a carrier is killed, so a retrieved bomb
		## always looks and behaves exactly like the original one.
		##
		## The raycast down is not cosmetic. The carrier's label — the position a death drop is taken from —
		## rides 2.2 blocks above their feet, and PICKUP_RANGE is 2.0: a bomb summoned right there sits out
		## of reach of anyone standing under it, so losing a gunfight silently ended the attack for the round.
		## Same downward raycast as the dropped-gun code (see core/weapon_drop.py), same fallback when
		## nothing is below within range.
		self.sub("spawn_loose_bomb", f"""
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 100
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/multiplayer/gamemodes/snd/place_loose_bomb"
scoreboard players set #snd_bomb_grounded {ns}.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage {ns}:input

# Dropped over the void: leave it where it fell rather than lose it entirely
execute if score #snd_bomb_grounded {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/place_loose_bomb
""")

		## S&D: the loose bomb's three entities, at the ground point the raycast found.
		self.sub("place_loose_bomb", f"""
scoreboard players set #snd_bomb_grounded {ns}.data 1
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.snd_loose_at","{ns}.gm_entity"]}}
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.gm_entity"],block_state:{{Name:"minecraft:tnt"}},transformation:{{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 BOMB","color":"gold","bold":true}}],transformation:{{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")

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
scoreboard players set #snd_channeling {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 2 as @a[tag={ns}.snd_alive,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator] at @s if entity @e[tag={ns}.snd_bomb,distance=..{SITE_RANGE}] run function {ns}:v{version}/multiplayer/gamemodes/snd/try_defuse
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 0 run scoreboard players set #snd_defuse_progress {ns}.data 0
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_channeling {ns}.data matches 1 run scoreboard players operation #snd_defuse_progress {ns}.data += #tick_delta {ns}.data
execute if score #snd_bomb_state {ns}.data matches 2 if score #snd_defuse_progress {ns}.data matches {DEFUSE_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/snd/bomb_defused
""")

		## S&D: Pickup attempt (@s = a living player standing on the loose bomb)
		self.sub("try_pickup", f"""
# Defenders cannot touch the bomb
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 1 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 2 run return fail

tag @s add {ns}.snd_carrier
kill @e[tag={ns}.snd_loose]

# The label rides along by teleport (an entity cannot be made to ride a player), and doubles as the record
# of where the carrier is: if they die, the bomb drops at this label's position.
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_carrier_label","{ns}.gm_entity"],billboard:"vertical",teleport_duration:1,text:[{{"text":"💣","color":"gold","bold":true}}],transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:false}}

tellraw @a [{MGS_TAG},"💣 ",{{"selector":"@s"}},{{"text":" picked up the bomb!","color":"gold"}}]
playsound minecraft:item.armor.equip_chain player @a ~ ~ ~ 1 1.2
""")

		## S&D: the carrier died — put the bomb back on the ground where they fell so another attacker can
		## retrieve it. Dropping it is what keeps a lost gunfight from silently ending the attack.
		self.sub("drop_bomb", f"""
tag @s remove {ns}.snd_carrier
execute at @e[tag={ns}.snd_carrier_label,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag={ns}.snd_carrier_label]
tellraw @a [{MGS_TAG},"💣 ",{{"text":"The bomb carrier is down!","color":"yellow"}}]
""")

		## S&D: Plant attempt (@s = the carrier, sneaking at a site).
		## Raises the channel flag and shows the progress; the tick owns the increment and the completion.
		self.sub("try_plant", f"""
scoreboard players set #snd_channeling {ns}.data 1
title @s actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#snd_plant_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{PLANT_TICKS}"}}]
""")

		## S&D: Bomb planted (@s = the carrier, at them)
		self.sub("bomb_planted", f"""
scoreboard players set #snd_bomb_state {ns}.data 2
scoreboard players set #snd_bomb_timer {ns}.data {BOMB_FUSE_TICKS}
scoreboard players set #snd_plant_progress {ns}.data 0

# Force the countdown label to be written on the very next tick
scoreboard players set #snd_bomb_sec_shown {ns}.data -1

# The bomb leaves the carrier's hands
tag @s remove {ns}.snd_carrier
kill @e[tag={ns}.snd_carrier_label]

# Plant it ON the site, not wherever the player happened to be standing. A CoD bomb sits at the site, so
# both teams know exactly where the defuse happens; planting at the player's feet is the Counter-Strike
# "anywhere inside the zone" rule and made the bomb hard to find.
execute as @e[tag={ns}.snd_obj,limit=1,sort=nearest] at @s run function {ns}:v{version}/multiplayer/gamemodes/snd/place_planted_bomb

playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5
""")

		## S&D: @s = the site being planted on, at it. Spawns the planted bomb and names the site in chat.
		## The half-scale TNT is raised to 0.625 so it pokes out of the chest lid (a chest is 0.875 tall)
		## instead of being summoned inside the block and invisible. The countdown label clears its top.
		self.sub("place_planted_bomb", f"""
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.snd_bomb","{ns}.gm_entity"]}}
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.snd_bomb_vis","{ns}.gm_entity"],block_state:{{Name:"minecraft:tnt"}},transformation:{{translation:[-0.25f,0.625f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_bomb_hud","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 PLANTED","color":"red","bold":true}}],transformation:{{translation:[0.0f,1.4f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}

# Name the site so the defenders know which one to rotate to
execute if entity @s[tag={ns}.snd_site_A] run tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB PLANTED AT A!","color":"red","bold":true}}]
execute if entity @s[tag={ns}.snd_site_B] run tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB PLANTED AT B!","color":"red","bold":true}}]
execute if entity @s[tag={ns}.snd_site_C] run tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB PLANTED AT C!","color":"red","bold":true}}]
execute if entity @s[tag={ns}.snd_site_D] run tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB PLANTED AT D!","color":"red","bold":true}}]
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

# Raise the channel flag and show the progress; the tick owns the increment, so extra defenders on the
# same bomb give cover rather than a faster defuse. The bomb countdown keeps running in parallel.
scoreboard players set #snd_channeling {ns}.data 1
title @s actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#snd_defuse_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]
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
# The HUD clock is reset here and not only in start_round: the tick stops driving it while no round is
# running, so the 3s gap would otherwise sit on the expired timer or the leftover fuse.
scoreboard players set #mp_timer {ns}.data {ROUND_TICKS}
kill @e[tag={ns}.snd_bomb]
kill @e[tag={ns}.snd_bomb_vis]
kill @e[tag={ns}.snd_bomb_hud]
kill @e[tag={ns}.snd_loose]
kill @e[tag={ns}.snd_carrier_label]
tag @a remove {ns}.snd_carrier
tag @a remove {ns}.snd_alive

# Check if either team reached the round-win threshold (set in setup, also read by the sidebar)
execute if score #red {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Red"}}
execute if score #blue {ns}.mp.team >= #snd_win_threshold {ns}.data run return run function {ns}:v{version}/multiplayer/team_wins {{team:"Blue"}}

# Swap sides at halftime
scoreboard players add #snd_round {ns}.data 1
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} if score #snd_attackers {ns}.data matches 1 run scoreboard players set #snd_attackers {ns}.data 2
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} if score #snd_attackers {ns}.data matches 2 run scoreboard players set #snd_attackers {ns}.data 1
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} run tellraw @a [{MGS_TAG},"⚔ ",{{"text":"Sides swapped!","color":"gold"}}]
execute if score #snd_round {ns}.data matches {HALFTIME_ROUND} run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
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
execute at @e[tag={ns}.snd_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag={ns}.snd_obj]
kill @e[tag={ns}.snd_label]
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
