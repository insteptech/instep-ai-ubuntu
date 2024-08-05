import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/ai.com/instep-ai-ubuntu")



from app import app as application  # Import your application
