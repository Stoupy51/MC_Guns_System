
#> mgs:v5.4.0/multiplayer/editor/start_secondary_mags
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/save
#

data modify storage mgs:temp _mag_data set from storage mgs:temp _build.secondary_data
execute store result score #pmag_count mgs.data run data get storage mgs:temp editor.secondary_mag_count
execute if score #pmag_count mgs.data matches 1.. run function mgs:v5.4.0/multiplayer/editor/append_mag_slots

