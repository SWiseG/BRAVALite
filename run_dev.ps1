Write-Host "Starting BRAVA Lite Setup..."

# Define virtual environment path and activation script
$venvPath = "brava_lite"
$venvActivate = ".\$venvPath\Scripts\Activate.ps1"

# Check if virtual environment exists
if (!(Test-Path $venvPath)) {
    Write-Host "Virtual environment '$venvPath' not found. Creating..."
    python -m venv $venvPath
    Start-Sleep -Seconds 3
}

# Activate virtual environment
Write-Host "Activating virtual environment: '$venvPath'"
& $venvActivate

# Install dependencies based on DEBUG mode
if ($env:DEBUG -eq "True") {
    Write-Host "Installing development dependencies..."
    pip install -r requirements.txt
    pip install -r dev-requirements.txt
} else {
    Write-Host "Installing production dependencies..."
    pip install -r requirements.txt
}

python.exe -m pip install --upgrade pip

# Setup database schema if needed
Write-Host "Running database schema setup..."
python manage.py setup_db

# Validate database structure
Write-Host "Running database structure validation..."
python manage.py db

# Generate migration files
Write-Host "Generating model migrations..."
python manage.py makemigrations

# (Optional) Run custom migrations
Write-Host "Applying custom database migrations..."
python manage.py migrate_custom

# Apply all migrations
Write-Host "Applying all database migrations..."
python manage.py migrate

# Load internationalization/translations
Write-Host "Loading translation files..."
python manage.py i18n

# Start the development server
Write-Host "Launching BRAVA Lite development server..."
python manage.py runserver
