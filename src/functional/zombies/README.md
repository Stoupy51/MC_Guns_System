
# FIXME:
- PaP machine:
  - Should change scope randomly each time you send your weapon in (should change scope when coming out of PaP), also should add component "enchantment_glint_override=true"
  - The ammo lore didn't get the pap suffix.
  - Magazine capacity should update to 8x the base weapon capacity
  - The animation is not accurate. It should properly use interpolation, rotation, and translation.
    - All should be horizontal movement. And timings are incorrect, check internet for black ops pap animation for reference.
  - Messages are not correctly timed
  - If the weapon is not picked up, it should disappear.

- Perks, mystery box, etc. are not placed with proper yaw even tho it's configured in editor
- Editor doesn't show option for item model overrides for PaP, perks, and mystery box.

- RayGun magazine bug: loosing item_model because conversion from consumable to not is scuffed

