import os
import shutil
import subprocess
import zipfile

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
output_dir = "dist/kannadaNudi"

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
    "--noconsole",
    os.path.join(project_dir, app_script),
    "--distpath={}".format(os.path.join(project_dir, output_dir))
]

# Run PyInstaller
subprocess.run(options)

# Copy additional directories to output_dir
directories_to_copy = ['datasets', 'resources']
for directory in directories_to_copy:
    source_path = os.path.join(project_dir, directory)
    destination_path = os.path.join(project_dir, output_dir, directory)

    try:
        shutil.copytree(source_path, destination_path)
        print("Directory {} copied to {}".format(directory, destination_path))
    except Exception as e:
        print("Error copying directory {}: {}".format(directory, str(e)))

# Create a compressed zip file
archive_filename = os.path.join(project_dir, output_dir, 'kannadaNudi.zip')

with zipfile.ZipFile(archive_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for directory in directories_to_copy:
        source_path = os.path.join(project_dir, output_dir, directory)
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.join(project_dir, output_dir))
                zipf.write(file_path, arcname=arcname)

    app_executable = os.path.join(output_dir, os.path.splitext(app_script)[0])
    zipf.write(app_executable, arcname=os.path.basename(app_executable))

print("Compressed archive created: {}".format(archive_filename))
