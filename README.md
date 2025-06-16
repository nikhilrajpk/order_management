# 🧾 Order Management System

A **Django-based web application** for managing orders, integrated with **Celery** for asynchronous email processing, **PostgreSQL** for data storage, and **Gemini AI** for enhanced order processing. Deployed on **AWS EC2** with **Nginx** and **SSL**, the system allows users to place orders, sends confirmation emails to a warehouse, and updates order statuses based on email replies.

---

## 🚀 Features

- **Order Placement**: Users can submit orders with details like customer name, product, quantity, and cost.  
- **Email Notifications**: Sends HTML emails to the warehouse `warehouseemail2025@gmail.com` with order details and a confirmation link (e.g., `https://order.nikhilrajpk.in/confirm/<order_id>/`).  
- **Asynchronous Processing**: Celery with Redis processes warehouse email replies every 5 minutes to update order statuses to `"Confirmed"`.  
- **Gemini AI Integration**: Utilizes Gemini AI API for intelligent order data analysis and processing (configured via `GEMINI_API_KEY`).  
- **Secure Deployment**: Hosted on AWS EC2 with Nginx, Gunicorn, and Let’s Encrypt SSL for HTTPS.  
- **Admin Interface**: Django admin panel for managing orders at `https://order.nikhilrajpk.in/admin/`.

---

## 🛠 Tech Stack

| Category     | Technology               |
|--------------|---------------------------|
| Backend      | Django 5.0, Python 3.12    |
| Task Queue   | Celery 5.5.3, Redis 7      |
| Database     | PostgreSQL 14             |
| AI           | Gemini AI API             |
| Web Server   | Nginx, Gunicorn           |
| Deployment   | AWS EC2 (Ubuntu 24.04), Docker Compose |
| SSL          | Let’s Encrypt (Certbot)   |
| Email        | Gmail SMTP                |
| Environment  | Docker                    |

---

## 📋 Prerequisites

- Python 3.12  
- Docker & Docker Compose  
- AWS account (for deployment)  
- Gmail account for SMTP (with App Password)  
- Gemini AI API key  
- Domain name (e.g., `order.nikhilrajpk.in`)  
- Git  

---

## 💻 Local Setup

### 1. Clone the Repository

git clone https://github.com/nikhilrajpk/order_management.git
cd order_management
2. Create .env File
Create a .env file in the root directory with the following:

env

SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=order_db
DB_USER=order_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
GEMINI_API_KEY=your_gemini_api_key
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
3. Build and Start Containers

docker-compose up --build -d
4. Apply Migrations

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
5. Set Up Periodic Task

docker-compose exec web python manage.py setup_periodic_task
6. Create Superuser

docker-compose exec web python manage.py createsuperuser
7. Collect Static Files

docker-compose exec web python manage.py collectstatic --noinput
8. Run Application

docker-compose exec web python manage.py runserver 0.0.0.0:8000
Access the app at: http://localhost:8000/

☁️ Deployment on AWS EC2
1. Launch EC2 Instance
Ubuntu 24.04 LTS

t2.micro (or larger)

Open ports 80 (HTTP) and 443 (HTTPS)

2. Set Up EC2

sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
3. Clone and Configure

git clone https://github.com/nikhilrajpk/order_management.git
cd order_management
Update .env with production values (e.g., DEBUG=False, DB_HOST=db).

4. Start Containers

docker-compose up --build -d
5. Migrations & Static Files

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py setup_periodic_task
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
6. Install & Configure Nginx

sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
Nginx Config
Create: /etc/nginx/sites-available/order_management

nginx

server {
    listen 80;
    server_name <your_ec2_ip> order.nikhilrajpk.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name <your_ec2_ip> order.nikhilrajpk.in;

    ssl_certificate /etc/letsencrypt/live/order.nikhilrajpk.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/order.nikhilrajpk.in/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ubuntu/order_management/staticfiles/;
    }

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
Enable config:


sudo ln -s /etc/nginx/sites-available/order_management /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
7. Set Up SSL (Certbot)

sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d order.nikhilrajpk.in
⚙️ Django Production Settings
Edit order_management/settings.py:

python

ALLOWED_HOSTS = ['<your_ec2_ip>', 'order.nikhilrajpk.in', 'localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
Restart:


docker-compose restart web
📦 Usage
1. Place an Order
Visit https://order.nikhilrajpk.in/ and fill out the form.

2. Confirm Order
Open the email and click the confirmation link.

Or reply:
Order confirmed with order ID <id>

3. Check Status
Visit https://order.nikhilrajpk.in/status/<order_id>/

4. Admin Access
Login: https://order.nikhilrajpk.in/admin/

🧰 Troubleshooting
Celery Not Running?

docker-compose logs celery
docker-compose logs celery_beat
docker-compose restart celery celery_beat
Nginx Issues?

sudo tail -f /var/log/nginx/error.log
Database Issues?

docker-compose exec web python manage.py migrate
Low Memory?

free -m
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
🤝 Contributing
Fork the repository.

Create your feature branch: git checkout -b feature/my-feature

Commit your changes: git commit -m 'Add feature'

Push: git push origin feature/my-feature

Open a Pull Request

📄 License
This project is licensed under the MIT License.

📬 Contact
For issues or questions, contact nikhilrajpk or open an issue in the repository.
