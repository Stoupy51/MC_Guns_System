
#> mgs:v5.4.4/lobby/vote/add_map
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/vote/collect_map
#

data modify storage mgs:temp _lv_opt set value {label:{text:"",color:"aqua"},hover:{text:""}}
data modify storage mgs:temp _lv_opt.label.text set from storage mgs:temp _lv_iter[0].name
data modify storage mgs:temp _lv_opt.hover.text set from storage mgs:temp _lv_iter[0].description
data modify storage mgs:temp _lv_opt.map_id set from storage mgs:temp _lv_iter[0].id
data modify storage mgs:temp _lv_opts append from storage mgs:temp _lv_opt

