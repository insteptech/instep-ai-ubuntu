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

# Restart on failure

Restart=always
RestartSec=3

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

Reload the Systemd Daemon
Whenever you create or modify a systemd service file, you need to reload the systemd daemon to apply the changes:

sudo systemctl daemon-reload

Step 3: Restart the Gunicorn Service
Restart the Gunicorn service to apply any changes or to simply restart the application:

sudo systemctl restart my_flask_app

Step 4: Enable the Service (if not already enabled)
Ensure that your service starts on boot:

sudo systemctl enable my_flask_app

Step 5: Check the Status of the Service
You can check the status of your Gunicorn service to ensure it is running correctly:

sudo systemctl status my_flask_app
Example Output
You should see output similar to this:

● my_flask_app.service - Gunicorn instance to serve my Flask app
Loaded: loaded (/etc/systemd/system/my_flask_app.service; enabled; vendor preset: enabled)
Active: active (running) since Mon 2024-08-05 10:00:00 UTC; 10s ago
Main PID: 1234 (gunicorn)
Tasks: 3 (limit: 1152)
Memory: 50.0M
CGroup: /system.slice/my_flask_app.service
├─1234 /var/www/ai.com/instep-ai-ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/var/www/ai.com/instep-ai-ubuntu/my_flask_app.sock -m 007 app:app
├─1235 /var/www/ai.com/instep-ai-ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/var/www/ai.com/instep-ai-ubuntu/my_flask_app.sock -m 007 app:app
└─1236 /var/www/ai.com/instep-ai-ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/var/www/ai.com/instep-ai-ubuntu/my_flask_app.sock -m 007 app:app
Troubleshooting
If you encounter any issues, check the logs for more information:

sudo journalctl -u my_flask_app

Using nohup and &
If you want to run Gunicorn in the background and keep it running even after logging out, you can use nohup with &:

Run Gunicorn with nohup:

nohup /var/www/ai.com/instep-ai-ubuntu/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app &

Check nohup.out for Logs:

By default, nohup will write output to nohup.out in the current directory. You can specify a different log file if needed.

nohup /var/www/ai.com/instep-ai-ubuntu/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app > /var/log/my_flask_app.log 2>&1 &

For Gunicorn Logs
If you're using systemd to manage Gunicorn, you can check the logs in real-time using journalctl:

Real-Time Logs with journalctl:

sudo journalctl -u my_flask_app -f
The -f option will follow the log file and show new entries as they are written.

Step 1: Find the Gunicorn Process ID (PID)
You can use the ps command to find the PID of the Gunicorn process. Gunicorn processes typically show up with the command gunicorn.

ps aux | grep gunicorn

If the process does not stop, you can use the -9 option to force kill it:

kill <PID>
kill -9 1234
