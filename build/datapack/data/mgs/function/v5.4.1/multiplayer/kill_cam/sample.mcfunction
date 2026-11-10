
#> mgs:v5.4.1/multiplayer/kill_cam/sample
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/record [ at @s ]
#

tp 006d6773-0000-0000-0000-000000006b63 ~ ~ ~ ~ ~
data modify storage mgs:kill_cam frames[-1].s append value {}
execute store result storage mgs:kill_cam frames[-1].s[-1].id int 1 run scoreboard players get @s bs.id
data modify storage mgs:kill_cam frames[-1].s[-1].p set from entity 006d6773-0000-0000-0000-000000006b63 Pos
data modify storage mgs:kill_cam frames[-1].s[-1].r set from entity 006d6773-0000-0000-0000-000000006b63 Rotation
execute if predicate mgs:v5.4.1/is_sneaking run data modify storage mgs:kill_cam frames[-1].s[-1].sneak set value 1b

