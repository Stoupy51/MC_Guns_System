
#> mgs:v5.1.0/zombies/revive/downed_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/tick [ at @s ]
#

# Identify THIS player's downed entities for the id-matching predicate, then tag the mannequin ONCE
# as downed_mine_temp. Every per-mannequin command below reuses that tag (or a single dispatch into
# move_mannequin) instead of re-selecting the mannequin ~11x per tick.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
tag @e[tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] add mgs.downed_mine_temp

# Read crawl inputs into scratch scores while @s is still the player (predicate self-checks on @s,
# no entity scan). These drive the mannequin's local velocity inside move_mannequin.
# Also snapshot the owner's yaw (x100): move_mannequin must not use a "nearest downed spectator"
# lookup, which binds to the wrong owner when several mannequins are close together.
execute store result score #rv_yaw mgs.data run data get entity @s Rotation[0] 100
scoreboard players set #crawl_vx mgs.data 0
scoreboard players set #crawl_vz mgs.data 0
execute if entity @s[predicate=mgs:v5.1.0/input/forward] run scoreboard players set #crawl_vz mgs.data 60
execute if entity @s[predicate=mgs:v5.1.0/input/backward] run scoreboard players set #crawl_vz mgs.data -60
execute if entity @s[predicate=mgs:v5.1.0/input/left] run scoreboard players set #crawl_vx mgs.data 60
execute if entity @s[predicate=mgs:v5.1.0/input/right] run scoreboard players set #crawl_vx mgs.data -60

# Third-person camera: position the cam item_display 2 up / 3 behind the mannequin (using the
# mannequin's CURRENT rotation, i.e. before this tick's yaw sync — same order as before), then
# re-mount the player onto the cam so the view follows it.
execute at @n[tag=mgs.downed_mine_temp] as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tp @s ^ ^2 ^-3
ride @s mount @n[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match]

# All remaining per-mannequin work (yaw sync, crawl motion, HUD anchor) in ONE pass over the tagged
# mannequin instead of re-selecting it for each command.
execute as @n[tag=mgs.downed_mine_temp] at @s run function mgs:v5.1.0/zombies/revive/move_mannequin

# Done with the per-tick mannequin tag
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# ── Shared body upkeep (revive.py::revive_body_detect) ──
# Decrement bleed timer (real-time via #tick_delta)
scoreboard players operation @s mgs.zb.bleed -= #tick_delta mgs.data

# Check for revivers: alive non-downed players within range of THIS body (id-matched, since with
# several bodies 'nearest mannequin' could be someone else's)
scoreboard players set #zb_reviving mgs.data 0
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run scoreboard players set #zb_reviving mgs.data 1

# Solo Quick Revive auto-revive: if no teammates in-game and player has quick_revive + uses left
execute if score #zb_reviving mgs.data matches 0 if entity @s[tag=mgs.perk.quick_revive] unless score #zb_solo_revive_block mgs.data matches 1 run function mgs:v5.1.0/zombies/revive/check_solo_qr

# Show bleed timer on downed player's actionbar ONLY when not in solo QR (which has its own actionbar)
# Compute display: whole seconds and tenths digit (sec = bleed/20, tenth = (bleed%20)/2)
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_sec mgs.data = @s mgs.zb.bleed
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_sec mgs.data /= #20 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data = @s mgs.zb.bleed
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data %= #20 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data /= #2 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run data modify storage smithed.actionbar:input message set value {json:[[{"text":"☠ ","color":"red"}, {"translate":"mgs.bleeding_out"}],{"score":{"name":"#rv_disp_sec","objective":"mgs.data"},"color":"gray"},{"text":".","color":"gray"},{"score":{"name":"#rv_disp_tenth","objective":"mgs.data"},"color":"gray"},{"text":"s","color":"dark_gray"}],priority:"override",freeze:2}
execute if score #zb_reviving mgs.data matches ..1 run function #smithed.actionbar:message

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
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 1 if score @s mgs.zb.revive_p matches 30.. run return run function mgs:v5.1.0/zombies/revive/revive_complete
execute if score #zb_reviving mgs.data matches 1 if score #rv_qr_near mgs.data matches 0 if score @s mgs.zb.revive_p matches 60.. run return run function mgs:v5.1.0/zombies/revive/revive_complete

# Bleed out: time's up
execute if score @s mgs.zb.bleed matches ..0 run function mgs:v5.1.0/zombies/revive/bleed_out

# Instant bleed out: if no healthy players remain and no solo QR auto-revive is active,
# there is no hope of revive — end the suspense immediately
execute if score #zb_reviving mgs.data matches 0 unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run function mgs:v5.1.0/zombies/revive/bleed_out

