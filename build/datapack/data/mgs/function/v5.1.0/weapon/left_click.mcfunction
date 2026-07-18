
#> mgs:v5.1.0/weapon/left_click
#
# @within	???
#

# The enchantment only sits on our guns, but a player can left-click mid-swap: re-check the mainhand
# so a click landing on the frame the weapon changes can't retarget whatever is held now.
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run return 0

function mgs:v5.1.0/utils/copy_gun_data

# Only weapons that actually have a second mode respond. Throwables carry a fire_mode too, so
# without this the toggle would pointlessly rewrite the item and fire the change signal on grenades.
execute unless data storage mgs:gun all.stats.can_auto unless data storage mgs:gun all.stats.can_burst run return 0

# Cycle the mode (auto -> semi -> burst -> auto, narrowed to whatever the weapon supports).
function mgs:v5.1.0/switch/do_toggle_fire_mode

