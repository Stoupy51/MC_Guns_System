data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:520,Id:520,display:{Name:"{\"text\":\"RPK\",\"italic\":false}"}}
scoreboard players operation v0 V = rpk_damage S
scoreboard players operation v1 V = rpk_cooldown S
scoreboard players operation v2 V = rpk_acc_sneaky S
scoreboard players operation v3 V = rpk_mag S
scoreboard players operation v4 V = rpk_reload S
function mgs:guns/_common/gen/gun