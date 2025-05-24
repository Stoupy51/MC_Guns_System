
#> stoupgun:v5.0.0/sound/check_reload_end
#
# @within	stoupgun:v5.0.0/player/tick
#

# TODO:IF COOLDOWN = RELOAD_END, RUN:
execute store result score #reload_end stoupgun.data run data get storage stoupgun:gun all.stats.reload_end
execute if score @s stoupgun.cooldown = #reload_end stoupgun.data run function stoupgun:v5.0.0/sound/reload_end with storage stoupgun:gun all.stats

