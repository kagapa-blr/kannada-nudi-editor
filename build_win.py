import os
import shutil
import subprocess
import zipfile
import time

def remove(path):
    """Attempt to remove a file or directory with retries in case of permission issues."""
    retries = 3
    for attempt in range(retries):
        if not os.path.exists(path):
            print(f"Path does not exist: {path}, skipping removal.")
            return
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                print(f"File {path} deleted")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Directory {path} deleted")
            return  # Exit function if successful
        except PermissionError:
            print(f"Permission denied: {path}. Retrying {attempt + 1}/{retries}...")
            time.sleep(2)
        except Exception as e:
            print(f"Error removing {path}: {e}")
            return  # Exit if it's another error
    print(f"Failed to delete {path} after {retries} retries.")

# Define application parameters
app_script = "app.py"
output_dir = "dist/kannadaNudi"
build_dir = "build"
spec_file = "app.spec"

# Get project root directory
project_dir = os.path.dirname(os.path.abspath(__file__))

# Clean old build files
remove(os.path.join(project_dir, output_dir))
remove(os.path.join(project_dir, build_dir))
remove(os.path.join(project_dir, spec_file))

# PyInstaller options
options = [
    "pyinstaller",
    "--onefile",
    "--name={}".format(os.path.splitext(app_script)[0]),
    "--noconsole",  # Hide console window
    os.path.join(project_dir, app_script),
    "--distpath={}".format(os.path.join(project_dir, output_dir)),
]

# Run PyInstaller
print("Running PyInstaller...")
subprocess.run(options, check=True)

# Copy additional directories if they exist
directories_to_copy = ["datasets", "resources"]
for directory in directories_to_copy:
    source_path = os.path.join(project_dir, directory)
    destination_path = os.path.join(project_dir, output_dir, directory)

    if os.path.exists(source_path):
        try:
            shutil.copytree(source_path, destination_path)
            print(f"Directory {directory} copied to {destination_path}")
        except Exception as e:
            print(f"Error copying directory {directory}: {e}")
    else:
        print(f"Skipping copy, directory not found: {directory}")

# Create a compressed zip file
archive_filename = os.path.join(project_dir, output_dir, "kannadaNudi.zip")
print(f"Creating zip archive: {archive_filename}")

with zipfile.ZipFile(archive_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for directory in directories_to_copy:
        source_path = os.path.join(project_dir, output_dir, directory)
        if os.path.exists(source_path):
            for root, _, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.join(project_dir, output_dir))
                    zipf.write(file_path, arcname=arcname)

    app_executable = os.path.join(output_dir, os.path.splitext(app_script)[0] + ".exe")
    if os.path.exists(app_executable):
        zipf.write(app_executable, arcname=os.path.basename(app_executable))
    else:
        print(f"Executable not found: {app_executable}")

print(f"Compressed archive created: {archive_filename}")
