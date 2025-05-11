
# Imports
from python_datapack.utils.database_helper import *


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]
    database: dict = config["database"]
    pass

