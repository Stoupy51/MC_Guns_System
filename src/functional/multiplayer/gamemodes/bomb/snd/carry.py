""" The carried bomb: one per round, collected off the ground, dropped where its carrier falls.

This is the whole difference between Search & Destroy and Demolition. Demolition arms every attacker on
every respawn and needs none of it.
"""
# ruff: noqa: E501
# Imports
from .....helpers import MGS_TAG
from .....helpers.text import Text
from .....progression import Xp
from ...base import GameModeVariant

# Constants
PICKUP_RANGE: float = 2.0
""" Blocks from the loose bomb that pick it up. No channel and no key press — in CoD you collect it by
walking over it. """


# Classes
class SndCarry:
	""" Spawning, collecting, dropping and recovering the single round bomb. """

	# Functions
	@staticmethod
	def write(variant: GameModeVariant) -> None:
		""" Write `spawn_loose_bomb`, `place_loose_bomb`, `recover_bomb`, `try_pickup` and `drop_bomb`. """
		ns, version = variant.ns, variant.version

		## S&D: put the bomb on the ground below the current position, free for any attacker to collect.
		## Used both for the round-start bomb and for the drop when a carrier is killed, so a retrieved bomb
		## always looks and behaves exactly like the original one.
		##
		## The raycast down is not cosmetic. The carrier's label — the position a death drop is taken from —
		## rides 2.2 blocks above their feet, and PICKUP_RANGE is 2.0: a bomb summoned right there sits out
		## of reach of anyone standing under it, so losing a gunfight silently ended the attack for the round.
		## Same downward raycast as the dropped-gun code (see core/weapon_drop.py), same fallback when
		## nothing is below within range.
		variant.sub("spawn_loose_bomb", f"""
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
		variant.sub("place_loose_bomb", f"""
scoreboard players set #snd_bomb_grounded {ns}.data 1
summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.snd_loose_at","{ns}.gm_entity"]}}
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.gm_entity"],block_state:{{Name:"minecraft:tnt"}},transformation:{{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_loose","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 BOMB","color":"gold","bold":true}}],transformation:{{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}
""")

		## S&D: the carrier is gone from @a (disconnect) but their label survives — put the bomb back.
		variant.sub("recover_bomb", f"""
execute at @e[tag={ns}.snd_carrier_label,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag={ns}.snd_carrier_label]
tellraw @a [{MGS_TAG},"💣 ",{{"text":"The bomb carrier left the game — bomb dropped!","color":"yellow"}}]
""")

		## S&D: Pickup attempt (@s = a living player standing on the loose bomb)
		variant.sub("try_pickup", f"""
# Defenders cannot touch the bomb
execute if score #snd_attackers {ns}.data matches 1 unless score @s {ns}.mp.team matches 1 run return fail
execute if score #snd_attackers {ns}.data matches 2 unless score @s {ns}.mp.team matches 2 run return fail

tag @s add {ns}.snd_carrier
kill @e[tag={ns}.snd_loose]

# The label rides along by teleport (an entity cannot be made to ride a player), and doubles as the record
# of where the carrier is: if they die, the bomb drops at this label's position.
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.snd_carrier_label","{ns}.gm_entity"],billboard:"vertical",teleport_duration:1,text:[{{"text":"💣","color":"gold","bold":true}}],transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:false}}

{Xp.announce("mp", "bomb_pickup", f'{MGS_TAG},"💣 ",{Text.player(ns, "@s")},{{"text":" picked up the bomb!","color":"gold"}}')}
playsound minecraft:item.armor.equip_chain player @a ~ ~ ~ 1 1.2
""")

		## S&D: the carrier died — put the bomb back on the ground where they fell so another attacker can
		## retrieve it. Dropping it is what keeps a lost gunfight from silently ending the attack.
		variant.sub("drop_bomb", f"""
tag @s remove {ns}.snd_carrier
execute at @e[tag={ns}.snd_carrier_label,limit=1] run function {ns}:v{version}/multiplayer/gamemodes/snd/spawn_loose_bomb
kill @e[tag={ns}.snd_carrier_label]
tellraw @a [{MGS_TAG},"💣 ",{{"text":"The bomb carrier is down!","color":"yellow"}}]
""")
