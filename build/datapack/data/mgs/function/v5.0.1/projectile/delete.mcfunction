
#> mgs:v5.0.1/projectile/delete
#
# @executed	at @s
#
# @within	mgs:v5.0.1/projectile/explode
#

# Decrease slow bullet counter and kill entity
scoreboard players remove #slow_bullet_count mgs.data 1
kill @s

