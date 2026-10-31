# Feature Specification: Zombie Spawn Profiles

**Feature Branch**: `010-zombie-spawn-profiles`

**Created**: 2026-10-30

**Status**: Built. Not a full Spec Kit folder on purpose: the decisions below were settled with the author before the work, this file keeps them and what not to forget.

## Map format

Every field is optional; a missing one keeps the behaviour maps had before it existed.

| Where | Field | Meaning |
|---|---|---|
| zombie and special spawns | `mob` | `{entity:"zombie", gun:..., nbt:{...}, riders:[<mob>, ...]}`. Default: `{entity:"zombie"}` on zombie spawns, `{entity:"wolf"}` (the hound) on special spawns. To vary, place several spawns at the same spot. |
| | `mob.gun` | Absent: the round decides (Zonweeb armed type). `false`: never armed. `{id?, level?}`: always armed; no `id` draws a non-explosive gun, an `id` without `level` is level 1, neither is the round's tier (1 to round 5, 2 to 10, 3 to 15, 4 after). |
| | `mob.nbt` | Merged into the entity; the round's health and speed always win over it. |
| | `mob.riders` | Mobs of the same format riding it, recursively. A whole stack takes 1 from the round's quota; each rider is an enemy of its own. |
| | `min_round`, `max_round` | Inclusive; 0 means from the start and never ending. |
| | `arrival` | `floor`, `ceiling`, `portal` or `instant`. Default `floor` on zombie spawns, `portal` on special ones. Replaces `from_ceiling`, which no saved map used (checked in the author's world). |
| zombie spawns only | `power` | Usable only once the power is on. |
| doors | `min_round` | Shared by every door of a `link_id`: hovering shows "Locked until round N", clicks are refused, nothing is announced. |
| mystery box spots | `rotation[1]`, `roll` | Pitch -90 to 90, roll 0/90/180/270; the yaw is free (only placement snaps it to 45). |

## Decisions

1. One spawn path for every enemy (`zombies/mob/*`): the hound is the `wolf` preset, the dog code is gone.
2. Presets by entity type, applied before the map's `nbt`: zombie (Silent, 15 attack, no knockback), wolf (black, 1.5 scale, 12 attack, no knockback). Every other entity keeps its vanilla stats.
3. Round scaling for every enemy: BO health (a `max_health` modifier, so wolf NBT writes cannot reset it), speed (horde curve, hound curve for wolves), death intercept, points, power-ups, stuck rescue, waypoint, horde team.
4. Zonweeb types only replace a plain zombie: the spawn's own mob, without `nbt`, `riders` or `gun`.
5. Special rounds (every 5th from 5) happen only when a special spawn is open (door) and in its round bounds; otherwise the round is normal. Example: special spawns with `max_round:14` (wolves) and `min_round:15` with `{entity:"spider"}`.
6. No open spawn: the enemy stays queued; the existing watchdog closes the round after 20 s.
7. Neutral mobs (wolf, bee, iron golem, polar bear, enderman, zombified piglin) get an anger target every second.
8. Spawn eligibility lives in marker tags: round bounds checked at each round start, doors on opening, power on activation, activation boxes once a second.
9. Zombies' random guns come from the catalog without explosives; Missions keep the RPG-7 on purpose (a death does not end a mission).
10. Technical entities (markers, displays, interactions) carry English names with their id in game, and names showing their configuration in the editor, refreshed by the editor's once-a-second sync.

## Not to forget

- Gun damage: enemy shots deal the gun's full damage with distance decay; the zombies multipliers only apply to players. The only "nerf" is the 60 ticks on, 40 off duty cycle and the mob spread. `level` only shows in the name.
- The 5% Max Ammo drop applies to every armed enemy, not only the Zonweeb armed type.
- Spiders only target players in the dark (vanilla light check).
- Entities created and killed within one function (raycast markers, probes, item shuttles) are left unnamed: naming them would cost an NBT write per shot.
- Removed tags `mgs.zb_dog`, `mgs.dog_portal`, `mgs.zb_scaled`, `mgs.spawn_from_ceiling`; a game suspended in the middle of a special round across the update loses its pending portals (the watchdog recovers the round).
- New objectives: `mgs.zb.spawn.rmin`, `mgs.zb.spawn.rmax`, `mgs.zb.door.minr`, `mgs.mb.roll`.
- Editor forms save through `/function`, so the client asks to confirm each save.
