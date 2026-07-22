
#> mgs:v5.1.0/zombies/doors/announce_progress
#
# @executed	as @e[tag=mgs.door_new]
#
# @within	mgs:v5.1.0/zombies/doors/on_right_click
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.chipped_in"}],{"score":{"name":"#door_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"green"}, {"translate":"mgs.points_for"}],{"storage":"mgs:temp","nbt":"_door_hover_name","color":"gold","interpret":true},{"text":"  (","color":"gray"},{"score":{"name":"#door_paid","objective":"mgs.data"},"color":"green"},{"text":"/","color":"gray"},{"score":{"name":"#door_total","objective":"mgs.data"},"color":"yellow"},{"text":")","color":"gray"}]
function mgs:v5.1.0/zombies/feedback/sound_announce

