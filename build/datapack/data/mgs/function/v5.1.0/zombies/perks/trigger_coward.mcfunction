
#> mgs:v5.1.0/zombies/perks/trigger_coward
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/check_coward
#

function mgs:v5.1.0/zombies/respawn_tp

scoreboard players set @s mgs.zb.ability_cd 1

effect give @s speed 5 1 true
effect give @s regeneration 5 1 true

title @s actionbar [{"text":"🏃 ","color":"white"},{"translate":"mgs.coward_activated_teleported_to_safety","color":"yellow"}]

