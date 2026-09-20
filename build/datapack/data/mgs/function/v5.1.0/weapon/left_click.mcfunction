
#> mgs:v5.1.0/weapon/left_click
#
# @within	???
#

# The enchantment only sits on our guns, but a player can left-click mid-swap: re-check the mainhand
# so a click landing on the frame the weapon changes can't retarget whatever is held now.
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run return 0

function mgs:v5.1.0/utils/copy_gun_data

# Guard throwables/knives: no reload_time -> ammo/reload would set a garbage cooldown and lock the item
execute unless data storage mgs:gun all.stats.reload_time run return 0

# Safe to spam: ammo/reload returns fail while reloading or already full
function mgs:v5.1.0/ammo/reload

