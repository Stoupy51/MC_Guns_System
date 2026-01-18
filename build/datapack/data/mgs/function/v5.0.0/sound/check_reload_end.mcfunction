
#> mgs:v5.0.0/sound/check_reload_end
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# If cooldown is reload end, and player was reloading, playsound
execute store result score #reload_end mgs.data run data get storage mgs:gun all.stats.reload_end
execute if score @s mgs.cooldown = #reload_end mgs.data run function mgs:v5.0.0/sound/reload_end with storage mgs:gun all.stats

