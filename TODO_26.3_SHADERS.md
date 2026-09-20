# 26.3 shaders: what to verify in game

The migration is written. Reference material lives in [POSTEFFECT_26.3.md](POSTEFFECT_26.3.md);
this file is only the list of things that cannot be checked from a build.

Everything below is unverified against a running client.

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

- [ ] **The clock.** `/posteffect add @s mgs:debug_clock`. A green strip should appear at the bottom
      of the screen and sweep across once every 10 ticks. Red means the persistent target never
      reported an unarmed frame, which invalidates every timed effect. No strip at all means the
      chain failed to compile, so check the log and remember that a compile error blacklists the id
      until F3+T.
- [ ] **Re-arming.** Remove it, wait a second, add it again. The sweep must restart from the left.
      If it resumes where it left off, `closePersistentTargets` is not doing what the source says
      and the flash will not repeat correctly.
- [ ] **Muzzle flash.** Fire a slow weapon. The burst should be visibly shorter than before, about
      two frames. Then fire the fastest automatic weapon available: the flash must still blink
      rather than sit on permanently. It is gated to one per 3 ticks, and the id needs a full tick
      off between bursts.
- [ ] **Flash while someone else shoots.** Stand near a shooter. The bloom is screen centred, which
      is how it already behaved, but check that the spark sprite shows in the right place and that
      line of sight still gates it through walls.
- [ ] **Pack-a-Punch flash** picks the purple id.
- [ ] **Aim down sights** on a scoped weapon: the magnification and the lens distortion ramp in over
      about a third of a second, then hold. Release: they ramp back out over 0.2 s and the id comes
      off. Tapping sneak repeatedly inside that 0.2 s window snaps back to zero first, which is
      known and accepted.
- [ ] **Unscoped weapon** gets the centre pull with no barrel distortion.
- [ ] **Weapon switch while aiming** clears the overlay (`zoom/clear_state`).
- [ ] **Crosshair** appears when holding a gun, disappears while aiming, and its gap animates
      between standing, walking, sprinting and jumping rather than snapping.
- [ ] **Low health.** Take damage below 40% for the soft vignette, below 20% for the heartbeat and
      the rim colour separation. Heal back up and confirm both come off.
- [ ] **Leaving a game** while hurt takes the overlay off, and so does the round ending.
- [ ] **Relog** mid-round: ids are stored in player NBT, so they should come back intact and the
      mirror scores should still agree with them.
- [ ] **Death and respawn:** post effects are dropped server side on respawn, while the mirror
      scores survive. The crosshair re-asserts on the next spread change and the hurt tier on the
      next health change, so check nothing is stuck for longer than that.

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

Post effects compose with shaderpacks (see [POSTEFFECT_26.3.md](POSTEFFECT_26.3.md) section 7), but
none of it is tested and Iris had no 26.3 branch at the time of writing.

- [ ] Sanity test with a heavy pack: flash bloom, scope distortion, crosshair, hurt vignette.
- [ ] Check the depth read specifically. `mgs:post/flash` is the only shader that reads main depth,
      and the Iris and vanilla split is most fragile there.
- [ ] Look for banding from grading an already tonemapped image. If it is bad, soften the flash.
- [ ] Re-read Iris's `MixinPostChain`. It is an empty class today; if that changes, the whole
      compatibility story needs revisiting.
