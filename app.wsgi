import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)

# Specify the path to your project and virtual environment
project_home = '/var/www/ai.com/instep-ai-ubuntu'
venv_home = os.path.join(project_home, 'venv', 'bin')

print(venv_home)

# Add the project directory to the sys.path
if project_home not in sys.path:
    sys.path.append(project_home)

# Activate the virtual environment
activate_this = os.path.join(venv_home, 'activate')

print(activate_this)
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import your Flask app
from app import app as application  # Import your Flask app
