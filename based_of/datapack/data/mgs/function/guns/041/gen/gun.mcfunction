data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:410,Id:410,display:{Name:"{\"text\":\"SVD-63\",\"italic\":false}"}}
scoreboard players operation v0 V = svd_damage S
scoreboard players operation v1 V = svd_cooldown S
scoreboard players operation v2 V = svd_acc_sneaky S
scoreboard players operation v3 V = svd_mag S
scoreboard players operation v4 V = svd_reload S
function mgs:guns/_common/gen/gun