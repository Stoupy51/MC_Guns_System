data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:420,Id:420,display:{Name:"{\"text\":\"M82A1\",\"italic\":false}"}}
scoreboard players operation v0 V = m82_damage S
scoreboard players operation v1 V = m82_cooldown S
scoreboard players operation v2 V = m82_acc_sneaky S
scoreboard players operation v3 V = m82_mag S
scoreboard players operation v4 V = m82_reload S
function mgs:guns/_common/gen/gun