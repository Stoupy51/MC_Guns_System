
#> mgs:v5.1.0/zombies/escort/update_lure
#
# @within	mgs:v5.1.0/zombies/game_tick
#

execute store result score #zb_lure_alive mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
scoreboard players set #zb_lure_inpap mgs.data 0
execute as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] at @s if entity @e[tag=mgs.pap_machine,distance=..14] run scoreboard players add #zb_lure_inpap mgs.data 1

scoreboard players set #zb_lure mgs.data 0
execute if score #zb_lure_alive mgs.data matches 1.. if score #zb_lure_inpap mgs.data = #zb_lure_alive mgs.data run scoreboard players set #zb_lure mgs.data 1

# Start center-bound escorts on a few stray zombies while luring (cap-gated; the retarget in
# escort/start reads #zb_lure and aims at the centre marker)
execute if score #zb_lure mgs.data matches 1 if score #zb_escort_count mgs.data matches ..7 as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,tag=!mgs.zb_escorted,tag=!mgs.zb_escort_failed,limit=2,sort=random] at @s unless entity @e[tag=mgs.lure_center,distance=..16] run function mgs:v5.1.0/zombies/escort/start

