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

def create_superuser():
    print("Creating superuser with username 'admin' and password 'admin'...")
    command = (
        'python manage.py shell -c "'
        'from django.contrib.auth import get_user_model; '
        'User = get_user_model(); '
        'User.objects.filter(username=\'admin\').exists() or '
        'User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin\')"'
    )
    run_command(command)

def setup_currencies():
    print("Ensuring 'USD' and 'EUR' currencies exist...")
    command = (
        'python manage.py shell -c "'
        'from exchange.models import Currency; '
        'Currency.objects.get_or_create(code=\'USD\', defaults={\'name\': \'US Dollar\', \'symbol\': \'$\'}); '
        'Currency.objects.get_or_create(code=\'EUR\', defaults={\'name\': \'Euro\', \'symbol\': \'€\'});"'
    )
    run_command(command)

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
    install_dependencies()
    apply_migrations()
    create_superuser()
    setup_currencies()
    load_historical_data()
    run_server()
