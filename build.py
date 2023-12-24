import shutil
import subprocess
import os
import tarfile


def remove(path):
    try:
        if os.path.isfile(path) or os.path.islink(path):
            print("File {} deleted".format(path))
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print("Directory {} deleted".format(path))
        else:
            raise ValueError("File {} is not a file or directory.".format(path))
    except Exception as e:
        print("Permission denied! Please close other applications.")


# Define your application script and other parameters
app_script = "app.py"
output_dir = "dist/spellcheckApp"

# Get the path to the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
remove(os.path.join(project_dir, output_dir))
remove(os.path.join(project_dir, "build"))
remove(os.path.join(project_dir, "app.spec"))

# Create a list of options for PyInstaller
options = [
    "pyinstaller",
    "--onefile",
    "--name={}".format(os.path.splitext(app_script)[0]),
    # "--debug=all",  # Set debug to "all" for detailed information
]

# Add the application script
options.append(os.path.join(project_dir, app_script))
# Set the output directory
options.append("--distpath={}".format(os.path.join(project_dir, output_dir)))
# Run PyInstaller
subprocess.run(options)
# Copy additional directories to output_dir
directories_to_copy = ['datasets', 'images', 'static']
for directory in directories_to_copy:
    source_path = os.path.join(project_dir, directory)
    destination_path = os.path.join(project_dir, output_dir, directory)

    try:
        shutil.copytree(source_path, destination_path)
        print("Directory {} copied to {}".format(directory, destination_path))
    except Exception as e:
        print("Error copying directory {}: {}".format(directory, str(e)))



# Create a compressed tar (gzipped) file
archive_filename = os.path.join(project_dir, output_dir, 'spellcheckApp.tar.gz')

with tarfile.open(archive_filename, 'w:gz') as tar:
    for directory in directories_to_copy:
        tar.add(os.path.join(output_dir, directory), arcname=directory)
    tar.add(os.path.join(output_dir, os.path.splitext(app_script)[0] + '.exe'), arcname=os.path.splitext(app_script)[0] + '.exe')

print("Compressed archive created: {}".format(archive_filename))