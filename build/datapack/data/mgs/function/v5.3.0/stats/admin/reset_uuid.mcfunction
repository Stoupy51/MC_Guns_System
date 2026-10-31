
#> mgs:v5.3.0/stats/admin/reset_uuid
#
# @within	mgs:v5.3.0/stats/admin/reset with storage mgs:temp _st_one
#
# @args		uuid (unknown)
#

$data modify storage mgs:temp _st_one.name set from storage mgs:stats players."$(uuid)".name
function mgs:v5.3.0/stats/admin/reset_name with storage mgs:temp _st_one

