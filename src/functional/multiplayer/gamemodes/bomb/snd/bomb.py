""" Planting, defusing and detonating the Search & Destroy bomb.

There is exactly one bomb in play, so the channel progress lives on plain fake-player scores.
Demolition has one bomb per site and keeps that state on each site marker instead.
"""
# Imports
from .....helpers import MGS_TAG
from .....progression import EARNER_TAG, Xp
from ...base import GameModeVariant
from ..visuals import BombVisuals

# Constants
BOMB_FUSE_TICKS: int = 900
""" 45s from plant to detonation ([CoD Wiki](https://callofduty.fandom.com/wiki/Search_and_Destroy)),
matching Black Ops 2's competitive setting. """
PLANT_TICKS: int = 100
""" 5s to plant, the Black Ops 2 competitive value. """
DEFUSE_TICKS: int = 150
""" 7.5s to defuse, the Black Ops 2 competitive value: deliberately longer than the plant, so a defuse
has to be covered rather than stolen. """
SITE_RANGE: float = 3.0
""" Blocks from a site marker where the carrier can plant, and from the planted bomb where it can be defused. """


# Classes
class SndBomb:
	""" The plant/defuse channels, the planted bomb and its countdown. """

	# Functions
	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write every function between "the carrier is sneaking at a site" and "the round is over". """
		ns, version = variant.ns, variant.version

		## Run as the carrier, sneaking at a site: raises the channel flag; the tick advances and completes it.
		variant.sub("try_plant", f"""
scoreboard players set #snd_channeling {ns}.data 1
title @s actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#snd_plant_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{PLANT_TICKS}"}}]
""")

		## Run as the carrier, at them.
		variant.sub("bomb_planted", f"""
scoreboard players set #snd_bomb_state {ns}.data 2
scoreboard players set #snd_bomb_timer {ns}.data {BOMB_FUSE_TICKS}
scoreboard players set #snd_plant_progress {ns}.data 0

# The countdown label is written on the next tick.
scoreboard players set #snd_bomb_sec_shown {ns}.data -1

tag @s remove {ns}.snd_carrier
kill @e[tag={ns}.snd_carrier_label]

# Marked so the site announce in place_planted_bomb carries their XP.
{Xp.give("mp", "bomb_plant")}
tag @a remove {ns}.{EARNER_TAG}
tag @s add {ns}.{EARNER_TAG}

# On the site, not at the player's feet: a CoD bomb sits at the site, so both teams know where the defuse happens.
execute as @e[tag={ns}.snd_obj,limit=1,sort=nearest] at @s run function {ns}:v{version}/multiplayer/gamemodes/snd/place_planted_bomb
tag @a remove {ns}.{EARNER_TAG}

playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5
""")

		## Run as the site, at it: spawns the planted bomb and names the site.
		variant.sub("place_planted_bomb", f"""
{BombVisuals.planted_entities(ns, "snd_bomb", "snd_bomb_vis", "snd_bomb_hud", "PLANTED")}

# The site name tells defenders where to rotate; the same line pays the planter.
{BombVisuals.announce_site_lines(variant, "BOMB PLANTED AT {letter}!", xp_key="bomb_plant")}
""")

		## Only when the displayed second changes.
		variant.sub("update_bomb_hud", f"""
scoreboard players operation #snd_bomb_sec_shown {ns}.data = #snd_bomb_sec {ns}.data
execute store result storage {ns}:temp _snd_hud.sec int 1 run scoreboard players get #snd_bomb_sec {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/snd/set_bomb_hud with storage {ns}:temp _snd_hud
""")

		## By tag rather than @n: the mode tick has no meaningful position.
		variant.sub("set_bomb_hud", f"""
$data modify entity @e[tag={ns}.snd_bomb_hud,limit=1] text set value [{{"text":"💣 ","color":"white"}},{{"text":"$(sec)s","color":"white","bold":true}}]
""")

		variant.sub("try_defuse", f"""
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 2 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 1 run return fail

# The tick owns the increment, so extra defenders give cover, not a faster defuse; the fuse keeps running.
scoreboard players set #snd_channeling {ns}.data 1
tag @s add {ns}.{EARNER_TAG}
title @s actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#snd_defuse_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]
""")

		## Defenders win. try_defuse tagged the channelers this tick, so the existing announce line pays them.
		variant.sub("bomb_defused", f"""
tellraw @a[tag=!{ns}.{EARNER_TAG}] [{MGS_TAG},{{"text":"💣 ","color":"white"}},{{"text":"BOMB DEFUSED!","color":"aqua","bold":true}}]
tellraw @a[tag={ns}.{EARNER_TAG}] [{MGS_TAG},{{"text":"💣 ","color":"white"}},{{"text":"BOMB DEFUSED!","color":"aqua","bold":true}},{Xp.suffix("mp", "bomb_defuse")}]
{Xp.give("mp", "bomb_defuse", f"@a[tag={ns}.{EARNER_TAG}]")}
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win
""")

		variant.sub("bomb_explodes", f"""
execute at @e[tag={ns}.snd_bomb] run particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
execute at @e[tag={ns}.snd_bomb] run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8

# Players within 10 blocks die.
execute at @e[tag={ns}.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run data modify storage {ns}:input with set value {{}}
execute at @e[tag={ns}.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={{{ns}.mp.in_game=1..}}] run function {ns}:v{version}/multiplayer/simulate_death

tellraw @a [{MGS_TAG},{{"text":"💥 ","color":"white"}},{{"text":"BOMB EXPLODED!","color":"red","bold":true}}]
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/attackers_win
""")

