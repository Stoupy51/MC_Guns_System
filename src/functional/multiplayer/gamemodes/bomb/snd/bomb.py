""" Planting, defusing and detonating the Search & Destroy bomb.

There is exactly one bomb in play, so the channel progress can live on plain fake-player scores. Demolition
cannot do that — it has a site-per-bomb and keeps the same state on each site marker instead.
"""
# Imports
from .....helpers import MGS_TAG
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

		## S&D: Plant attempt (@s = the carrier, sneaking at a site).
		## Raises the channel flag and shows the progress; the tick owns the increment and the completion.
		variant.sub("try_plant", f"""
scoreboard players set #snd_channeling {ns}.data 1
title @s actionbar [{{"text":"Planting... ","color":"gold"}},{{"score":{{"name":"#snd_plant_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{PLANT_TICKS}"}}]
""")

		## S&D: Bomb planted (@s = the carrier, at them)
		variant.sub("bomb_planted", f"""
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
		variant.sub("place_planted_bomb", f"""
{BombVisuals.planted_entities(ns, "snd_bomb", "snd_bomb_vis", "snd_bomb_hud", "PLANTED")}

# Name the site so the defenders know which one to rotate to
{BombVisuals.announce_site_lines(variant, "BOMB PLANTED AT {letter}!")}
""")

		## S&D: rewrite the bomb countdown label (only called when the displayed second changes)
		variant.sub("update_bomb_hud", f"""
scoreboard players operation #snd_bomb_sec_shown {ns}.data = #snd_bomb_sec {ns}.data
execute store result storage {ns}:temp _snd_hud.sec int 1 run scoreboard players get #snd_bomb_sec {ns}.data
function {ns}:v{version}/multiplayer/gamemodes/snd/set_bomb_hud with storage {ns}:temp _snd_hud
""")

		## Selected by tag rather than @n: this runs from the mode tick, which has no meaningful position.
		variant.sub("set_bomb_hud", f"""
$data modify entity @e[tag={ns}.snd_bomb_hud,limit=1] text set value [{{"text":"💣 ","color":"red","bold":true}},{{"text":"$(sec)s","color":"white"}}]
""")

		## S&D: Defuse attempt
		variant.sub("try_defuse", f"""
# Only defenders can defuse
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 2 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 1 run return fail

# Raise the channel flag and show the progress; the tick owns the increment, so extra defenders on the
# same bomb give cover rather than a faster defuse. The bomb countdown keeps running in parallel.
scoreboard players set #snd_channeling {ns}.data 1
title @s actionbar [{{"text":"Defusing... ","color":"aqua"}},{{"score":{{"name":"#snd_defuse_progress","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/{DEFUSE_TICKS}"}}]
""")

		## S&D: Bomb defused → defenders win
		variant.sub("bomb_defused", f"""
tellraw @a [{MGS_TAG},"💣 ",{{"text":"BOMB DEFUSED!","color":"aqua","bold":true}}]
kill @e[tag={ns}.snd_bomb]
function {ns}:v{version}/multiplayer/gamemodes/snd/defenders_win
""")

		## S&D: Bomb explodes → attackers win
		variant.sub("bomb_explodes", f"""
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
