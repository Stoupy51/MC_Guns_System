data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:330,Id:330,display:{Name:"{\"text\":\"M590\",\"italic\":false}"}}
scoreboard players set v0 V 3
scoreboard players operation v0 V *= m590_damage S
scoreboard players operation v1 V = m590_cooldown S
scoreboard players operation v2 V = m590_acc_sneaky S
scoreboard players operation v3 V = m590_mag S
scoreboard players operation v4 V = m590_mag S
scoreboard players operation v4 V *= m590_reload S
function mgs:guns/_common/gen/gun