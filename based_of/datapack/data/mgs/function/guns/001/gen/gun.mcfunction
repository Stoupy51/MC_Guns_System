data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:10,Id:10,display:{Name:"{\"text\":\"M16A4\",\"italic\":false}"}}
scoreboard players operation v0 V = m16_damage S
scoreboard players operation v1 V = m16_cooldown S
scoreboard players operation v2 V = m16_acc_sneaky S
scoreboard players operation v3 V = m16_mag S
scoreboard players operation v4 V = m16_reload S
function mgs:guns/_common/gen/gun