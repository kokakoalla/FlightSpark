# FlightSpark

FlightSpark is a web application for searching and booking flights, built using the kiwi.com API, Quart, Vite, and PostgreSQL. The application is deployed on AWS Lightsail using Nginx for the web server.

## Technologies

- **API:** [kiwi.com](https://partners.kiwi.com/) - used for fetching flight data.
- **Backend:** [Quart](https://pgjones.gitlab.io/quart/) - an asynchronous web framework based on Flask.
- **Frontend:** [Vite](https://vitejs.dev/) - a modern build tool for frontend applications.
- **Database:** [PostgreSQL](https://www.postgresql.org/) - a relational database management system.

## Installation and Setup

### Step 1: Clone the repository

```
git clone https://github.com/yourusername/flightspark.git
cd flightspark
```

### Step 2: Create and configure the .env file

Create a .env file in the root directory of the project and add the following environment variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/flightspark
API_KEY=your_kiwi_api_key
```

### Step 3: Install dependencies

Install the dependencies for both backend and frontend:

```
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

### Step 4: Setup the database

Install PostgreSQL and create the database and user:

```
# Install PostgreSQL on Ubuntu
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create the database and user
sudo -i -u postgres
psql
CREATE DATABASE flightspark;
CREATE USER yourusername WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE flightspark TO yourusername;
\q
exit
```

### Step 5: Deploy on AWS Lightsail

1. Create a Lightsail instance and connect to it:

```
ssh ubuntu@your_lightsail_instance_ip
```

2. Install and configure Nginx:

sudo apt update
sudo apt upgrade
sudo apt install nginx

3. Set up the Nginx configuration file for your application:

```
sudo nano /etc/nginx/sites-available/flightspark
```

example configuration file

```
server {
    listen 80;
    server_name your_domain_or_ip;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your_domain_or_ip;

    ssl_certificate /path/to your/fullchain.pem;
    ssl_certificate_key /path/to your//privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_fo
r;
        proxy_set_header X-Forwarded-Proto $scheme;
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTION
S';
        add_header Access-Control-Allow-Headers 'Origin, Content-T
ype, Accept';
    }

    location /static/ {
        alias /path/to/your/static/files;
    }
}
```

Enable the new configuration and restart Nginx:

```
sudo ln -s /etc/nginx/sites-available/flightspark /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Obtain a Free SSL Certificate

1. Install Certbot:

```
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

2. Obtain the SSL certificate:

```
sudo certbot --nginx -d your_domain_or_ip
```

### Step 7: Create a Systemd Service for Quart

Create a systemd service file for Quart:

```
sudo nano /etc/systemd/system/quart_app.service
```

example service file

```
[Unit]
Description=Quart Application
After=network.target

[Service]
User=yourusername
Group=yourusergroup
WorkingDirectory=/path/to your/FlightSpark

ExecStart=/path/to your/FlightSpark/server/myenv/bin/python3 /path/to your/FlightSpark/server/server.py

Restart=always

[Install]
WantedBy=multi-user.target

2. Reload systemd to apply the new service:

```

sudo systemctl daemon-reload

```

3. Start the Quart service:

```

sudo systemctl start quart_app

```

4. Enable the service to start on boot:

```

sudo systemctl enable quart_app

```

## Running the Application Manually

If you need to run the application manually, you can use the following commands:

Run the backend
```

python3 server.py

```

Run the frontend:

```

cd frontend
npm run dev

```

## Contribution

Contributions are welcome! Please create a pull request or open an issue to discuss.
```
