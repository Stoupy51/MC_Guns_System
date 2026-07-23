
#> mgs:v5.1.0/zombies/revive/revive_complete
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#			mgs:v5.1.0/zombies/revive/solo_qr_complete
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Identify THIS player's mannequin by downed_id — with several downed players,
# a 'nearest mannequin' lookup could consume someone else's mannequin and revive at the wrong place
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
tag @e[tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] add mgs.downed_mine_temp

# Store mannequin position before hiding it. Track read success: if the mannequin is missing,
# the storage would keep a stale position (this is how players ended up respawning at 0 0 0)
scoreboard players set #rv_pos_ok mgs.data 0
execute store success score #rv_pos_ok mgs.data run data get entity @n[tag=mgs.downed_mine_temp] Pos
execute store result storage mgs:temp rv_x double 0.001 run data get entity @n[tag=mgs.downed_mine_temp] Pos[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get entity @n[tag=mgs.downed_mine_temp] Pos[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get entity @n[tag=mgs.downed_mine_temp] Pos[2] 1000

# Hide mannequin and HUD by teleporting far below the world (avoids kill animation/drops)
tp @n[tag=mgs.downed_mine_temp] ~ -10000 ~
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tp @s ~ -10000 ~
tag @n[tag=mgs.downed_mine_temp] remove mgs.downed_mannequin
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tag @s remove mgs.downed_hud
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run kill @s

# Dismount from camera entity and restore adventure mode
ride @s dismount
gamemode adventure @s

# Teleport player to where the mannequin was; if it couldn't be found, fall back to a safe
# spawn point near a teammate instead of teleporting to a stale position (e.g. 0 0 0)
execute if score #rv_pos_ok mgs.data matches 1 run function mgs:v5.1.0/zombies/revive/tp_revive_pos with storage mgs:temp
execute unless score #rv_pos_ok mgs.data matches 1 run function mgs:v5.1.0/zombies/revive/respawn_near_player

# Restore max health (check for Juggernog perk)
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full and reset stamina to full (the stamina system owns the hunger bar)
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s mgs.stam_seen 0

# Tombstone: revived → discard the pending marker + perk snapshot (nothing to recover)
function mgs:v5.1.0/zombies/perks/tombstone_on_revived

# Announce
title @s title ["❤"]
title @s subtitle [{"translate":"mgs.you_have_been_revived","color":"green"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_been_revived"}]]

