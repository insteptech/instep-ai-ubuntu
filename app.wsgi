import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/myapp")

from myapp import app as application  # Import your application