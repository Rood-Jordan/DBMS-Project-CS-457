import os
import shutil

# remove directories created after testing
if os.path.exists(os.path.join(os.getcwd(), "SetupDB")):
    shutil.rmtree(os.path.join(os.getcwd(), "SetupDB"))

if os.path.exists(os.path.join(os.getcwd(), "TestDB")):
    shutil.rmtree(os.path.join(os.getcwd(), "TestDB"))
