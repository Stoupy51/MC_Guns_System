
#> mgs:v5.1.0/zombies/revive/move_mannequin
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick [ at @s ]
#

# Sync mannequin yaw from the owner's look direction (snapshotted into #rv_yaw x100 by downed_tick)
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #rv_yaw mgs.data
data modify entity @s Rotation[1] set value 0.0f

# Crawl motion via Bookshelf physics. XZ from the crawl-input scratch scores (0 when no input is held);
# Y a constant downward pull so the mannequin doesn't float off ledges (set_motion overrides gravity).
scoreboard players operation @s bs.vel.x = #crawl_vx mgs.data
scoreboard players set @s bs.vel.y -400
scoreboard players operation @s bs.vel.z = #crawl_vz mgs.data
function #bs.move:local_to_canonical
function #bs.move:set_motion {scale:0.001}

# Keep the HUD text_display anchored 2 blocks above the mannequin (id-matched via #my_downed_id)
tp @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] ~ ~2 ~

