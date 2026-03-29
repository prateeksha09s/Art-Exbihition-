# Art-Exbihition-
Art Exhibition Management System   HTML · CSS · JavaScript · MySQL • Developed a web application with secure user authentication and a well-structured relational database  schema for efficient exhibition data management.

# 🎨 Art Exhibition Management System

![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)

A web application for managing art exhibitions — allowing artists, curators, and visitors to interact with exhibitions, artworks, and events through a secure and well-structured platform.

---

## 📖 Project Overview

The Art Exhibition Management System is a web-based application built with JavaScript, HTML, CSS, and MySQL. It provides a structured platform for managing artists, artworks, exhibitions, and visitor registrations. The system features secure user authentication and an optimized relational database schema to ensure data integrity and performance.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Database | MySQL |
| Authentication | Session-based secure login |
| Architecture | Client-Server, MVC |

---

## ✨ Features

- 🔐 **Secure Authentication** – User login and registration with session management
- 🖼️ **Artwork Management** – Add, view, update, and remove artworks
- 🏛️ **Exhibition Management** – Create and manage exhibitions with dates and venues
- 👨‍🎨 **Artist Profiles** – Maintain artist information linked to their artworks
- 🎟️ **Visitor Registration** – Allow visitors to register for exhibitions
- 🗄️ **Optimized Database** – Relational schema with well-defined foreign keys and indexes
- 🎨 **Clean UI** – Simple, intuitive design for a smooth user experience

---

## 🖼️ Screenshots

> _Screenshots coming soon — stay tuned!_

<!-- Add your screenshots here -->
<!-- ![Home](screenshots/home.png) -->
<!-- ![Exhibition Page](screenshots/exhibition.png) -->
<!-- ![Artwork Gallery](screenshots/gallery.png) -->

---

## ⚙️ Setup & Installation

### Prerequisites

- Any modern web browser (Chrome, Firefox, Edge)
- MySQL 8+
- A local server (XAMPP / WAMP / LAMP recommended)

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/prateeksha09s/art-exhibition-management.git
cd art-exhibition-management
```

### Database Setup

```sql
-- Create the database
CREATE DATABASE art_exhibition_db;
USE art_exhibition_db;

-- Import the schema
SOURCE database/schema.sql;

-- (Optional) Import sample data
SOURCE database/seed.sql;
```

### Running the Application

1. Copy the project folder to your local server's root directory:
   - XAMPP → `htdocs/`
   - WAMP → `www/`

2. Update database credentials in `config/db.php` (or equivalent config file):
```javascript
const DB_HOST = 'localhost';
const DB_USER = 'your_username';
const DB_PASS = 'your_password';
const DB_NAME = 'art_exhibition_db';
```

3. Open your browser and go to:
```
http://localhost/art-exhibition-management
```

---

## 🗂️ Database Schema (Overview)

| Table | Description |
|-------|-------------|
| `users` | Stores user credentials and roles |
| `artists` | Artist profile information |
| `artworks` | Artwork details linked to artists |
| `exhibitions` | Exhibition events with dates and venues |
| `registrations` | Visitor registrations for exhibitions |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add: your feature description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow clean code practices and include comments where necessary.

---

## 👩‍💻 Author

**Prateeksha S**  
Associate Software Engineer | Full Stack Developer  
[GitHub](https://github.com/prateeksha09s) • [LinkedIn](https://linkedin.com)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
