
#> mgs:v5.0.0/multiplayer/end_prep
#
# @within	mgs:v5.0.0/multiplayer/start 200t [ scheduled ]
#

# Only if still preparing (game might have been stopped)
execute unless data storage mgs:multiplayer game{state:"preparing"} run return fail

# Restore movement
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision

# Re-apply permanent saturation for the active game
effect give @a[scores={mgs.mp.in_game=1}] saturation infinite 255 true

# Set state to active
data modify storage mgs:multiplayer game.state set value "active"

# Announce
tellraw @a [{"text":"","color":"green","bold":true},"⚔ ",{"translate": "mgs.go_go_go"}]

