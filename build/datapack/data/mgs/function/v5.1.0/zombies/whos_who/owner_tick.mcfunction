
#> mgs:v5.1.0/zombies/whos_who/owner_tick
#
# @executed	as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/whos_who/tick [ as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}] ]
#

# Bleed timer on the body
scoreboard players operation @s mgs.zb.ww.bleed -= #tick_delta mgs.data

# Identify this owner's body/HUD
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id

# Any alive in-game player (including the doppelganger themselves) within range of the body = reviving
scoreboard players set #ww_reviving mgs.data 0
execute as @e[tag=mgs.ww_body,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..2.5] run scoreboard players set #ww_reviving mgs.data 1

# Progress / decay
scoreboard players operation #ww_decay mgs.data = #tick_delta mgs.data
scoreboard players operation #ww_decay mgs.data *= #2 mgs.data
execute if score #ww_reviving mgs.data matches 1 run scoreboard players operation @s mgs.zb.ww.rev += #tick_delta mgs.data
execute if score #ww_reviving mgs.data matches 0 if score @s mgs.zb.ww.rev matches 1.. run scoreboard players operation @s mgs.zb.ww.rev -= #ww_decay mgs.data

# Body particles + keep the HUD anchored above the body
execute as @e[tag=mgs.ww_body,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] at @s run particle minecraft:soul ~ ~1 ~ 0.2 0.4 0.2 0.01 2 force @a[distance=..48]

# Reviving actionbar for the doppelganger
execute if score #ww_reviving mgs.data matches 1 run data modify storage smithed.actionbar:input message set value {json:[{"translate":"mgs.reviving_your_body","color":"dark_aqua"}],priority:"override",freeze:2}
execute if score #ww_reviving mgs.data matches 1 run function #smithed.actionbar:message

# Revive complete
execute if score @s mgs.zb.ww.rev matches 60.. run function mgs:v5.1.0/zombies/whos_who/revive_complete

# Body bled out: doppelganger fights on with just the pistol (perks stay lost)
execute if score @s mgs.zb.ww.bleed matches ..0 run function mgs:v5.1.0/zombies/whos_who/bleed_out

