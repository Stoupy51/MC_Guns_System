tag @s add self
playsound mgs:common.rocket_crack player @s ~ ~ ~ 1.0
execute as @a[tag=!self,distance=0..16] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.65
execute as @a[tag=!self,distance=16..32] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.6
execute as @a[tag=!self,distance=32..48] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.55
execute as @a[tag=!self,distance=48..64] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.5
execute as @a[tag=!self,distance=64..80] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.45
execute as @a[tag=!self,distance=80..96] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.4
execute as @a[tag=!self,distance=96..112] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.35
execute as @a[tag=!self,distance=112..128] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.3
execute as @a[tag=!self,distance=128..144] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.25
execute as @a[tag=!self,distance=144..160] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.2
execute as @a[tag=!self,distance=160..176] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.15
execute as @a[tag=!self,distance=176..192] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.1
execute as @a[tag=!self,distance=192..208] at @s run playsound mgs:common.rocket_crack player @s ~ ~ ~ 0.05
playsound mgs:common.rocket_crack_mono player @a[tag=!self] ~ ~ ~ 14
tag @s remove self
