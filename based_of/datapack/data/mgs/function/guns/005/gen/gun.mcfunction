data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:50,Id:50,display:{Name:"{\"text\":\"M4A1\",\"italic\":false}"}}
scoreboard players operation v0 V = m4_damage S
scoreboard players operation v1 V = m4_cooldown S
scoreboard players operation v2 V = m4_acc_sneaky S
scoreboard players operation v3 V = m4_mag S
scoreboard players operation v4 V = m4_reload S
function mgs:guns/_common/gen/gun