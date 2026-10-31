
#> mgs:v5.3.0/zombies/spawn_name
#
# @within	mgs:v5.3.0/zombies/summon_spawn_iter with storage mgs:temp _spawn_label
#
# @args		group_id (int)
#			name (unknown)
#			sid (unknown)
#

$data modify storage mgs:temp _spos.name set value "$(name) #$(sid) (group $(group_id))"

