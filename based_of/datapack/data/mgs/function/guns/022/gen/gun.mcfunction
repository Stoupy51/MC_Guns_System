data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:220,Id:220,display:{Name:"{\"text\":\"MAC-10\",\"italic\":false}"}}
scoreboard players operation v0 V = mac10_damage S
scoreboard players operation v1 V = mac10_cooldown S
scoreboard players operation v2 V = mac10_acc_sneaky S
scoreboard players operation v3 V = mac10_mag S
scoreboard players operation v4 V = mac10_reload S
function mgs:guns/_common/gen/gun