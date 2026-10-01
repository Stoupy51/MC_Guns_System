
#> mgs:v5.1.0/zombies/whos_who/owner_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/tick [ at @s ]
#

# zb.ww.id, not zb.downed_id, which a later normal down overwrites.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.ww.id

# Body upkeep (revive_body_detect).
scoreboard players operation @s mgs.zb.bleed -= #tick_delta mgs.data

# Id-matched, since with several bodies the nearest mannequin can be someone else's.
scoreboard players set #zb_reviving mgs.data 0
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run scoreboard players set #zb_reviving mgs.data 1

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
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 1 if score @s mgs.zb.revive_p matches 30.. run return run function mgs:v5.1.0/zombies/whos_who/revive_complete
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 0 if score @s mgs.zb.revive_p matches 60.. run return run function mgs:v5.1.0/zombies/whos_who/revive_complete

# The doppelganger fights on with the pistol; perks stay lost.
execute if score @s mgs.zb.bleed matches ..0 run function mgs:v5.1.0/zombies/whos_who/bleed_out

