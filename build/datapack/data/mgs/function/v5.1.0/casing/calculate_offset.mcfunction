
#> mgs:v5.1.0/casing/calculate_offset
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.1.0/casing/process_vectors
#

### Local casing offsets to world coordinates, through the gun's orientation vectors.

# Local offsets, x1000.
execute if score #is_zoom mgs.data matches 0 store result score #offset_x mgs.data run data get storage mgs:gun all.stats.casing_offset.normal[0] 1000
execute if score #is_zoom mgs.data matches 0 store result score #offset_y mgs.data run data get storage mgs:gun all.stats.casing_offset.normal[1] 1000
execute if score #is_zoom mgs.data matches 0 store result score #offset_z mgs.data run data get storage mgs:gun all.stats.casing_offset.normal[2] 1000
execute if score #is_zoom mgs.data matches 1 store result score #offset_x mgs.data run data get storage mgs:gun all.stats.casing_offset.zoom[0] 1000
execute if score #is_zoom mgs.data matches 1 store result score #offset_y mgs.data run data get storage mgs:gun all.stats.casing_offset.zoom[1] 1000
execute if score #is_zoom mgs.data matches 1 store result score #offset_z mgs.data run data get storage mgs:gun all.stats.casing_offset.zoom[2] 1000

# Each axis is the sum of the offsets projected on binormal, normal and tangent, plus the start position.
scoreboard players operation #off_bx mgs.data = #binormal_x mgs.data
scoreboard players operation #off_bx mgs.data *= #offset_x mgs.data
scoreboard players operation #off_nx mgs.data = #normal_x mgs.data
scoreboard players operation #off_nx mgs.data *= #offset_y mgs.data
scoreboard players operation #off_tx mgs.data = #tangent_x mgs.data
scoreboard players operation #off_tx mgs.data *= #offset_z mgs.data

scoreboard players operation #pos_new_x mgs.data = #off_bx mgs.data
scoreboard players operation #pos_new_x mgs.data += #off_nx mgs.data
scoreboard players operation #pos_new_x mgs.data += #off_tx mgs.data
scoreboard players operation #pos_new_x mgs.data /= #1000 mgs.data

scoreboard players operation #pos_new_x mgs.data += #pos_initial_x mgs.data

scoreboard players operation #off_by mgs.data = #binormal_y mgs.data
scoreboard players operation #off_by mgs.data *= #offset_x mgs.data
scoreboard players operation #off_ny mgs.data = #normal_y mgs.data
scoreboard players operation #off_ny mgs.data *= #offset_y mgs.data
scoreboard players operation #off_ty mgs.data = #tangent_y mgs.data
scoreboard players operation #off_ty mgs.data *= #offset_z mgs.data

scoreboard players operation #pos_new_y mgs.data = #off_by mgs.data
scoreboard players operation #pos_new_y mgs.data += #off_ny mgs.data
scoreboard players operation #pos_new_y mgs.data += #off_ty mgs.data
scoreboard players operation #pos_new_y mgs.data /= #1000 mgs.data
scoreboard players operation #pos_new_y mgs.data += #pos_initial_y mgs.data

scoreboard players operation #off_bz mgs.data = #binormal_z mgs.data
scoreboard players operation #off_bz mgs.data *= #offset_x mgs.data
scoreboard players operation #off_nz mgs.data = #normal_z mgs.data
scoreboard players operation #off_nz mgs.data *= #offset_y mgs.data
scoreboard players operation #off_tz mgs.data = #tangent_z mgs.data
scoreboard players operation #off_tz mgs.data *= #offset_z mgs.data

scoreboard players operation #pos_new_z mgs.data = #off_bz mgs.data
scoreboard players operation #pos_new_z mgs.data += #off_nz mgs.data
scoreboard players operation #pos_new_z mgs.data += #off_tz mgs.data
scoreboard players operation #pos_new_z mgs.data /= #1000 mgs.data
scoreboard players operation #pos_new_z mgs.data += #pos_initial_z mgs.data

