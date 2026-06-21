
# TODO:
- idea for better zombie AI: use a different entity (for instance warden)
- Optimisation: Avoid repeating @x selectors when they can be grouped. Entity selectors are very very slow.
- quick action menu: move all of what appears in /trigger set 1 chat menu, and when trigger is set to 1 open the quick action menu instead of the chat menu
- replace self.func with proper write_versioned_function and raw_function with write_function because seriously, they are much more readable and fitting.
- zombies/revive/downed_tick is not using a predicate for matching same id entity (see the how the turret trap does it) for optimization.

