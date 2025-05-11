data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:70,Id:70,display:{Name:"{\"text\":\"FAMAS F1\",\"italic\":false}"}}
scoreboard players operation v0 V = famas_damage S
scoreboard players operation v1 V = famas_cooldown S
scoreboard players operation v2 V = famas_acc_sneaky S
scoreboard players operation v3 V = famas_mag S
scoreboard players operation v4 V = famas_reload S
function mgs:guns/_common/gen/gun