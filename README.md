# 🔐ManagerPasswords

Storing passwords in a safe place (API)

![PyPI pyversions](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/github/license/eli64s/readme-ai?color=blueviolet)

---

## 🔗 Quick Links
* [Overview](#-overview)
* [Getting Started](#-getting-started)
* [License](#-license)

---

## 🔭 Overview
***Stack***

FastApi, PostgreSQL, Sentry, Docker

***Users***

Each user must register to use the system. After that, an <em>AES-key</em>
will be generated for him, which will encrypt all his passwords.
The user can regenerate the AES-key at any time.

***Passwords***

All passwords are stored encrypted in the database.
The user has access to each of his passwords.
It can also search for a part of the service name.
> [!NOTE]
>
>This system does not guarantee 100% security of your data,
> so you should change the password from the account system and generate a new
> AES key at least once every 6 months.
>
---
## 👩‍💻 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

- *Python version 3.11 or higher*
- *Package manager (i.e. pip, conda, poetry) or Docker*


***ManagerPasswords API***

An  .env file is needed to use *Manager Passwords API*
The steps below outline this process to create it:

<details closed><summary>🔐 ManagerPasswords API - .env file</summary>
You need to create variables to connect to the database in the .env file

For example:

- *POSTGRES_USER: postgres_user*
- *POSTGRES_PASSWORD: postgres_password*
- *POSTGRES_DB: postgres_db*
- *POSTGRES_PORT: 5432*

You should also connect this project to [Sentry](https://sentry.io/) and add SENTRY_URL to the .env file

For example:
- *SENTRY_URL: https://eec20034949b2b27dc10652f4cef5d46@o4506314416521216.ingest.sentry.io/454243420649984*
</details>

---
### 🚀 Running *ManagerPasswords*

Using `docker`

```bash
docker compose -f docker-compose-dev.yaml up -d
```

### 📝 Documentation

API documentation will be available after running
[Documentation](http://localhost:8000/docs) at http://localhost:8000/docs

---

### 🧪 Tests

Execute the test suite using the command below.

```bash
 docker-compose -f docker-compose-test.yaml run --rm backend_test sh -c 'pytest'
```

---

## 📄 License

[MIT](https://github.com/eli64s/readme-ai/blob/main/LICENSE)

---
