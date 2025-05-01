# Session Management in Scaled Docker Environments Using Redis

This project demonstrates how to manage user sessions in a scalable Docker environment using **Flask**, **PostgreSQL**, **Redis**, and **NGINX**. It simulates a login-based blog or dashboard system where users must register and log in to access content.

The application uses two Flask containers (`frontend1` and `frontend2`) behind an NGINX load balancer. User sessions are maintained across both containers using Redis, ensuring a consistent user experience even if the server scales or the page is refreshed.

---

## Architecture Diagram

![Session-App-Architecture](https://github.com/sreehariskumar/Session-Management-in-Scaled-Docker-Environments-Using-Redis/blob/main/Session-App-Architecture%20Diagram.png)

- **NGINX** routes incoming traffic to either frontend container.
- **Flask containers** handle user registration, login, and dashboard rendering.
- **Redis** stores session data centrally, enabling consistent login state across both containers.
- **PostgreSQL** persists user credentials securely.

---

## 📦 Dependencies

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

The services used:

- **Flask** (Python Web Framework)
- **PostgreSQL** (Relational DB for user data)
- **Redis** (In-memory store for session data)
- **NGINX** (Load balancer and reverse proxy)

---

## 🚀 Getting Started

### 1. Clone the repository

```
git clone https://github.com/sreehariskumar/Session-Management-in-Scaled-Docker-Environments-Using-Redis.git
cd Session-Management-in-Scaled-Docker-Environments-Using-Redis
```

### 2. Run the application

```
docker-compose up -d
```

This will:

- Build the Flask app containers
- Start NGINX, Redis, PostgreSQL
- Serve the app at `http://localhost`

---

### 3. Check the application logs

```
docker-compose logs -f
```

## ✅ Test the App

1. Visit [http://localhost](http://localhost)
2. Register a new user
3. Login with your credentials
4. Refresh the page multiple times or open in new tabs — you’ll notice the *container hostname* changes but your session persists!
5. Click Logout to clear the session (also removed from Redis)

---

## 🧩 Folder Structure

```
.
├── app/
│   ├── app.py               # Flask app logic
│   ├── templates/           # HTML templates
│   └── requirements.txt     # Python dependencies
├── nginx/
│   └── nginx.conf           # Load balancer config
├── docker-compose.yml       # Service definitions
└── README.md                # This file
```

---

## Why PostgreSQL?

We use PostgreSQL for secure, reliable, and scalable data storage. It provides superior compliance, extensibility, and data integrity over MySQL—making it ideal for managing authentication in production-grade environments.

---

## Why Redis?

Flask stores session data in signed cookies by default. However, with many containers, you may want to centralize session logic - not rely solely on cookies or risk state mismatch.
Redis acts as a shared cache/database that all containers can access, ensuring session validity regardless of which container serves the request.

---

## 📝 License

This project is open-source and free to use under the MIT License.

---

## 🙌 Credits

Crafted with 💙 using Flask, Docker, Redis, and PostgreSQL.
