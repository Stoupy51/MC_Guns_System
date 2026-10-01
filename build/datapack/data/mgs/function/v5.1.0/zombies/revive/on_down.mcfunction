
#> mgs:v5.1.0/zombies/revive/on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/on_respawn
#

# Dying Wish first: off cooldown, it replaces going down with a berserk. Must stay above Who's Who.
execute if score @s mgs.zb.perk.dying_wish matches 1 if score @s mgs.zb.dw_cd matches ..0 run return run function mgs:v5.1.0/zombies/perks/dying_wish_trigger

# A doppelganger going down again forfeits their unrevived body first (BO2 rule), then goes down normally
# (or as a fresh Who's Who if they rebought it).
execute if entity @s[tag=mgs.ww_active] run function mgs:v5.1.0/zombies/whos_who/forfeit

# Who's Who: play on as a doppelganger with a pistol while the body waits for a revive, solo or co-op.
# It sits above the solo Quick Revive and Tombstone paths, so it wins over both.
execute if score @s mgs.zb.perk.whos_who matches 1 run return run function mgs:v5.1.0/zombies/whos_who/on_down

scoreboard players set @s mgs.zb.downed 1
scoreboard players set @s mgs.zb.bleed 1200
scoreboard players set @s mgs.zb.revive_p 0
tag @s add mgs.downed_spectator

# on_respawn already set it to 0.
scoreboard players set @s mgs.mp.death_count 0

# Unique downed id, then the revivable body (mannequin and name HUD) at the death spot.
scoreboard players add #downed_id_next mgs.data 1
scoreboard players operation @s mgs.zb.downed_id = #downed_id_next mgs.data
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/revive/spawn_downed_body

# Electric Cherry: a full-strength discharge (used == cap == 1) before the perk is stripped (BO behaviour).
scoreboard players set #ec_used mgs.data 1
scoreboard players set #ec_cap mgs.data 1
execute if score @s mgs.special.electric_cherry matches 1 at @s run function mgs:v5.1.0/zombies/perks/electric_cherry_shock

# Tombstone: snapshot the perks before they are stripped. Never reached by a Who's Who down.
execute if score @s mgs.zb.perk.tombstone matches 1 run function mgs:v5.1.0/zombies/perks/tombstone_on_down

# Solo Quick Revive: snapshot ownership before lose_all strips the perk, since the auto-revive runs a tick later
# from downed_tick. Recomputed on every down.
tag @s remove mgs.zb_qr_armed
execute if entity @s[tag=mgs.perk.quick_revive] run tag @s add mgs.zb_qr_armed

function mgs:v5.1.0/zombies/perks/lose_all

gamemode spectator @s

# The spectator rides this item_display for a locked third-person view.
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.downed_cam","mgs.downed_cam_new","mgs.gm_entity"],teleport_duration:1}

scoreboard players operation @n[tag=mgs.downed_cam_new] mgs.zb.downed_id = @s mgs.zb.downed_id

# Id-matched, since with Who's Who bodies around the nearest mannequin can be someone else's.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run tp @n[tag=mgs.downed_cam_new] ^ ^2 ^-3
tag @e[tag=mgs.downed_cam_new] remove mgs.downed_cam_new

execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tag @s add mgs.downed_mine_temp
ride @s mount @n[tag=mgs.downed_mine_temp]
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp

title @s times 0 60 20
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_are_down_a_teammate_can_revive_you","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"red"}],[{"text":" ","color":"gray"}, {"translate":"mgs.is_down"}]]

