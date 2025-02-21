# setup_env.ps1
$venvPath = ".venv"

# Remove existing virtual environment if it is corrupted
if (Test-Path $venvPath) {
    Remove-Item -Recurse -Force $venvPath
}

# Create virtual environment
python -m venv $venvPath

# Activate virtual environment
$venvActivate = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    . $venvActivate
    Write-Output "Virtual environment activated."
} else {
    Write-Error "Failed to activate virtual environment."
    exit 1
}

# Upgrade pip safely
python -m ensurepip --default-pip
python -m pip install --upgrade --user pip

# Install dependencies
pip install -r requirements.txt
