data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:40,Id:40,display:{Name:"{\"text\":\"AUG A3\",\"italic\":false}"}}
scoreboard players operation v0 V = aug_damage S
scoreboard players operation v1 V = aug_cooldown S
scoreboard players operation v2 V = aug_acc_sneaky S
scoreboard players operation v3 V = aug_mag S
scoreboard players operation v4 V = aug_reload S
function mgs:guns/_common/gen/gun