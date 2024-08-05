1. Set Up Your Flask Application
   First, create a simple Flask app. For example, create a file named app.py:

from flask import Flask

app = Flask(**name**)

@app.route('/')
def home():
return "Welcome to My Fun Flask App!"

if **name** == '**main**':
app.run(debug=True)

2. Create a Virtual Environment
   Set up a virtual environment for your project:

cd /var/www/ai.com/instep-ai-ubuntu
python3 -m venv venv
source venv/bin/activate

3. Install Flask and Gunicorn
   Install Flask and Gunicorn within your virtual environment:

pip install Flask gunicorn

4. Run Your Flask App with Gunicorn
   Test your Flask app using Gunicorn:

gunicorn app:app --bind 127.0.0.1:8000

5. Install Apache and mod_proxy
   If you haven't installed Apache yet, do so:

sudo apt update
sudo apt install apache2

Enable the necessary modules:

sudo a2enmod proxy
sudo a2enmod proxy_http

6. Configure Apache
   Create a new configuration file for your Flask app, e.g., /etc/apache2/sites-available/my_flask_app.conf:

<VirtualHost \*:80>
ServerName yourdomain.com

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    ErrorLog ${APACHE_LOG_DIR}/flask_app_error.log
    CustomLog ${APACHE_LOG_DIR}/flask_app_access.log combined

</VirtualHost>

Make sure to replace yourdomain.com with your actual domain name.

7. Enable Your Site and Restart Apache
   Enable the new site configuration:

sudo a2ensite my_flask_app.conf
Restart Apache to apply the changes:

sudo systemctl restart apache2

8. Create a Service File for Gunicorn
   Create a systemd service file for Gunicorn at /etc/systemd/system/my_flask_app.service:

[Unit]
Description=Gunicorn instance to serve my Flask app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai.com/instep-ai-ubuntu
Environment="PATH=/var/www/ai.com/instep-ai-ubuntu/venv/bin"
ExecStart=/var/www/ai.com/instep-ai-ubuntu/venv/bin/gunicorn --workers 3 --bind unix:my_flask_app.sock -m 007 app:app

[Install]
WantedBy=multi-user.target

9. Start and Enable the Gunicorn Service
   Start and enable the Gunicorn service:

sudo systemctl start my_flask_app
sudo systemctl enable my_flask_app

10. Check Everything
    Finally, check your Apache and Gunicorn logs to ensure everything is running smoothly:

sudo journalctl -u my_flask_app
sudo tail -f /var/log/apache2/flask_app_error.log
