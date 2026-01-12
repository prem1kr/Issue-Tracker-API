## 🎯 Goal

The goal of this project is to build a **backend service** using **Python** and **PostgreSQL** that allows users to manage **issues, comments, and labels**.
The system is designed to demonstrate **real-world backend engineering concepts** such as:

* Optimistic concurrency control
* Database transactions
* CSV-based bulk data import
* Aggregated reporting

---

## 🛠 Technology Stack

* **Python 3.10+**
* **FastAPI** (Web framework)
* **PostgreSQL** (Relational database)
* **SQLAlchemy** (ORM)
* **Pydantic** (Validation)
* **Uvicorn** (ASGI server)

---

## 📁 Project Structure

```
API/
│
├── venv/
│
├── app/
│   ├── main.py          # Application entry point
│   ├── db.py            # Database configuration
│   ├── models.py        # Database models
│   ├── schemas.py       # Request/response schemas
│   │
│   ├── routes/
│   │   ├── issues.py    # Issue CRUD & concurrency
│   │   ├── comments.py  # Comments management
│   │   ├── labels.py    # Label assignment
│   │   └── reports.py   # Reporting endpoints
│   │
│   └── utils/
│       └── csv_import.py # CSV import logic
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ PostgreSQL Configuration

Create the database:

```sql
CREATE DATABASE issue_tracker;
```

Create `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/issue_tracker
```

---

### 4️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧩 Core Features Implementation

### 1️⃣ Issue Management

* Full CRUD operations on issues
* Issues include version field for **optimistic concurrency control**
* Version mismatch returns **409 Conflict**

### 2️⃣ Comments

* Comments can be added to issues
* Validation:

  * Comment body must be non-empty
  * Author must exist (foreign key constraint)

### 3️⃣ Labels

* Labels are unique across the system
* Issues can have multiple labels
* Label replacement is **atomic**

### 4️⃣ Bulk Update (Transactional)

* Bulk issue status update endpoint
* Uses database transactions
* If any issue violates business rules, **entire operation is rolled back**



## 🗄 Database Design

### Tables

* `users`
* `issues`
* `comments`
* `labels`
* `issue_labels` (many-to-many)

### Constraints & Indexes

* Foreign key constraints for referential integrity
* Unique constraint on label names
* Indexed issue status for performance

---

## 🌐 API Endpoints

| Endpoint                 | Method | Description                        |
| ------------------------ | ------ | ---------------------------------- |
| `/issues`                | POST   | Create new issue                   |
| `/issues`                | GET    | List issues (filter + pagination)  |
| `/issues/{id}`           | GET    | Get issue with comments & labels   |
| `/issues/{id}`           | PATCH  | Update issue (version check)       |
| `/issues/{id}/comments`  | POST   | Add comment                        |
| `/issues/{id}/labels`    | PUT    | Replace labels atomically          |
| `/issues/bulk-status`    | POST   | Bulk status update (transactional) |
| `/issues/import`         | POST   | CSV upload for issue import        |
| `/reports/top-assignees` | GET    | Aggregated report                  |
| `/reports/latency`       | GET    | Average resolution time            |

---

## 🔐 Concurrency & Transactions

* **Optimistic locking** prevents lost updates
* **Database transactions** ensure atomic operations
* Automatic rollback on failure conditions


