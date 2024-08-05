import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)

# Specify the path to your project and virtual environment
project_home = '/var/www/ai.com/instep-ai-ubuntu'
venv_home = os.path.join(project_home, 'venv', 'bin')

# Add the project directory to the sys.path
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the environment variables for your WSGI app
activate_this = os.path.join(venv_home, 'activate')
os.environ['VIRTUAL_ENV'] = venv_home
os.environ['PATH'] = venv_home + ':' + os.environ['PATH']

# Import your Flask app
from app import app as application  # Import your Flask app
