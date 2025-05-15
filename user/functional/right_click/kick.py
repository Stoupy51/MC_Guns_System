
# Imports
from python_datapack.utils.database_helper import write_versioned_function

from user.config.stats import KICK


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Simulate weapon kick
function {ns}:v{version}/kicks/main
""")

    ## Kicks
    write_versioned_function(config, "kicks/main",
f"""
# Extract kick type & pick random value between 1 and 5
scoreboard players set #kick {ns}.data 0
execute store result score #kick {ns}.data run data get storage {ns}:gun stats.{KICK}
execute store result score #random {ns}.data run random value 1..5

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
        for j, (yaw, pitch) in enumerate(kicks):
            content += f"\nexecute if score #random {ns}.data matches {j+1} run tp @s ~ ~ ~ ~{yaw} ~{pitch}"
        write_versioned_function(config, f"kicks/type_{i}", content)

