
#> mgs:v5.0.0/sound/hearing/4_closest
#
# @within	mgs:v5.0.0/sound/propagation with storage mgs:gun all.stats
#

$execute if entity @s[distance=0..16] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.45
$execute if entity @s[distance=16..32] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.4
$execute if entity @s[distance=32..48] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.35
$execute if entity @s[distance=48..64] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.3
$execute if entity @s[distance=64..80] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.25
$execute if entity @s[distance=80..96] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.2
$execute if entity @s[distance=96..112] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.15
$execute if entity @s[distance=112..128] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.1
$execute if entity @s[distance=128..144] positioned as @s run playsound mgs:common/$(crack_type)_crack_4_closest player @s ^ ^ ^-12 0.05

