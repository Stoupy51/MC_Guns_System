""" The carried bomb: one per round, collected off the ground, dropped where its carrier falls.

This is the whole difference between Search & Destroy and Demolition. Demolition arms every attacker on
every respawn and needs none of it.
"""
# Imports
from .....helpers import MGS_TAG
from .....helpers.text import Text
from .....progression import Xp
from ...base import GameModeVariant

# Constants
PICKUP_RANGE: float = 2.0
""" Blocks from the loose bomb that pick it up: no channel and no key press, as in CoD you collect it by walking over it. """


# Classes
class SndCarry:
	""" Spawning, collecting, dropping and recovering the single round bomb. """

	# Functions
	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write `spawn_loose_bomb`, `place_loose_bomb`, `recover_bomb`, `try_pickup` and `drop_bomb`. """
		ns, version = variant.ns, variant.version

		## Put the bomb on the ground below, free for any attacker; used for the round-start bomb and a carrier's death drop.
		## The raycast down matters: a death drop starts at the carrier's label, 2.2 above their feet, out of PICKUP_RANGE (2.0); same raycast and fallback as core/weapon_drop.
		variant.sub("spawn_loose_bomb", f"""
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 100
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/multiplayer/gamemodes/snd/place_loose_bomb"
scoreboard players set #snd_bomb_grounded {ns}.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage {ns}:input

# Over the void it stays where it fell.
execute if score #snd_bomb_grounded {ns}.data matches 0 run function {ns}:v{version}/multiplayer/gamemodes/snd/place_loose_bomb
""")

		## The loose bomb's three entities, at the ground point.
		variant.sub("place_loose_bomb", f"""
scoreboard players set #snd_bomb_grounded {ns}.data 1
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.snd_loose_at","{ns}.gm_entity"]}}
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.gm_entity"],block_state:"minecraft:tnt",transformation:{{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 ","color":"white"}},{{"text":"BOMB","color":"gold","bold":true}}],transformation:{{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")

		## The carrier left the server but their label remains: put the bomb back there.
		variant.sub("recover_bomb", f"""
execute at @e[tag={ns}.snd_carrier_label,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag={ns}.snd_carrier_label]
tellraw @a [{MGS_TAG},{{"text":"💣 ","color":"white"}},{{"text":"The bomb carrier left the game: bomb dropped!","color":"yellow"}}]
""")

		## Run as a living player standing on the loose bomb.
		variant.sub("try_pickup", f"""
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 1 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 2 run return fail

tag @s add {ns}.snd_carrier
kill @e[tag={ns}.snd_loose]

# The label follows by teleport (an entity cannot ride a player) and marks where the bomb drops if the carrier dies.
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_carrier_label","{ns}.gm_entity"],billboard:"vertical",teleport_duration:1,text:[{{"text":"💣","color":"white"}}],transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:false}}

{Xp.announce("mp", "bomb_pickup", f'{MGS_TAG},{{"text":"💣 ","color":"white"}},{Text.player(ns, "@s")},{{"text":" picked up the bomb!","color":"gold"}}')}
playsound minecraft:item.armor.equip_chain player @a ~ ~ ~ 1 1.2
""")

		## The carrier died: the bomb drops where they fell, so the attack can go on.
		variant.sub("drop_bomb", f"""
tag @s remove {ns}.snd_carrier
execute at @e[tag={ns}.snd_carrier_label,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag={ns}.snd_carrier_label]
tellraw @a [{MGS_TAG},{{"text":"💣 ","color":"white"}},{{"text":"The bomb carrier is down!","color":"yellow"}}]
""")

