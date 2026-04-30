
#> mgs:v5.0.0/zombies/revive/revive_complete
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick
#			mgs:v5.0.0/zombies/revive/solo_qr_complete
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Store mannequin position before killing it
execute store result storage mgs:temp rv_x double 0.001 run data get entity @n[tag=mgs.downed_mannequin] Pos[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get entity @n[tag=mgs.downed_mannequin] Pos[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get entity @n[tag=mgs.downed_mannequin] Pos[2] 1000

# Hide mannequin and HUD by teleporting far below the world (avoids kill animation/drops)
tp @n[tag=mgs.downed_mannequin] ~ -10000 ~
tp @n[tag=mgs.downed_hud] ~ -10000 ~
tag @n[tag=mgs.downed_mannequin] remove mgs.downed_mannequin
tag @n[tag=mgs.downed_hud] remove mgs.downed_hud
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_cam] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run kill @s

# Dismount from camera entity and restore adventure mode
ride @s dismount
gamemode adventure @s

# Teleport player to where the mannequin was
function mgs:v5.0.0/zombies/revive/tp_revive_pos with storage mgs:temp

# Restore max health (check for Juggernog perk)
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full and re-apply saturation
effect give @s minecraft:instant_health 1 255 true
effect give @s minecraft:saturation infinite 255 true

# Announce
title @s title [{"text":"❤","color":"green"}]
title @s subtitle [{"translate":"mgs.you_have_been_revived","color":"green"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_been_revived"}]]

