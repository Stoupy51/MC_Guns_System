
#> mgs:v5.1.0/weapon/left_click
#
# @within	enchantment mgs:left_click
#

# A left click can land on the frame the weapon changes, so the main hand is checked again.
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run return 0

function mgs:v5.1.0/utils/copy_gun_data

# Throwables and knives have no reload_time: ammo/reload would set a garbage cooldown and lock the item.
execute unless data storage mgs:gun all.stats.reload_time run return 0

# ammo/reload fails while reloading or full, so spamming is safe.
function mgs:v5.1.0/ammo/reload

