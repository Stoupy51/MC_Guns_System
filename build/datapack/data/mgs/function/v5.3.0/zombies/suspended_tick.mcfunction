
#> mgs:v5.3.0/zombies/suspended_tick
#
# @within	mgs:v5.3.0/zombies/freeze_tick
#

execute unless entity @a[scores={mgs.zb.in_game=1}] run return run scoreboard players set #zb_resume_timer mgs.data 0
scoreboard players add #zb_resume_timer mgs.data 1
scoreboard players set #zb_resume_left mgs.data 119
scoreboard players operation #zb_resume_left mgs.data -= #zb_resume_timer mgs.data
scoreboard players operation #zb_resume_left mgs.data /= #20 mgs.data
title @a[scores={mgs.zb.in_game=1}] actionbar [{"text":"⏸ ","color":"white"},{"translate":"mgs.paused","fallback":"PAUSED","color":"aqua","bold":true},[{"text":", ","color":"gray"}, {"translate":"mgs.resuming_in","fallback":"resuming in "}],{"score":{"name":"#zb_resume_left","objective":"mgs.data"},"color":"white"}]
execute if score #zb_resume_timer mgs.data matches 100.. run function mgs:v5.3.0/zombies/resume

