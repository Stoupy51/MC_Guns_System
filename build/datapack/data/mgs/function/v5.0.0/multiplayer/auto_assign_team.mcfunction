
#> mgs:v5.0.0/multiplayer/auto_assign_team
#
# @within	???
#

# Count players on each team
execute store result score #red_count mgs.data if entity @a[scores={mgs.mp.team=1}]
execute store result score #blue_count mgs.data if entity @a[scores={mgs.mp.team=2}]

# Assign to team with fewer players (red if tied)
execute if score #red_count mgs.data <= #blue_count mgs.data run function mgs:v5.0.0/multiplayer/join_red
execute if score #red_count mgs.data > #blue_count mgs.data run function mgs:v5.0.0/multiplayer/join_blue

