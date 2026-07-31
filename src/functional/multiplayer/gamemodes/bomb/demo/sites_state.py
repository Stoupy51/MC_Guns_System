""" Per-site state for Demolition: planting, defusing and blowing up each bomb site independently.

Two sites can be planted, contested and defused at the same time, so none of this can live on the shared
fake-player scores Search & Destroy uses — every value below is stored **on the site marker**:

| Objective       | Meaning                                                              |
| --------------- | -------------------------------------------------------------------- |
| `demo_state`    | 0 = intact, 1 = planted, 2 = destroyed                               |
| `demo_prog`     | progress of whatever channel is running on this site                 |
| `demo_fuse`     | ticks left before this site's bomb goes off                          |
| `demo_owner`    | team channeling it, then the team that planted it (0 = nobody)       |

The loop is also inverted compared to S&D: sites on the outside, players on the inside. That makes the
channel rate structurally one-per-site (a single `+=` per marker, whatever the crowd standing on it) and
it is cheaper — two markers to walk instead of every player.
"""
# ruff: noqa: E501
# Imports
from .....helpers import MGS_TAG
from ...base import GameModeVariant
from ..visuals import BombVisuals

# Constants
PLANT_TICKS: int = 50
""" 2.5s to plant. Faster than Search & Destroy's 5s because a Demolition plant is repeatable and dying
costs a respawn rather than the round. NOT a sourced value — tune in game. """
DEFUSE_TICKS: int = 100
""" 5s to defuse. NOT a sourced value — tune in game. """
BOMB_FUSE_TICKS: int = 200
""" 10s from plant to detonation. Short on purpose: the clock stops while a bomb is down and a defuse does
not end the round, so a long fuse would just be dead time. NOT a sourced value — tune in game. """
SITE_RANGE: float = 3.0
""" Blocks from a site marker where it can be planted or defused. """
BLAST_RANGE: float = 8.0
""" Blocks from a detonating site that get killed by it. """
TIME_BONUS: int = 1200
""" 60s added to the round clock for each site destroyed, so the attackers can reach the other one.
The rule is from CoD; the amount is mine. """


# Classes
class DemoSites:
	""" The channels, the fuse and the destruction of a single Demolition site. """

	# Functions
	@staticmethod
	def reset_lines(variant: GameModeVariant) -> str:
		""" Return the lines putting every site back to intact, used at each round start. """
		ns, version = variant.ns, variant.version
		return f"""kill @e[tag={ns}.demo_bomb]
kill @e[tag={ns}.demo_bomb_vis]
kill @e[tag={ns}.demo_bomb_hud]
kill @e[tag={ns}.demo_wreck]
kill @e[tag={ns}.demo_rubble]
scoreboard players set @e[tag={ns}.demo_obj] {ns}.demo_state 0
scoreboard players set @e[tag={ns}.demo_obj] {ns}.demo_prog 0
scoreboard players set @e[tag={ns}.demo_obj] {ns}.demo_fuse 0
scoreboard players set @e[tag={ns}.demo_obj] {ns}.demo_owner 0
execute as @e[tag={ns}.demo_obj] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/restore_site"""

	@staticmethod
	def tick_lines(variant: GameModeVariant) -> str:
		""" Return the per-site dispatch: channels, then fuses, then the once-a-second label rewrite. """
		ns, version = variant.ns, variant.version
		return f"""# Channels first, fuses second, and the clock LAST (see the clock block below): a plant that completes on
# this tick has to have stopped the clock before the clock is allowed to reach 0, otherwise the defenders
# steal a round off a bomb that is already down.
execute as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=0}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_plant_tick
execute as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_defuse_tick
execute as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_fuse_tick

# One NBT write per planted site per second. Rewriting on a whole-second boundary rather than tracking a
# "last shown" value per site keeps the same cost without a fifth per-entity objective.
execute store result score #demo_sec_tick {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #demo_sec_tick {ns}.data %= #20 {ns}.data
execute if score #demo_sec_tick {ns}.data matches 0 as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_hud

# Ambient marker on whatever is still standing
execute at @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=0}}] run particle dust{{color:[1.0,0.6,0.0],scale:1.0}} ~ ~1 ~ 1.0 0.5 1.0 0 5"""

	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write every per-site function: restore, channels, fuse, HUD, defuse and destruction. """
		ns, version = variant.ns, variant.version

		## Put the chest and its barrier back (@s = a site, at it). The floating letter is never touched,
		## which is why destruction is shown with added entities rather than by rewriting that label: the
		## letter is only known at summon time and nothing stores it afterwards.
		variant.sub("restore_site", """
setblock ~ ~ ~ chest
setblock ~ ~1 ~ barrier
""")

		## Plant channel (@s = an intact site, at it).
		## #demo_ch is which team is planting: 0 = nobody, or contested. In a normal round only one side is
		## armed so a contest is impossible; in overtime BOTH are, and "clear the site before you plant" is
		## exactly the rule that makes the resulting owner unambiguous.
		variant.sub("site_plant_tick", f"""
execute store result score #demo_ch_red {ns}.data if entity @a[tag={ns}.demo_atk,scores={{{ns}.mp.team=1}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]
execute store result score #demo_ch_blue {ns}.data if entity @a[tag={ns}.demo_atk,scores={{{ns}.mp.team=2}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]
scoreboard players set #demo_ch {ns}.data 0
execute if score #demo_ch_red {ns}.data matches 1.. if score #demo_ch_blue {ns}.data matches 0 run scoreboard players set #demo_ch {ns}.data 1
execute if score #demo_ch_blue {ns}.data matches 1.. if score #demo_ch_red {ns}.data matches 0 run scoreboard players set #demo_ch {ns}.data 2

# A different team taking over restarts the plant from zero
execute unless score #demo_ch {ns}.data = @s {ns}.demo_owner run scoreboard players set @s {ns}.demo_prog 0
scoreboard players operation @s {ns}.demo_owner = #demo_ch {ns}.data

# The += is here and NOT inside a per-player function, so a crowd plants no faster than one attacker
execute if score #demo_ch {ns}.data matches 0 run scoreboard players set @s {ns}.demo_prog 0
execute if score #demo_ch {ns}.data matches 1.. run scoreboard players operation @s {ns}.demo_prog += #tick_delta {ns}.data

# Progress readout. Mirrored into a fake player first: a score component naming @s would be resolved in
# the recipient's context, not the site's.
scoreboard players operation #demo_prog_shown {ns}.data = @s {ns}.demo_prog
execute if score #demo_ch {ns}.data matches 1.. run title @a[tag={ns}.demo_atk,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#demo_prog_shown","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{PLANT_TICKS}"}}]

execute if score @s {ns}.demo_prog matches {PLANT_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/demo/site_planted
""")

		## The bomb goes down on this site (@s = the site, at it). demo_owner already holds the planting team.
		variant.sub("site_planted", f"""
scoreboard players set @s {ns}.demo_state 1
scoreboard players set @s {ns}.demo_fuse {BOMB_FUSE_TICKS}
scoreboard players set @s {ns}.demo_prog 0

{BombVisuals.planted_entities(ns, "demo_bomb", "demo_bomb_vis", "demo_bomb_hud", "PLANTED")}

{BombVisuals.announce_site_lines(variant, "BOMB PLANTED AT {letter}!")}
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5
""")

		## Defuse channel (@s = a planted site, at it). "Anyone whose team is not the owner" covers both
		## phases at once: in a normal round that is the defenders, in overtime it is whoever did not plant.
		variant.sub("site_defuse_tick", f"""
scoreboard players set #demo_ch {ns}.data 0
execute if score @s {ns}.demo_owner matches 1 store result score #demo_ch {ns}.data if entity @a[scores={{{ns}.mp.team=2}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]
execute if score @s {ns}.demo_owner matches 2 store result score #demo_ch {ns}.data if entity @a[scores={{{ns}.mp.team=1}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]

# Single-rate again: #demo_ch is a COUNT of defusers, and it is only ever tested against zero
execute if score #demo_ch {ns}.data matches 0 run scoreboard players set @s {ns}.demo_prog 0
execute if score #demo_ch {ns}.data matches 1.. run scoreboard players operation @s {ns}.demo_prog += #tick_delta {ns}.data

# Readout to the defusing side only. Without the team filter the attacker crouched next to their own bomb
# was told they were defusing it.
scoreboard players operation #demo_prog_shown {ns}.data = @s {ns}.demo_prog
execute if score #demo_ch {ns}.data matches 1.. if score @s {ns}.demo_owner matches 1 run title @a[scores={{{ns}.mp.team=2}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#demo_prog_shown","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]
execute if score #demo_ch {ns}.data matches 1.. if score @s {ns}.demo_owner matches 2 run title @a[scores={{{ns}.mp.team=1}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#demo_prog_shown","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]

execute if score @s {ns}.demo_prog matches {DEFUSE_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/demo/site_defused
""")

		## Defused (@s = the site, at it). This does NOT end the round: the attackers keep their bombs and
		## may plant this site again, which is the whole reason Demolition rounds are longer than S&D ones.
		variant.sub("site_defused", f"""
scoreboard players set @s {ns}.demo_state 0
scoreboard players set @s {ns}.demo_prog 0
scoreboard players set @s {ns}.demo_fuse 0
scoreboard players set @s {ns}.demo_owner 0
kill @e[tag={ns}.demo_bomb,distance=..2]
kill @e[tag={ns}.demo_bomb_vis,distance=..2]
kill @e[tag={ns}.demo_bomb_hud,distance=..2]

{BombVisuals.announce_site_lines(variant, "BOMB DEFUSED AT {letter}!", color="aqua")}
playsound minecraft:block.note_block.bit player @a ~ ~ ~ 1 1.5
""")

		## Fuse (@s = a planted site, at it)
		variant.sub("site_fuse_tick", f"""
scoreboard players operation @s {ns}.demo_fuse -= #tick_delta {ns}.data
execute if score @s {ns}.demo_fuse matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/demo/site_destroyed
""")

		## Rewrite this site's countdown (@s = a planted site, at it)
		variant.sub("site_hud", f"""
scoreboard players operation #demo_sec {ns}.data = @s {ns}.demo_fuse
scoreboard players operation #demo_sec {ns}.data /= #20 {ns}.data
execute store result storage {ns}:temp _demo_hud.sec int 1 run scoreboard players get #demo_sec {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/demo/set_site_hud with storage {ns}:temp _demo_hud
""")

		## @s = the planted site, at it — so the label is found by proximity rather than by a global tag
		variant.sub("set_site_hud", f"""
$data modify entity @n[tag={ns}.demo_bomb_hud,distance=..2] text set value [{{"text":"💣 ","color":"red","bold":true}},{{"text":"$(sec)s","color":"white"}}]
""")

		## The site blows up (@s = the site, at it).
		## Cosmetic only. realistic_explosion:explode is deliberately NOT used: it destroys real blocks, and
		## cleanup restores the map from these very markers, so a genuine explosion would leave a hole nobody
		## could put back.
		variant.sub("site_destroyed", f"""
scoreboard players set @s {ns}.demo_state 2
scoreboard players set @s {ns}.demo_prog 0
scoreboard players operation #demo_last_owner {ns}.data = @s {ns}.demo_owner

particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8
execute as @a[distance=..{BLAST_RANGE},gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run data modify storage {ns}:input with set value {{}}
execute as @a[distance=..{BLAST_RANGE},gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run function {ns}:v{version}/multiplayer/simulate_death

# The site is wrecked: no chest to plant on, rubble and a struck-out label in its place
kill @e[tag={ns}.demo_bomb,distance=..2]
kill @e[tag={ns}.demo_bomb_vis,distance=..2]
kill @e[tag={ns}.demo_bomb_hud,distance=..2]
setblock ~ ~ ~ air
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.demo_rubble","{ns}.gm_entity"],block_state:{{Name:"minecraft:polished_blackstone"}},transformation:{{translation:[-0.3f,0.0f,-0.3f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.6f,0.2f,0.6f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.demo_wreck","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💥 DESTROYED","color":"dark_gray"}}],transformation:{{translation:[0.0f,1.4f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}

{BombVisuals.announce_site_lines(variant, "BOMB SITE {letter} DESTROYED!")}

# Destroying a site buys time to reach the other one
scoreboard players add #demo_timer {ns}.data {TIME_BONUS}
tellraw @a [{MGS_TAG},"⏱ ",{{"text":"+{TIME_BONUS // 20}s on the clock","color":"gold"}}]

# Overtime is a single neutral site, so blowing it up takes the MATCH for whoever planted it
execute if score #demo_round {ns}.data matches 3.. run return run function {ns}:v{version}/multiplayer/gamemodes/demo/overtime_won

# Otherwise the attackers only win once nothing is left standing
execute unless entity @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=..1}}] run function {ns}:v{version}/multiplayer/gamemodes/demo/attackers_win
""")
