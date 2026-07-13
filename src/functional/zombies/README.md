
# TODO:
- E:\my_folders\advanced_desktop\StoupGun\README.md the part about the map editor is too long, need to compress it!
- make so that a zombie can never respawn to the same location as the previous one (remember the id of the spawn point). Also, the detect of zombies stuck should evolve: If staying in the same spot (after 20s), then only take 5 seconds to respawn if not moved. If the entity moved but doesn't get closer to player, then take 15 seconds to respawn.
- When shooting too many entities, limit the number of particles spawned (to avoid lag, like particles only for 3 entities max per shot (not pellets))
- When shooting with ray gun and killing an entity, we see the debug damage message hitting an item_display (that should not be there)
- We were two players, I bought quick revive and not the other player, and when both of us died, instead of game ending, it was trying to self revive me but at the end of the time it revived airdox, that was very strange.
- When reviving someone, the increment score on actionbar is telling 0/60t. Fix that, and also use seconds instead of ticks.
- Due to strange respawn behaviors, I was respawned at 0 0 0 in blocks, and I died. Prevent that.
- When shooting through barrier blocks, damages get divided by so much that they become 0, that's an issue.
- For projectiles, their are stopped by barrier blocks, they need to be not be stopped by barrier blocks. https://docs.mcbookshelf.dev/en/latest/modules/move/
- Kino der toten, when game ended, entities interactions were still there. Fix that by adding the common tag that removes all entities when the game ends.

- idea for better zombie AI: use a different entity (for instance warden)

