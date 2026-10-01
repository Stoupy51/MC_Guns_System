
#> mgs:v5.1.0/zombies/revive/downed_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/tick [ at @s ]
#

# Tag this player's mannequin once; everything below reuses that tag.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
tag @e[tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] add mgs.downed_mine_temp

# Crawl inputs and yaw (x100) are read here, while @s is the player, because move_mannequin cannot
# find its owner reliably when several mannequins are close.
execute store result score #rv_yaw mgs.data run data get entity @s Rotation[0] 100
scoreboard players set #crawl_vx mgs.data 0
scoreboard players set #crawl_vz mgs.data 0
execute if entity @s[predicate=mgs:v5.1.0/input/forward] run scoreboard players set #crawl_vz mgs.data 60
execute if entity @s[predicate=mgs:v5.1.0/input/backward] run scoreboard players set #crawl_vz mgs.data -60
execute if entity @s[predicate=mgs:v5.1.0/input/left] run scoreboard players set #crawl_vx mgs.data 60
execute if entity @s[predicate=mgs:v5.1.0/input/right] run scoreboard players set #crawl_vx mgs.data -60

# Camera 2 up and 3 behind the mannequin's rotation from before this tick's yaw sync, then the player re-mounts it.
execute at @n[tag=mgs.downed_mine_temp] as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tp @s ^ ^2 ^-3
ride @s mount @n[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match]

execute as @n[tag=mgs.downed_mine_temp] at @s run function mgs:v5.1.0/zombies/revive/move_mannequin

tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# Body upkeep (revive_body_detect).
scoreboard players operation @s mgs.zb.bleed -= #tick_delta mgs.data

# Id-matched, since with several bodies the nearest mannequin can be someone else's.
scoreboard players set #zb_reviving mgs.data 0
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run scoreboard players set #zb_reviving mgs.data 1

# Solo Quick Revive: gated on the zb_qr_armed snapshot, since lose_all already removed the perk (see on_down).
execute if score #zb_reviving mgs.data matches 0 if entity @s[tag=mgs.zb_qr_armed] run function mgs:v5.1.0/zombies/revive/check_solo_qr

# Bleed timer, except during the solo Quick Revive (which has its own actionbar): seconds = bleed / 20, tenths = (bleed % 20) / 2.
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_sec mgs.data = @s mgs.zb.bleed
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_sec mgs.data /= #20 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data = @s mgs.zb.bleed
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data %= #20 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data /= #2 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run data modify storage smithed.actionbar:input message set value {json:[{"text":"☠ ","color":"white"},{"translate":"mgs.bleeding_out","color":"red"},{"score":{"name":"#rv_disp_sec","objective":"mgs.data"},"color":"gray"},{"text":".","color":"gray"},{"score":{"name":"#rv_disp_tenth","objective":"mgs.data"},"color":"gray"},{"text":"s","color":"dark_gray"}],priority:"override",freeze:2}
execute if score #zb_reviving mgs.data matches ..1 run function #smithed.actionbar:message

# Progress (revive_body_progress): +delta while someone revives (1), nothing during a solo revive (2), 2x decay otherwise (0).
execute if score #zb_reviving mgs.data matches 1 run scoreboard players operation @s mgs.zb.revive_p += #tick_delta mgs.data
scoreboard players operation #rv_decay mgs.data = #tick_delta mgs.data
scoreboard players operation #rv_decay mgs.data *= #2 mgs.data
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.revive_p matches 1.. run scoreboard players operation @s mgs.zb.revive_p -= #rv_decay mgs.data

# Snapshot for the reviver bar: a reviver cannot reliably select the downed player.
scoreboard players operation #rv_reviver_disp mgs.data = @s mgs.zb.revive_p
tag @a remove mgs.zb_reviver
execute if score #zb_reviving mgs.data matches 1 as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run function mgs:v5.1.0/zombies/revive/show_reviver_bar

execute if score #zb_reviving mgs.data matches 1.. run function mgs:v5.1.0/zombies/revive/hud_white
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches 400.. run function mgs:v5.1.0/zombies/revive/hud_yellow
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches 200..399 run function mgs:v5.1.0/zombies/revive/hud_gold
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches ..199 run function mgs:v5.1.0/zombies/revive/hud_red

# Faster when a reviver at the body owns Quick Revive. `return run`: zb.bleed is 0 on the completion tick,
# so the caller's bleed-out checks must not run.
execute if score #zb_reviving mgs.data matches 1 run scoreboard players set #rv_qr_near mgs.data 0
execute if score #zb_reviving mgs.data matches 1 as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5,tag=mgs.perk.quick_revive] run scoreboard players set #rv_qr_near mgs.data 1
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 1 if score @s mgs.zb.revive_p matches 30.. run return run function mgs:v5.1.0/zombies/revive/revive_complete
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 0 if score @s mgs.zb.revive_p matches 60.. run return run function mgs:v5.1.0/zombies/revive/revive_complete

execute if score @s mgs.zb.bleed matches ..0 run function mgs:v5.1.0/zombies/revive/bleed_out

# No healthy player left and no solo revive running: bleed out now.
execute if score #zb_reviving mgs.data matches 0 unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run function mgs:v5.1.0/zombies/revive/bleed_out

