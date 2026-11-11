
#> mgs:v5.4.2/switch/adopt_fire_modes
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/switch/main with storage mgs:gun all.stats
#
# @args		base_weapon (unknown)
#

$execute unless data storage mgs:data fire_modes.$(base_weapon) run return fail
$data modify storage mgs:gun all.stats.fire_modes set from storage mgs:data fire_modes.$(base_weapon)
data modify storage mgs:gun all.stats.fire_mode set from storage mgs:gun all.stats.fire_modes[0].name
data remove storage mgs:gun all.stats.can_auto
data remove storage mgs:gun all.stats.can_burst
data remove storage mgs:gun all.stats.burst
item modify entity @s weapon.mainhand mgs:v5.4.2/update_stats

