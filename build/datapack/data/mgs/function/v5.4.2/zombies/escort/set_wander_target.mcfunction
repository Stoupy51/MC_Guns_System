
#> mgs:v5.4.2/zombies/escort/set_wander_target
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/escort/retarget with entity @s data.walk_to
#			mgs:v5.4.2/zombies/escort/retarget with storage mgs:temp _escort
#			mgs:v5.4.2/zombies/escort/retarget_lure with storage mgs:temp _escort
#			mgs:v5.4.2/zombies/escort/retarget_monkey with storage mgs:temp _escort
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute positioned $(x) $(y) $(z) run function mgs:v5.4.2/zombies/escort/pick_range

$scoreboard players set #zb_esc_dx mgs.data $(x)
$scoreboard players set #zb_esc_dy mgs.data $(y)
$scoreboard players set #zb_esc_dz mgs.data $(z)
scoreboard players operation #zb_esc_dx mgs.data -= @s mgs.zb.escort_tx
scoreboard players operation #zb_esc_dy mgs.data -= @s mgs.zb.escort_ty
scoreboard players operation #zb_esc_dz mgs.data -= @s mgs.zb.escort_tz
execute if score #zb_esc_dx mgs.data matches -3..3 if score #zb_esc_dy mgs.data matches -3..3 if score #zb_esc_dz mgs.data matches -3..3 if data entity @s wander_target run return 0

$data modify entity @s wander_target set value [I;$(x),$(y),$(z)]
$scoreboard players set @s mgs.zb.escort_tx $(x)
$scoreboard players set @s mgs.zb.escort_ty $(y)
$scoreboard players set @s mgs.zb.escort_tz $(z)

