
#> mgs:v5.4.2/zombies/escort/set_range
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/escort/pick_range {range:48}
#			mgs:v5.4.2/zombies/escort/pick_range {range:72}
#			mgs:v5.4.2/zombies/escort/pick_range {range:96}
#
# @args		range (int)
#

$execute if score @s mgs.zb.escort_range matches $(range) run return 0
$scoreboard players set @s mgs.zb.escort_range $(range)
$attribute @s minecraft:follow_range base set $(range)

