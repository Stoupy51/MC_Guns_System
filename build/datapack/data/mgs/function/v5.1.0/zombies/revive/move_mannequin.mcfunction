
#> mgs:v5.1.0/zombies/revive/move_mannequin
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick [ at @s ]
#

execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #rv_yaw mgs.data
data modify entity @s Rotation[1] set value 0.0f

# Bookshelf physics: XZ from the crawl inputs, and a constant downward Y because set_motion overrides gravity.
scoreboard players operation @s bs.vel.x = #crawl_vx mgs.data
scoreboard players set @s bs.vel.y -400
scoreboard players operation @s bs.vel.z = #crawl_vz mgs.data
function #bs.move:local_to_canonical
function #bs.move:set_motion {scale:0.001}

tp @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] ~ ~2 ~

