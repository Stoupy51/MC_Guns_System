
#> mgs:v5.1.0/zombies/perks/dying_wish_trigger
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/on_down
#

# Not a real down — undo the downs++ that on_respawn added before calling on_down
scoreboard players remove @s mgs.zb.downs 1

# Count the use and set the escalating cooldown (60s * uses = 1200t * uses)
scoreboard players add @s mgs.zb.dw_uses 1
scoreboard players operation @s mgs.zb.dw_cd = @s mgs.zb.dw_uses
scoreboard players operation @s mgs.zb.dw_cd *= #1200 mgs.data

# Teleport back to the death location (reuse the revive tp macro)
execute store result storage mgs:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000
function mgs:v5.1.0/zombies/revive/tp_revive_pos with storage mgs:temp

# Restore: adventure mode, full health (respect Juggernog), stamina
gamemode adventure @s
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s mgs.stam_seen 0

# Berserk for 9s (180t): invulnerable (resistance V) + one-shot melee + mobility, and a big melee attribute
scoreboard players set @s mgs.zb.dw_timer 180
tag @s add mgs.dying_wish_active
effect give @s minecraft:resistance 180 4 true
effect give @s minecraft:fire_resistance 180 0 true
effect give @s minecraft:strength 180 4 true
effect give @s minecraft:speed 180 1 true
attribute @s minecraft:attack_damage modifier add mgs:dying_wish 200 add_value

# Feedback
title @s times 5 40 15
title @s title ["⚔"]
title @s subtitle [{"translate":"mgs.dying_wish_berserk","color":"dark_red"}]
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.3 80 force @a[distance=..32]
playsound minecraft:item.totem.use player @a[distance=..32] ~ ~ ~ 1 0.8
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"blue"},[{"text":" ","color":"gray"}, {"translate":"mgs.refuses_to_die"}]]

