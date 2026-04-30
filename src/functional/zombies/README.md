
# TODO:
- bonuses (max-ammo, insta-kill, double points, barrier repair, unlimited ammo, nuke, random perk, free pap (player only), cash drop)
- grenades
- Revive system:
  - Currently completely broken.
  - Use "/data get entity @s LastDeathLocation.pos" to get the position of the last death, and teleport there after respawned of death (when @e[type=player] is able to select player, because @a is able to select dead players)
  - We don't want the downed player to be attacked by zombies, so we will use mannequin:
    - https://minecraft.wiki/w/Mannequin
    - When player dies, we summon a mannequin with the same skin and armor as the player, and tag it with {ns}.downed. We also teleport the mannequin to the player's death location. The mannequin should have Invulnerable:1b, so it can't be damaged by players or zombies. The player will be teleported in spectator mode inside the mannequin (/spectate) and we can help move the mannequin slowly by detecting the spectator's input using predicate, content:
      - https://github.com/Stoupy51/ShoppingKart/raw/refs/heads/main/build/datapack/data/shopping_kart/predicate/input/any.json
      - https://github.com/Stoupy51/ShoppingKart/raw/refs/heads/main/build/datapack/data/shopping_kart/predicate/input/backward.json
      - https://github.com/Stoupy51/ShoppingKart/raw/refs/heads/main/build/datapack/data/shopping_kart/predicate/input/forward.json
      - https://github.com/Stoupy51/ShoppingKart/raw/refs/heads/main/build/datapack/data/shopping_kart/predicate/input/left.json
      - https://github.com/Stoupy51/ShoppingKart/raw/refs/heads/main/build/datapack/data/shopping_kart/predicate/input/right.json
    - This will simulate the player being downed and crawling on the ground. The player can be revived by another player just by being near the mannequin, this will show a progress bar in actionbar using priority "override" using smithed.actionbar.
    - After 3 seconds of being revived, the mannequin disappears and the player is teleported out of spectator mode and can play again.
    - If the player is not revived within 30 seconds, they will die and respawn normally, and the mannequin will disappear.
    - To indicate to other players the revive state of the player, we will use text display like in multiplayer domination: always being above the mannequin and slowly changing color from orange to red as the revive timer goes down and turn white while being revived.
- PAP fire sounds
- Traps damage:
  - Currently, it does a fixed amount of damage. It should do infinite damage
- Visuals for mystery box, pap, and perks

