data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:320,Id:320,display:{Name:"{\"text\":\"M500\",\"italic\":false}"}}
scoreboard players set v0 V 3
scoreboard players operation v0 V *= m500_damage S
scoreboard players operation v1 V = m500_cooldown S
scoreboard players operation v2 V = m500_acc_sneaky S
scoreboard players operation v3 V = m500_mag S
scoreboard players operation v4 V = m500_mag S
scoreboard players operation v4 V *= m500_reload S
function mgs:guns/_common/gen/gun