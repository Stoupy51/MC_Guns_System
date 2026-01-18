
#> mgs:v5.0.0/sound/hearing/3_near
#
# @executed	as @a[distance=0.001..224] & facing entity @s eyes
#
# @within	mgs:v5.0.0/sound/propagation with storage mgs:gun all.stats
#
# @args		crack_type (unknown)
#

$execute if entity @s[distance=0..16] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.75
$execute if entity @s[distance=16..32] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.675
$execute if entity @s[distance=32..48] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.6
$execute if entity @s[distance=48..64] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.525
$execute if entity @s[distance=64..80] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.45
$execute if entity @s[distance=80..96] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.375
$execute if entity @s[distance=96..112] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.3
$execute if entity @s[distance=112..128] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.225
$execute if entity @s[distance=128..144] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.15
$execute if entity @s[distance=144..160] positioned as @s run playsound mgs:common/$(crack_type)_crack_3_near player @s ^ ^ ^-6 0.075

