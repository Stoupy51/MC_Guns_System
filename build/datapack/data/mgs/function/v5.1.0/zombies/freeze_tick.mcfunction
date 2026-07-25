
#> mgs:v5.1.0/zombies/freeze_tick
#
# @within	mgs:v5.1.0/tick
#

scoreboard players add #zb_freeze_msg mgs.data 1
execute if score #zb_freeze_msg mgs.data matches 20.. run scoreboard players set #zb_freeze_msg mgs.data 0
execute if score #zb_freeze_msg mgs.data matches 0 run title @a[scores={mgs.zb.in_game=1}] actionbar [[{"text":"⏸ ","color":"aqua","bold":true}, {"translate":"mgs.game_frozen"}]]

