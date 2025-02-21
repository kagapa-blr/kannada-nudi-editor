# setup_env.ps1
$venvPath = ".venv"

# Create virtual environment if it does not exist
if (!(Test-Path $venvPath)) {
    python -m venv $venvPath
}

# Activate virtual environment
$venvActivate = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    . $venvActivate
    Write-Output "Virtual environment activated."
} else {
    Write-Error "Failed to activate virtual environment."
    exit 1
}

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
