""" Per-site state for Demolition: planting, defusing and blowing up each bomb site on its own.

Two sites can be planted, contested and defused at once, so unlike Search & Destroy's fake-player scores every value lives **on the site marker**:

| Objective       | Meaning                                                              |
| --------------- | -------------------------------------------------------------------- |
| `demo_state`    | 0 = intact, 1 = planted, 2 = destroyed                               |
| `demo_prog`     | progress of whatever channel is running on this site                 |
| `demo_fuse`     | ticks left before this site's bomb goes off                          |
| `demo_owner`    | team that planted it (0 = intact or defused)                          |

The loop is inverted compared to S&D, sites outside and players inside.
That makes the channel rate one per site (a single `+=` per marker, whatever the crowd), and it walks two markers instead of every player.
"""
# Imports
from .....helpers import MGS_TAG
from .....progression import EARNER_TAG, Xp
from ...base import GameModeVariant
from ..visuals import BombVisuals

# Constants
PLANT_TICKS: int = 50
""" 2.5 s to plant, faster than Search & Destroy's 5 s: a Demolition plant is repeatable and dying costs a respawn, not the round.
Not a sourced value, tune it in game.
"""
DEFUSE_TICKS: int = 100
""" 5 s to defuse. Not a sourced value, tune it in game. """
BOMB_FUSE_TICKS: int = 200
""" 10 s from plant to detonation: the clock stops while a bomb is down and a defuse does not end the round, so a long fuse would be dead time.
Not a sourced value, tune it in game.
"""
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
		return f"""# Channels, then fuses, then the clock: a plant completing this tick must stop the clock before it can reach 0,
# or the defenders would win a round off a bomb that is already down.
execute as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=0}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_plant_tick
execute as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_defuse_tick
execute as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_fuse_tick

# One NBT write per planted site per second, on whole-second boundaries, with no extra per-entity objective.
execute store result score #demo_sec_tick {ns}.data run scoreboard players get #total_tick {ns}.data
scoreboard players operation #demo_sec_tick {ns}.data %= #20 {ns}.data
execute if score #demo_sec_tick {ns}.data matches 0 as @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=1}}] at @s run function {ns}:v{version}/multiplayer/gamemodes/demo/site_hud

# Ambient marker on the sites still standing.
execute at @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=0}}] run particle dust{{color:[1.0,0.6,0.0],scale:1.0}} ~ ~1 ~ 1.0 0.5 1.0 0 5"""

	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write every per-site function: restore, channels, fuse, HUD, defuse and destruction. """
		ns, version = variant.ns, variant.version

		## Run as a site, at it. The floating letter is never touched: it is only known at summon time,
		## so destruction is shown with added entities.
		variant.sub("restore_site", """
setblock ~ ~ ~ chest
setblock ~ ~1 ~ barrier
""")

		## Run as an intact site, at it. Exactly one side is armed each round, so #demo_ch only counts the attackers channeling here.
		variant.sub("site_plant_tick", f"""
execute store result score #demo_ch {ns}.data if entity @a[tag={ns}.demo_atk,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]

# The += is here, not per player, so a crowd plants no faster than one attacker.
execute if score #demo_ch {ns}.data matches 0 run scoreboard players set @s {ns}.demo_prog 0
execute if score #demo_ch {ns}.data matches 1.. run scoreboard players operation @s {ns}.demo_prog += #tick_delta {ns}.data

# Mirrored into a fake player: a score component naming @s would resolve for the reader, not the site.
scoreboard players operation #demo_prog_shown {ns}.data = @s {ns}.demo_prog
execute if score #demo_ch {ns}.data matches 1.. run title @a[tag={ns}.demo_atk,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#demo_prog_shown","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{PLANT_TICKS}"}}]

execute if score @s {ns}.demo_prog matches {PLANT_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/demo/site_planted
""")

		## Run as the site, at it: the planters are the players channeling in range, tagged before the announce so it pays them.
		variant.sub("site_planted", f"""
scoreboard players set @s {ns}.demo_state 1
scoreboard players set @s {ns}.demo_fuse {BOMB_FUSE_TICKS}
scoreboard players set @s {ns}.demo_prog 0
scoreboard players operation @s {ns}.demo_owner = #demo_attackers {ns}.data

tag @a remove {ns}.{EARNER_TAG}
tag @a[tag={ns}.demo_atk,predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] add {ns}.{EARNER_TAG}
{Xp.give("mp", "bomb_plant", f"@a[tag={ns}.{EARNER_TAG}]")}

{BombVisuals.planted_entities(ns, "demo_bomb", "demo_bomb_vis", "demo_bomb_hud", "PLANTED")}

{BombVisuals.announce_site_lines(variant, "BOMB PLANTED AT {letter}!", xp_key="bomb_plant")}
tag @a remove {ns}.{EARNER_TAG}
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5
""")

		## Run as a planted site, at it. Keyed on demo_owner, so each site says who may defuse it and the two stay independent.
		variant.sub("site_defuse_tick", f"""
scoreboard players set #demo_ch {ns}.data 0
execute if score @s {ns}.demo_owner matches 1 store result score #demo_ch {ns}.data if entity @a[scores={{{ns}.mp.team=2}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]
execute if score @s {ns}.demo_owner matches 2 store result score #demo_ch {ns}.data if entity @a[scores={{{ns}.mp.team=1}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}]

# #demo_ch counts defusers and is only tested against zero.
execute if score #demo_ch {ns}.data matches 0 run scoreboard players set @s {ns}.demo_prog 0
execute if score #demo_ch {ns}.data matches 1.. run scoreboard players operation @s {ns}.demo_prog += #tick_delta {ns}.data

# Only the defending side sees it, or an attacker crouched by their own bomb would read that they are defusing.
scoreboard players operation #demo_prog_shown {ns}.data = @s {ns}.demo_prog
execute if score #demo_ch {ns}.data matches 1.. if score @s {ns}.demo_owner matches 1 run title @a[scores={{{ns}.mp.team=2}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#demo_prog_shown","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]
execute if score #demo_ch {ns}.data matches 1.. if score @s {ns}.demo_owner matches 2 run title @a[scores={{{ns}.mp.team=1}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#demo_prog_shown","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]

execute if score @s {ns}.demo_prog matches {DEFUSE_TICKS}.. run function {ns}:v{version}/multiplayer/gamemodes/demo/site_defused
""")

		## Run as the site, at it. The round goes on: the attackers keep their bombs and may plant again (why Demolition rounds run longer).
		## demo_owner names the defusers, so it is read before being cleared below.
		variant.sub("site_defused", f"""
tag @a remove {ns}.{EARNER_TAG}
execute if score @s {ns}.demo_owner matches 1 run tag @a[scores={{{ns}.mp.team=2}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] add {ns}.{EARNER_TAG}
execute if score @s {ns}.demo_owner matches 2 run tag @a[scores={{{ns}.mp.team=1}},predicate={ns}:v{version}/is_sneaking,gamemode=!spectator,distance=..{SITE_RANGE}] add {ns}.{EARNER_TAG}
{Xp.give("mp", "bomb_defuse", f"@a[tag={ns}.{EARNER_TAG}]")}

scoreboard players set @s {ns}.demo_state 0
scoreboard players set @s {ns}.demo_prog 0
scoreboard players set @s {ns}.demo_fuse 0
scoreboard players set @s {ns}.demo_owner 0
kill @e[tag={ns}.demo_bomb,distance=..2]
kill @e[tag={ns}.demo_bomb_vis,distance=..2]
kill @e[tag={ns}.demo_bomb_hud,distance=..2]

{BombVisuals.announce_site_lines(variant, "BOMB DEFUSED AT {letter}!", color="aqua", xp_key="bomb_defuse")}
tag @a remove {ns}.{EARNER_TAG}
playsound minecraft:block.note_block.bit player @a ~ ~ ~ 1 1.5
""")

		## Run as a planted site, at it.
		variant.sub("site_fuse_tick", f"""
scoreboard players operation @s {ns}.demo_fuse -= #tick_delta {ns}.data
execute if score @s {ns}.demo_fuse matches ..0 run function {ns}:v{version}/multiplayer/gamemodes/demo/site_destroyed
""")

		## Run as a planted site, at it.
		variant.sub("site_hud", f"""
scoreboard players operation #demo_sec {ns}.data = @s {ns}.demo_fuse
scoreboard players operation #demo_sec {ns}.data /= #20 {ns}.data
execute store result storage {ns}:temp _demo_hud.sec int 1 run scoreboard players get #demo_sec {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/demo/set_site_hud with storage {ns}:temp _demo_hud
""")

		## Run as the planted site, at it, so the label is found by proximity.
		variant.sub("set_site_hud", f"""
$data modify entity @n[tag={ns}.demo_bomb_hud,distance=..2] text set value [{{"text":"💣 ","color":"white"}},{{"text":"$(sec)s","color":"white","bold":true}}]
""")

		## Run as the site, at it. Cosmetic only: realistic_explosion:explode would destroy real blocks,
		## and cleanup restores the map from these markers, so the hole could never be filled.
		variant.sub("site_destroyed", f"""
scoreboard players set @s {ns}.demo_state 2
scoreboard players set @s {ns}.demo_prog 0

# The attackers are paid before the blast, whose simulate_death would turn the planter into a spectator.
tag @a remove {ns}.{EARNER_TAG}
tag @a[tag={ns}.demo_atk,gamemode=!spectator] add {ns}.{EARNER_TAG}
{Xp.give("mp", "site_destroyed", f"@a[tag={ns}.{EARNER_TAG}]")}

particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8
execute as @a[distance=..{BLAST_RANGE},gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run data modify storage {ns}:input with set value {{}}
execute as @a[distance=..{BLAST_RANGE},gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run function {ns}:v{version}/multiplayer/simulate_death

# No chest to plant on: rubble and a struck-out label.
kill @e[tag={ns}.demo_bomb,distance=..2]
kill @e[tag={ns}.demo_bomb_vis,distance=..2]
kill @e[tag={ns}.demo_bomb_hud,distance=..2]
setblock ~ ~ ~ air
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.demo_rubble","{ns}.gm_entity"],block_state:"minecraft:polished_blackstone",transformation:{{translation:[-0.3f,0.0f,-0.3f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.6f,0.2f,0.6f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.demo_wreck","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💥 ","color":"white"}},{{"text":"DESTROYED","color":"dark_gray"}}],transformation:{{translation:[0.0f,1.4f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}

{BombVisuals.announce_site_lines(variant, "BOMB SITE {letter} DESTROYED!", xp_key="site_destroyed")}
tag @a remove {ns}.{EARNER_TAG}

# Time to reach the other site.
scoreboard players add #demo_timer {ns}.data {TIME_BONUS}
tellraw @a [{MGS_TAG},{{"text":"⏱ ","color":"white"}},{{"text":"+{TIME_BONUS // 20}s on the clock","color":"gold"}}]

# Attackers win once nothing is left standing, in the decider too.
execute unless entity @e[tag={ns}.demo_obj,scores={{{ns}.demo_state=..1}}] run function {ns}:v{version}/multiplayer/gamemodes/demo/attackers_win
""")

