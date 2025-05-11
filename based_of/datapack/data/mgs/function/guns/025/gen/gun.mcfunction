data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:250,Id:250,display:{Name:"{\"text\":\"Sten MK II\",\"italic\":false}"}}
scoreboard players operation v0 V = sten_damage S
scoreboard players operation v1 V = sten_cooldown S
scoreboard players operation v2 V = sten_acc_sneaky S
scoreboard players operation v3 V = sten_mag S
scoreboard players operation v4 V = sten_reload S
function mgs:guns/_common/gen/gun