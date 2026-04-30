
#> mgs:v5.0.0/zombies/revive/downed_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/tick [ at @s ]
#

# Decrement bleed timer
scoreboard players remove @s mgs.zb.bleed 1

# Third-person view: teleport camera item_display to 3 blocks behind and 2 above the mannequin
# Player rides the item_display, so camera follows it automatically
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run tag @s add mgs.downed_mine_temp
execute as @n[tag=mgs.downed_mine_temp] at @s as @e[tag=mgs.downed_cam] if score @s mgs.zb.downed_id = #my_downed_id mgs.data at @n[tag=mgs.downed_mine_temp] run tp @s ^ ^2 ^-3
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# Re-mount player onto camera entity every tick (ensures no accidental dismount)
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[tag=mgs.downed_cam] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run tag @s add mgs.downed_mine_temp
ride @s mount @n[tag=mgs.downed_mine_temp]
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# Sync mannequin yaw from player look direction — use downed_id to target correct mannequin
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run tag @s add mgs.downed_mine_temp
execute as @n[tag=mgs.downed_mine_temp] run data modify entity @s Rotation[0] set from entity @p[tag=mgs.downed_spectator] Rotation[0]
execute as @n[tag=mgs.downed_mine_temp] run data modify entity @s Rotation[1] set value 0.0f
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

# Move mannequin using Bookshelf motion (smooth, physics-based, no tp stuttering)
# Zero out velocity first, then accumulate based on active inputs
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.x 0
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.y 0
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.z 0

# Forward/backward: local +Z / -Z (scale: 80 = 0.08 blocks/tick at scale:0.001)
execute if entity @s[predicate=mgs:v5.0.0/input/forward] as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.z 60
execute if entity @s[predicate=mgs:v5.0.0/input/backward] as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.z -60

# Left/right: local +X / -X
execute if entity @s[predicate=mgs:v5.0.0/input/left] as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.x 60
execute if entity @s[predicate=mgs:v5.0.0/input/right] as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run scoreboard players set @s bs.vel.x -60

# Convert local velocity (relative to mannequin facing) to canonical (world), then apply motion
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data at @s rotated as @s run function #bs.move:local_to_canonical
execute as @e[tag=mgs.downed_mannequin] if score @s mgs.zb.downed_id = #my_downed_id mgs.data run function #bs.move:set_motion {scale:0.001}

# Keep HUD text_display anchored 2 blocks above the mannequin
execute as @n[tag=mgs.downed_mannequin] at @s run tp @n[tag=mgs.downed_hud] ~ ~2 ~

# Check for revivers (alive non-downed players within range of mannequin)
scoreboard players set #zb_reviving mgs.data 0
execute as @n[tag=mgs.downed_mannequin] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run scoreboard players set #zb_reviving mgs.data 1

# Solo Quick Revive auto-revive: if no teammates in-game and player has quick_revive + uses left
execute if score #zb_reviving mgs.data matches 0 if entity @s[tag=mgs.perk.quick_revive] unless score #zb_solo_revive_block mgs.data matches 1 run function mgs:v5.0.0/zombies/revive/check_solo_qr

# If someone is reviving, increment progress; if not, decay
execute if score #zb_reviving mgs.data matches 1.. run scoreboard players add @s mgs.zb.revive_p 1
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.revive_p matches 1.. run scoreboard players remove @s mgs.zb.revive_p 2

# Show bleed timer on downed player's actionbar ONLY when not in solo QR (which has its own actionbar)
# Compute display: whole seconds and tenths digit (sec = bleed/20, tenth = (bleed%20)/2)
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_sec mgs.data = @s mgs.zb.bleed
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_sec mgs.data /= #20 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data = @s mgs.zb.bleed
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data %= #20 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run scoreboard players operation #rv_disp_tenth mgs.data /= #2 mgs.data
execute if score #zb_reviving mgs.data matches ..1 run data modify storage smithed.actionbar:input message set value {json:[[{"text":"☠ ","color":"red"}, {"translate":"mgs.bleeding_out"}],{"score":{"name":"#rv_disp_sec","objective":"mgs.data"},"color":"gray"},{"text":".","color":"gray"},{"score":{"name":"#rv_disp_tenth","objective":"mgs.data"},"color":"gray"},{"text":"s","color":"dark_gray"}],priority:"override",freeze:2}
execute if score #zb_reviving mgs.data matches ..1 run function #smithed.actionbar:message

# Show revive progress bar to nearby alive players (from mannequin position)
execute if score #zb_reviving mgs.data matches 1 as @n[tag=mgs.downed_mannequin] at @s run execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] run function mgs:v5.0.0/zombies/revive/show_reviver_bar

# Update HUD text_display color based on revive state / bleed timer
execute if score #zb_reviving mgs.data matches 1.. run function mgs:v5.0.0/zombies/revive/hud_white
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches 400.. run function mgs:v5.0.0/zombies/revive/hud_orange
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches 200..399 run function mgs:v5.0.0/zombies/revive/hud_gold
execute if score #zb_reviving mgs.data matches 0 if score @s mgs.zb.bleed matches ..199 run function mgs:v5.0.0/zombies/revive/hud_red

# Check revive complete (Quick Revive threshold if reviver nearby has perk; normal otherwise)
# Use matches 1 (exactly) to exclude solo QR mode (which sets #zb_reviving=2)
execute if score #zb_reviving mgs.data matches 1 if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5,tag=mgs.perk.quick_revive] if score @s mgs.zb.revive_p matches 30.. run function mgs:v5.0.0/zombies/revive/revive_complete
execute if score #zb_reviving mgs.data matches 1 unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5,tag=mgs.perk.quick_revive] if score @s mgs.zb.revive_p matches 60.. run function mgs:v5.0.0/zombies/revive/revive_complete

# Bleed out: time's up
execute if score @s mgs.zb.bleed matches ..0 run function mgs:v5.0.0/zombies/revive/bleed_out

