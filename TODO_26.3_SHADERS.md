# 26.3 shaders: what to verify in game

The migration is written. Reference material lives in [POSTEFFECT_26.3.md](specs/POSTEFFECT_26.3.md);
this file is only the list of things that cannot be checked from a build.

Everything below is verified in game, except the Iris items still open.

---

## What the pack now ships

`assets/mgs/post_effect/` holds 38 ids, all applied per player through `/posteffect`. There is no
`end_of_frame`, no core shader override and no marker particle.

| Family                                    | Ids | Applied by                                                        |
|-------------------------------------------|-----|-------------------------------------------------------------------|
| `mgs:flash`, `_pap`, `_zoom`, `_pap_zoom` | 4   | `player/apply_flash_if_can_see`, taken off by `player/flash_tick` |
| `mgs:zoom_{2,3,4}` and `_out`             | 6   | `zoom/fx_enter`, `zoom/fx_leave`, `zoom/fx_tick`                  |
| `mgs:crosshair_{0..4}_{0..4}`             | 25  | `zoom/crosshair_spread`                                           |
| `mgs:hurt`, `mgs:hurt_critical`           | 2   | `player/hurt_tick`                                                |
| `mgs:debug_clock`                         | 1   | by hand                                                           |

Each chain is three passes: stamp the activation time into a 1x1 persistent target, copy it back,
then one fullscreen pass. `mgs:clock.glsl` holds the pack and ramp helpers.

---

## Test in this order

Stop at the first failure. Everything rests on step 1.

- [x] **The clock.** `/posteffect add @s mgs:debug_clock`. A green strip should appear at the bottom
      of the screen and sweep across once every 10 ticks, turning blue (settled) after a minute. Red means the persistent target never
      reported an unarmed frame, which invalidates every timed effect. No strip at all means the
      chain failed to compile, so check the log and remember that a compile error blacklists the id
      until F3+T.
- [x] **Re-arming.** Remove it, wait a second, add it again. The sweep must restart from the left.
      If it resumes where it left off, `closePersistentTargets` is not doing what the source says
      and the flash will not repeat correctly.
- [x] **No grid.** Nothing tiled or offset anywhere on screen with any effect applied.
- [x] **Muzzle flash.** Full strength for one tick, gone after about 80 ms, and **behind the gun**.
      The fastest automatic weapon should flash 10 times per second, each burst distinct.
- [x] **Flash while someone else shoots.** Stand near a shooter. The bloom is screen centred, which
      is how it already behaved, but check that the spark sprite shows in the right place and that
      line of sight still gates it through walls.
- [x] **Pack-a-Punch flash** picks the purple id.
- [x] **Aim down sights** on a scoped weapon: the magnification and the lens distortion ramp in over
      about a third of a second, then hold. Release: they ramp back out over 0.2 s and the id comes
      off. Tapping sneak repeatedly inside that 0.2 s window snaps back to zero first, which is
      known and accepted.
- [x] **Unscoped weapon** gets the centre pull with no barrel distortion.
- [x] **Weapon switch while aiming** clears the overlay (`zoom/clear_state`).
- [x] **Crosshair** shows the base size with no gun, animates with movement while holding a gun or
      a grenade, and disappears while aiming.
- [x] **Low health.** Below 40% a vignette with an uneven, drifting edge; below 20% the heartbeat
      and rim colour separation too. Heal up fast and it fades out over 2 seconds.
- [x] **Leaving a game** while hurt takes the overlay off, and so does the round ending.
- [x] **Relog** mid-round: ids are stored in player NBT, so they should come back intact and the
      mirror scores should still agree with them.
- [x] **Death and respawn:** the server drops the effect list on respawn, and `{ns}.fx_deaths`
      resets the mirror scores, so the crosshair should be back within one tick.

---

## Known regressions

- **No third-person special casing.** The old marker particle carried a camera-to-particle distance
  that let the shader suppress the spark sprite in F5. Nothing in a post effect can see the camera
  perspective, so the sprite now draws in third person too.
- **Re-aiming during the zoom fade-out restarts the ramp from zero** rather than from the current
  value, because the two directions are separate ids with separate clocks.
- **The crosshair ramp starts from the previous transition's end,** not from the current
  interpolated value, so changing movement state mid-ramp gives a small jump.
- **First use of an id costs a pipeline compile.** 25 crosshair variants compile lazily as the
  player first hits each movement pair. If that stutters, warm them at game start.

---

## Iris

Post effects compose with shaderpacks (see [POSTEFFECT_26.3.md](specs/POSTEFFECT_26.3.md) section 7), but
none of it is tested and Iris had no 26.3 branch at the time of writing.

- [ ] Sanity test with a heavy pack: flash bloom, scope distortion, crosshair, hurt vignette.
- [x] Flash bloom, scope, crosshair and hurt all work with Iris.
- [x] **Flash in front of the gun with Iris: not fixable by depth.** `mgs:debug_depth` shows the gun
      magenta (masked) without Iris, but with Iris it is plain world-grey: Iris draws the hand in
      its own pass, never runs `core/integrate_depth`, and leaves no trace of it in the depth a post
      effect can read. The spark draws over the gun under shaderpacks; everything else is unaffected.
- [ ] Look for banding from grading an already tonemapped image. If it is bad, soften the flash.
- [ ] Re-read Iris's `MixinPostChain`. It is an empty class today; if that changes, the whole
      compatibility story needs revisiting.
