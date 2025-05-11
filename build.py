
# Install required package
import os
import sys

try:
	from python_datapack import build_process
except ImportError:
	print("python_datapack package not found, installing it...")
	os.system(f"{sys.executable} -m pip install python_datapack")
	print("\npython_datapack package has been installed.\nPlease restart the build script!\n")
	sys.exit(-1)

# Setup config
from config import configuration

# Import my code
from user.link import main as link_main  # Called near the end of the build process
from user.setup_database import main as setup_database_main

# Run build process
if __name__ == "__main__":
	build_process(configuration, setup_database_main, user_code=link_main)

