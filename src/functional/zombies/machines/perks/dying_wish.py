""" Dying Wish: the owner is restored at their death spot and goes berserk instead of going down. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from ....helpers.titles import TitleTimes


# Functions
def write_dying_wish() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Dying Wish: instead of going down, the owner is restored where they died and goes berserk for 9 s (invulnerable,
	# heavy melee), then is left at 1 HP, with a cooldown of 60 s per use. Triggered from revive/on_down.

	## Run as the player who would have gone down (already respawned, LastDeathLocation set).
	write_versioned_function("zombies/perks/dying_wish_trigger", f"""
# Not a real down: undo the downs++ that on_respawn added.
scoreboard players remove @s {ns}.zb.downs 1

# 60 s x uses.
scoreboard players add @s {ns}.zb.dw_uses 1
scoreboard players operation @s {ns}.zb.dw_cd = @s {ns}.zb.dw_uses
scoreboard players operation @s {ns}.zb.dw_cd *= #1200 {ns}.data

# Reuses the revive teleport macro.
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000
function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp

# Juggernog's health is respected.
gamemode adventure @s
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# 9 s: resistance V, one-shot melee, mobility.
scoreboard players set @s {ns}.zb.dw_timer 180
tag @s add {ns}.dying_wish_active
effect give @s minecraft:resistance 180 4 true
effect give @s minecraft:fire_resistance 180 0 true
effect give @s minecraft:strength 180 4 true
effect give @s minecraft:speed 180 1 true
attribute @s minecraft:attack_damage modifier add {ns}:dying_wish 200 add_value

{TitleTimes.EVENT.cmd()}
title @s title ["⚔"]
title @s subtitle [{{"text":"DYING WISH: Berserk!","color":"dark_red"}}]
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.3 80 force @a[distance=..32]
playsound minecraft:item.totem.use player @a[distance=..32] ~ ~ ~ 1 0.8
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="blue")},{{"text":" refuses to die!","color":"gray"}}]
""")

	## Run as the player from player/tick while dw_timer >= 1.
	write_versioned_function("zombies/perks/dying_wish_tick", f"""
particle minecraft:crit ~ ~1 ~ 0.4 0.6 0.4 0.05 4 force @a[distance=..24]
scoreboard players remove @s {ns}.zb.dw_timer 1
execute if score @s {ns}.zb.dw_timer matches ..0 run function {ns}:v{version}/zombies/perks/dying_wish_end
""")

	## Run as the player: strip the buffs and leave 1 HP.
	write_versioned_function("zombies/perks/dying_wish_end", f"""
attribute @s minecraft:attack_damage modifier remove {ns}:dying_wish
effect clear @s minecraft:resistance
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:strength
effect clear @s minecraft:speed
tag @s remove {ns}.dying_wish_active
scoreboard players set @s {ns}.zb.dw_timer 0

# Left at 1 HP (BO). /data cannot write a player's Health, so an exact (Health - 1) generic_kill hit lands on 1 HP
# through armor, resistance and effects. Health x 1000 for precision; skipped at 1 HP or below.
execute store result score #dw_hp {ns}.data run data get entity @s Health 1000
scoreboard players remove #dw_hp {ns}.data 1000
execute if score #dw_hp {ns}.data matches 1.. run function {ns}:v{version}/zombies/perks/dying_wish_to_1
{TitleTimes.AFTERMATH.cmd()}
title @s title ["⚔"]
title @s subtitle [{{"text":"...barely alive.","color":"gray"}}]
""")

	# #dw_hp = (Health - 1) x 1000. generic_kill has no source entity, so entity_hurt_player never fires.
	write_versioned_function("zombies/perks/dying_wish_to_1", f"""
execute store result storage {ns}:temp _dw_dmg.amount double 0.001 run scoreboard players get #dw_hp {ns}.data
data modify storage {ns}:temp _dw_dmg.type set value "minecraft:generic_kill"
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _dw_dmg
""")

