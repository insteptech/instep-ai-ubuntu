import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/ai.com/instep-ai-ubuntu")

activate_this = '/var/www/ai.com/instep-ai-ubuntu/venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


from app import app as application  # Import your application
