data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:440,Id:440,display:{Name:"{\"text\":\"M24A3\",\"italic\":false}"}}
scoreboard players operation v0 V = m24_damage S
scoreboard players operation v1 V = m24_cooldown S
scoreboard players operation v2 V = m24_acc_sneaky S
scoreboard players operation v3 V = m24_mag S
scoreboard players operation v4 V = m24_mag S
scoreboard players operation v4 V *= mosin_reload S
function mgs:guns/_common/gen/gun