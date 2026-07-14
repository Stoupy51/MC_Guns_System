Here is the closest **implementation-level reconstruction** of the **BO1 Zombies Stamin-Up / stamina system** that is publicly documented. BO1 Zombies Stamin-Up first appears on **Ascension**, costs **2000 points**, and is described as the Zombies version of **Marathon + Lightweight**: it gives **double sprint endurance** and a **7% movement-speed increase**. It is not the BO1 Multiplayer “Marathon Pro” version, which had unlimited sprint; Zombies Stamin-Up keeps sprint finite and just extends it. ([Call of Duty Wiki][1])

```text
Core state

player.hasStaminUp           // perk owned
player.isSprinting            // current locomotion state
player.sprintEnergy           // current sprint resource
player.sprintEnergyMax        // max sprint resource
player.sprintDrainRate
player.sprintRegenRate
player.moveSpeedMult          // final movement multiplier

Initialization

if hasStaminUp:
    sprintEnergyMax = baseSprintEnergyMax * 2
    moveSpeedMult = baseMoveSpeedMult * 1.07
else:
    sprintEnergyMax = baseSprintEnergyMax
    moveSpeedMult = baseMoveSpeedMult
```

The runtime behavior is simple: while sprint input is held and `sprintEnergy > 0`, the game drains sprint energy and uses the sprint locomotion speed; when energy hits zero, the player is forced back to normal movement until energy regenerates. Stamin-Up only changes the endurance budget and the global movement multiplier; it does not add tactical sprint, firing while sprinting, or any extra BO1-only side effect. ([Call of Duty Wiki][1])

```text
Per-frame update

if sprint button held AND sprintEnergy > 0:
    isSprinting = true
    sprintEnergy -= sprintDrainRate * deltaTime
    if sprintEnergy <= 0:
        sprintEnergy = 0
        isSprinting = false
else:
    isSprinting = false
    sprintEnergy += sprintRegenRate * deltaTime
    sprintEnergy = clamp(sprintEnergy, 0, sprintEnergyMax)

finalMoveSpeed = baseWeaponMoveSpeed * moveSpeedMult
```

The important detail for a faithful recode is that the perk is **multiplicative**, not additive: it scales the player’s existing movement model rather than replacing it. The underlying engine also treats movement speed as something affected by the equipped weapon, so the perk sits on top of weapon mobility rather than overriding it. That is why Stamin-Up feels strongest on slow weapons and during long train routes. ([Call of Duty Wiki][1])

As we are in Minecraft, make sure the saturation you give doesn't go higher than what's visible (every tick give saturation 0 during 1 tick until it foodLevel reaches 20, then the hunger effect will affect directly).
Also you could use a slow hunger effect to show to the player that they are sprinting too much, no sound effet and no "out of breath" message

