
#> mgs:v5.0.0/raycast/on_targeted_block
#
# @within	mgs:v5.0.0/raycast/main
#

# If the block can be passed through, increment back piercing, and stop here if it's not water
scoreboard players set #is_pass_through mgs.data 0
execute if block ~ ~ ~ #bs.hitbox:can_pass_through run scoreboard players set #is_pass_through mgs.data 1
execute if score #is_pass_through mgs.data matches 1 run scoreboard players add $raycast.piercing bs.lambda 1
execute if score #is_pass_through mgs.data matches 1 unless block ~ ~ ~ #mgs:v5.0.0/sounds/water run return 1

# Allow bullets to pierce 2 blocks at most (if block isn't water)
execute if score #is_pass_through mgs.data matches 0 if score $raycast.piercing bs.lambda matches 1..3 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score #is_pass_through mgs.data matches 0 if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 3

# Reduce damage by 50% in air, 20% in water
execute if score #is_pass_through mgs.data matches 0 store result storage mgs:gun all.stats.damage float 0.5 run data get storage mgs:gun all.stats.damage
execute if score #is_pass_through mgs.data matches 1 store result storage mgs:gun all.stats.damage float 0.8 run data get storage mgs:gun all.stats.damage

## Playsounds
# Each sound type has a scoreboard objective that tracks if it has been played.
# The score is set to 1 when the sound plays, preventing it from playing again.
# The 'run return run' command ensures only one sound tries to play per block hit
# (e.g. if water already played and it's water again, it will not trigger soft)
execute if score #is_pass_through mgs.data matches 1 run return run execute if score #played_water mgs.data matches 0 store success score #played_water mgs.data run playsound minecraft:entity.axolotl.splash block @a[distance=..24] ~ ~ ~ 0.8 1.5
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/glass run return run execute if score #played_glass mgs.data matches 0 store success score #played_glass mgs.data run playsound minecraft:block.glass.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/cloth run return run execute if score #played_cloth mgs.data matches 0 store success score #played_cloth mgs.data run playsound mgs:common/cloth_bullet_impact block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/dirt run return run execute if score #played_dirt mgs.data matches 0 store success score #played_dirt mgs.data run playsound mgs:common/dirt_bullet_impact block @a[distance=..24] ~ ~ ~ 0.3
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/mud run return run execute if score #played_mud mgs.data matches 0 store success score #played_mud mgs.data run playsound mgs:common/mud_bullet_impact block @a[distance=..24] ~ ~ ~ 0.4
execute if block ~ ~ ~ #mgs:v5.0.0/sounds/wood run return run execute if score #played_wood mgs.data matches 0 store success score #played_wood mgs.data run playsound mgs:common/wood_bullet_impact block @a[distance=..24] ~ ~ ~ 0.5
execute if block ~ ~ ~ #mgs:v5.0.0/plant run return run execute if score #played_plant mgs.data matches 0 store success score #played_plant mgs.data run playsound minecraft:block.azalea_leaves.break block @a[distance=..24] ~ ~ ~ 1
execute if block ~ ~ ~ #mgs:v5.0.0/solid run return run execute if score #played_solid mgs.data matches 0 store success score #played_solid mgs.data run playsound mgs:common/solid_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2
execute if score #played_soft mgs.data matches 0 store success score #played_soft mgs.data run playsound mgs:common/soft_bullet_impact block @a[distance=..24] ~ ~ ~ 0.2

