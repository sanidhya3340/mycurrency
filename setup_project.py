import os
import subprocess
import sys

def run_command(command):
    """
    Helper function to run shell commands and handle errors.
    """
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def install_dependencies():
    print("Installing dependencies...")
    run_command("pip install -r requirements.txt")

def apply_migrations():
    print("Applying migrations...")
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

def load_historical_data():
    print("Loading historical data...")
    # Run a Django shell command to load historical data
    command = (
        'python manage.py shell -c "'
        'from exchange.tasks import load_historical_data; '
        'load_historical_data(\'USD\', \'EUR\', \'2023-10-01\', \'2023-10-10\')"'
    )
    run_command(command)

def run_server():
    print("Starting the development server...")
    run_command("python manage.py runserver")

if __name__ == "__main__":
    print("Setting up the MyCurrency Django project...")
    
    # Step 1: Install dependencies
    install_dependencies()

    # Step 2: Apply database migrations
    apply_migrations()

    # Step 3: Load historical data (synchronously)
    load_historical_data()

    # Step 4: Start the Django development server
    run_server()
