
#> mgs:v5.1.0/zombies/revive/revive_complete
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#			mgs:v5.1.0/zombies/revive/solo_qr_complete
#			mgs:v5.1.0/zombies/revive/round_respawn [ as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] ]
#

scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# By downed_id: with several downed players, the nearest mannequin can be someone else's.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
tag @e[tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] add mgs.downed_mine_temp

# The read can fail when the mannequin is missing, which would keep a stale position (players respawned at 0 0 0).
scoreboard players set #rv_pos_ok mgs.data 0
execute store success score #rv_pos_ok mgs.data run data get entity @n[tag=mgs.downed_mine_temp] Pos
execute store result storage mgs:temp rv_x double 0.001 run data get entity @n[tag=mgs.downed_mine_temp] Pos[0] 1000
execute store result storage mgs:temp rv_y double 0.001 run data get entity @n[tag=mgs.downed_mine_temp] Pos[1] 1000
execute store result storage mgs:temp rv_z double 0.001 run data get entity @n[tag=mgs.downed_mine_temp] Pos[2] 1000
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

function mgs:v5.1.0/zombies/revive/hide_body

ride @s dismount
gamemode adventure @s

# Mannequin not found: a safe spawn near a teammate instead of a stale position.
execute if score #rv_pos_ok mgs.data matches 1 run function mgs:v5.1.0/zombies/revive/tp_revive_pos with storage mgs:temp
execute unless score #rv_pos_ok mgs.data matches 1 run function mgs:v5.1.0/zombies/revive/respawn_near_player

execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# The stamina system owns the hunger bar.
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s mgs.stam_seen 0

# Tombstone: revived, so nothing to recover.
function mgs:v5.1.0/zombies/perks/tombstone_on_revived

title @s times 5 40 15
title @s title ["❤"]
title @s subtitle [{"translate":"mgs.you_have_been_revived","color":"green"}]
tag @a remove mgs.xp_earner
tag @a[tag=mgs.zb_reviver] add mgs.xp_earner
tellraw @a[scores={mgs.zb.in_game=1},tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"green"}],[{"text":" ","color":"gray"}, {"translate":"mgs.has_been_revived"}]]
tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"green"}],[{"text":" ","color":"gray"}, {"translate":"mgs.has_been_revived"}],[" ",{"text":"+10 XP","color":"gold"}]]
execute as @a[tag=mgs.xp_earner] run function mgs:v5.1.0/progression/zb/award_revive
tag @a remove mgs.xp_earner

