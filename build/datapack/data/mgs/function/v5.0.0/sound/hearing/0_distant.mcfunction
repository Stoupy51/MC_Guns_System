
#> mgs:v5.0.0/sound/hearing/0_distant
#
# @executed	as @a[distance=0.001..224] & facing entity @s eyes
#
# @within	mgs:v5.0.0/sound/propagation with storage mgs:gun all.sounds
#
# @args		crack (unknown)
#

$execute if entity @s[distance=0..32] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.9
$execute if entity @s[distance=32..48] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.825
$execute if entity @s[distance=48..64] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.75
$execute if entity @s[distance=64..80] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.675
$execute if entity @s[distance=80..96] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.6
$execute if entity @s[distance=96..112] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.525
$execute if entity @s[distance=112..128] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.45
$execute if entity @s[distance=128..144] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.375
$execute if entity @s[distance=144..160] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.3
$execute if entity @s[distance=160..176] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.225
$execute if entity @s[distance=176..192] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.15
$execute if entity @s[distance=192..208] positioned as @s run playsound mgs:common/$(crack)_crack_0_distant player @s ^ ^ ^-6 0.075

