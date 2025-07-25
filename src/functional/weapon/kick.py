
# Imports
from stewbeet import Mem, write_versioned_function

from ...config.stats import KICK


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Handle pending clicks
    write_versioned_function("player/right_click",
f"""
# Simulate weapon kick
function {ns}:v{version}/kicks/main
""")

    ## Kicks
    write_versioned_function("kicks/main",
f"""
# Extract kick type & pick random value between 1 and 5
scoreboard players set #kick {ns}.data 0
execute store result score #kick {ns}.data run data get storage {ns}:gun all.stats.{KICK}
execute store result score #random {ns}.data run random value 1..5

# Check if player is riding a vehicle - if so, use /rotate instead of /tp to avoid dismounting
scoreboard players set #has_vehicle {ns}.data 0
execute on vehicle run scoreboard players set #has_vehicle {ns}.data 1

# Switch case
execute if score #kick {ns}.data matches ..0 run function {ns}:v{version}/kicks/type_0
execute if score #kick {ns}.data matches 1 run function {ns}:v{version}/kicks/type_1
execute if score #kick {ns}.data matches 2 run function {ns}:v{version}/kicks/type_2
execute if score #kick {ns}.data matches 3 run function {ns}:v{version}/kicks/type_3
execute if score #kick {ns}.data matches 4 run function {ns}:v{version}/kicks/type_4
execute if score #kick {ns}.data matches 5.. run function {ns}:v{version}/kicks/type_5
""")
    all_kicks: list[list[tuple[float, float]]] = [
        [(-0.05, -0.25), (-0.025, -0.25), (-0.0, -0.25), (0.025, -0.25), (0.05, -0.25)],
        [(-0.08, -0.5), (-0.03, -0.5), (-0.0, -0.5), (0.03, -0.5), (0.08, -0.5)],
        [(-0.11, -1.0), (-0.05, -1.0), (-0.0, -1.0), (0.05, -1.0), (0.11, -1.0)],
        [(-0.13, -1.5), (-0.06, -1.5), (-0.0, -1.5), (0.06, -1.5), (0.13, -1.5)],
        [(-0.15, -2.0), (-0.06, -2.0), (-0.0, -2.0), (0.06, -2.0), (0.15, -2.0)],
        [(-0.17, -2.5), (-0.06, -2.5), (-0.0, -2.5), (0.06, -2.5), (0.17, -2.5)],
    ]
    for i, kicks in enumerate(all_kicks):
        content: str = ""
        for score, command in [(0, "tp @s ~ ~ ~"), (1, "rotate @s")]:
            for j, (yaw, pitch) in enumerate(kicks):
                content += f"\nexecute if score #has_vehicle {ns}.data matches {score} if score #random {ns}.data matches {j+1} run {command} ~{yaw} ~{pitch}"
        write_versioned_function(f"kicks/type_{i}", content)

