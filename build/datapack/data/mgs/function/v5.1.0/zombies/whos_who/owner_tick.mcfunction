
#> mgs:v5.1.0/zombies/whos_who/owner_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/tick [ at @s ]
#

# The body is id-linked via zb.ww.id (NOT zb.downed_id, which a later normal down overwrites)
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.ww.id

# ── Shared body upkeep (revive.py::revive_body_detect) ──
# Decrement bleed timer (real-time via #tick_delta)
scoreboard players operation @s mgs.zb.bleed -= #tick_delta mgs.data

# Check for revivers: alive non-downed players within range of THIS body (id-matched, since with
# several bodies 'nearest mannequin' could be someone else's)
scoreboard players set #zb_reviving mgs.data 0
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run scoreboard players set #zb_reviving mgs.data 1

# ── Shared revive progress (revive.py::revive_body_progress) ──
# If someone is reviving (=1), increment progress; if solo QR (=2), skip (solo_qr_tick handles it);
# if none (=0), decay at double speed. Real-time via #tick_delta.
execute if score #zb_reviving mgs.data matches 1 run scoreboard players operation @s mgs.zb.revive_p += #tick_delta mgs.data
scoreboard players operation #rv_decay mgs.data = #tick_delta mgs.data
scoreboard players operation #rv_decay mgs.data *= #2 mgs.data
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.revive_p matches 1.. run scoreboard players operation @s mgs.zb.revive_p -= #rv_decay mgs.data

# Show the revive progress bar to the revivers (snapshot @s's progress first: a reviver cannot
# reliably re-select the downed player, see show_reviver_bar)
scoreboard players operation #rv_reviver_disp mgs.data = @s mgs.zb.revive_p
execute if score #zb_reviving mgs.data matches 1 as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run function mgs:v5.1.0/zombies/revive/show_reviver_bar

# Update HUD text_display color based on revive state / bleed timer
execute if score #zb_reviving mgs.data matches 1.. run function mgs:v5.1.0/zombies/revive/hud_white
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches 400.. run function mgs:v5.1.0/zombies/revive/hud_yellow
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches 200..399 run function mgs:v5.1.0/zombies/revive/hud_gold
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches ..199 run function mgs:v5.1.0/zombies/revive/hud_red

# Revive complete (faster threshold if a reviver AT THE BODY has Quick Revive). return run: the
# caller's bleed-out checks below must not run on the completion tick (zb.bleed was reset to 0)
execute if score #zb_reviving mgs.data matches 1 run scoreboard players set #rv_qr_near mgs.data 0
execute if score #zb_reviving mgs.data matches 1 as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5,tag=mgs.perk.quick_revive] run scoreboard players set #rv_qr_near mgs.data 1
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 1 if score @s mgs.zb.revive_p matches 30.. run return run function mgs:v5.1.0/zombies/whos_who/revive_complete
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 0 if score @s mgs.zb.revive_p matches 60.. run return run function mgs:v5.1.0/zombies/whos_who/revive_complete

# Body bled out: doppelganger fights on with just the pistol (perks stay lost)
execute if score @s mgs.zb.bleed matches ..0 run function mgs:v5.1.0/zombies/whos_who/bleed_out

