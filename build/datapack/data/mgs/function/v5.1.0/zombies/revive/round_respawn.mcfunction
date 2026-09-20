
#> mgs:v5.1.0/zombies/revive/round_respawn
#
# @within	mgs:v5.1.0/zombies/round_complete
#

# Surviving the round while downed is a free pickup, wherever the body fell and whoever was near it:
# the round is over, every zombie is dead, and the bleed timer never ran out. Losing a full loadout
# because a Nuke cleared the last zombie instead of a teammate reaching you is not a play the player
# could have made differently. Reviving through revive_complete is what keeps the inventory: it only
# restores state and teleports, and never touches the hotbar. Perks stay lost, like any other revive.
# Must run before the respawn pass below, which would otherwise wipe them back to the starting loadout.
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/revive/revive_complete

# Respawn every remaining spectator: they bled out during the round, and that still costs the loadout
execute as @a[scores={mgs.zb.in_game=1},gamemode=spectator] run function mgs:v5.1.0/zombies/revive/do_round_respawn

