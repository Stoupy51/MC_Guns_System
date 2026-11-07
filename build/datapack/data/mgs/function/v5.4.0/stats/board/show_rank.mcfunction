
#> mgs:v5.4.0/stats/board/show_rank
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/board/show with storage mgs:temp _lb_rank
#
# @args		k (unknown)
#

$data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:["",{translate:"mgs.your_rank",fallback:"Your rank",color:"gray"},": ",{text:"#$(k)",color:"gold"}]}

