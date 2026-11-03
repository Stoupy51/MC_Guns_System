
#> mgs:v5.3.0/zombies/escort/set_range
#
# @executed	as @n[tag=mgs.zb_escort_new] & at @s
#
# @within	mgs:v5.3.0/zombies/escort/pick_range {range:48}
#			mgs:v5.3.0/zombies/escort/pick_range {range:72}
#			mgs:v5.3.0/zombies/escort/pick_range {range:96}
#
# @args		range (int)
#

$execute if score @s mgs.zb.escort_range matches $(range) run return 0
$scoreboard players set @s mgs.zb.escort_range $(range)
$attribute @s minecraft:follow_range base set $(range)

