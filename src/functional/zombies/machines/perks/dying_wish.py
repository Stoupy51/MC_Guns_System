""" Dying Wish: the owner is restored at their death spot and goes berserk instead of going down. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG


# Functions
def write_dying_wish() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Dying Wish: instead of going down, the owner is restored at the death spot and goes berserk.
	# Invulnerable with heavy melee for 9s, then left at 1 HP, on an escalating 60s-per-use cooldown.
	# Triggered from the top of revive/on_down, which is why there is no purchase-time effect.

	## Trigger: @s = the player who would have gone down (already vanilla-respawned; LastDeathLocation set).
	write_versioned_function("zombies/perks/dying_wish_trigger", f"""
# Not a real down — undo the downs++ that on_respawn added before calling on_down
scoreboard players remove @s {ns}.zb.downs 1

# Count the use and set the escalating cooldown (60s * uses = 1200t * uses)
scoreboard players add @s {ns}.zb.dw_uses 1
scoreboard players operation @s {ns}.zb.dw_cd = @s {ns}.zb.dw_uses
scoreboard players operation @s {ns}.zb.dw_cd *= #1200 {ns}.data

# Teleport back to the death location (reuse the revive tp macro)
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000
function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp

# Restore: adventure mode, full health (respect Juggernog), stamina
gamemode adventure @s
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Berserk for 9s (180t): invulnerable (resistance V) + one-shot melee + mobility, and a big melee attribute
scoreboard players set @s {ns}.zb.dw_timer 180
tag @s add {ns}.dying_wish_active
effect give @s minecraft:resistance 180 4 true
effect give @s minecraft:fire_resistance 180 0 true
effect give @s minecraft:strength 180 4 true
effect give @s minecraft:speed 180 1 true
attribute @s minecraft:attack_damage modifier add {ns}:dying_wish 200 add_value

# Feedback
title @s times 5 40 15
title @s title ["⚔"]
title @s subtitle [{{"text":"DYING WISH — Berserk!","color":"dark_red"}}]
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.3 80 force @a[distance=..32]
playsound minecraft:item.totem.use player @a[distance=..32] ~ ~ ~ 1 0.8
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"blue"}},{{"text":" refuses to die!","color":"gray"}}]
""")

	## Per-tick berserk countdown (called from player/tick while dw_timer >= 1). @s = player.
	write_versioned_function("zombies/perks/dying_wish_tick", f"""
particle minecraft:crit ~ ~1 ~ 0.4 0.6 0.4 0.05 4 force @a[distance=..24]
scoreboard players remove @s {ns}.zb.dw_timer 1
execute if score @s {ns}.zb.dw_timer matches ..0 run function {ns}:v{version}/zombies/perks/dying_wish_end
""")

	## Berserk ends: strip the buffs and leave the player at 1 HP. @s = player.
	write_versioned_function("zombies/perks/dying_wish_end", f"""
attribute @s minecraft:attack_damage modifier remove {ns}:dying_wish
effect clear @s minecraft:resistance
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:strength
effect clear @s minecraft:speed
tag @s remove {ns}.dying_wish_active
scoreboard players set @s {ns}.zb.dw_timer 0

# Left at 1 HP (BO behaviour). /data can't write a player's Health and the max-health clamp trick
# doesn't reliably pull current HP down (both attribute sets collapse in one tick), so deal an exact
# (Health - 1) hit with generic_kill — it bypasses armor, resistance and effects, landing the player
# on precisely 1 HP. Health*1000 for sub-HP precision; skip if already at/below 1.
execute store result score #dw_hp {ns}.data run data get entity @s Health 1000
scoreboard players remove #dw_hp {ns}.data 1000
execute if score #dw_hp {ns}.data matches 1.. run function {ns}:v{version}/zombies/perks/dying_wish_to_1
title @s times 3 25 10
title @s subtitle [{{"text":"...barely alive.","color":"gray"}}]
""")

	# Deal exactly (Health - 1) damage to land the player on 1 HP; #dw_hp = (Health-1)*1000. generic_kill has no source entity, so this never trips the entity_hurt_player handler.
	write_versioned_function("zombies/perks/dying_wish_to_1", f"""
execute store result storage {ns}:temp _dw_dmg.amount double 0.001 run scoreboard players get #dw_hp {ns}.data
data modify storage {ns}:temp _dw_dmg.type set value "minecraft:generic_kill"
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _dw_dmg
""")

