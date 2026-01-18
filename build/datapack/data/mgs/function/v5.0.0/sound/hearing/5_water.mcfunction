
#> mgs:v5.0.0/sound/hearing/5_water
#
# @executed	as @a[distance=0.001..224] & facing entity @s eyes
#
# @within	mgs:v5.0.0/sound/propagation with storage mgs:gun all.stats
#
# @args		crack_type (unknown)
#

$execute if entity @s[distance=0..16] positioned as @s run playsound mgs:common/$(crack_type)_crack_5_water player @s ^ ^ ^-6 0.225
$execute if entity @s[distance=16..32] positioned as @s run playsound mgs:common/$(crack_type)_crack_5_water player @s ^ ^ ^-6 0.15
$execute if entity @s[distance=32..48] positioned as @s run playsound mgs:common/$(crack_type)_crack_5_water player @s ^ ^ ^-6 0.075

