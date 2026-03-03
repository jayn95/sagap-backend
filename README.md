# 📦 SAGAP Inventory Backend

Backend Inventory Management System built with:

* **FastAPI**
* **SQLAlchemy ORM**
* **PostgreSQL**
* Layered Architecture (API → Services → DB → Schemas)

---

## 🚀 System Overview

SAGAP Inventory Backend is a scalable asset management system designed to track:

* 👤 Agents (Employees)
* 💻 Assets (Devices & Peripherals)
* 📜 Asset Assignments (Ownership & History)

The system supports:

* ✅ Asset lifecycle tracking
* ✅ Ownership history preservation
* ✅ Current ownership queries
* ✅ Data integrity protections
* ✅ Soft delete strategy
* ✅ Enterprise-style service layer
* ✅ Asset search & filtering
* ✅ Update endpoints for agents & assets
* ✅ Future scalability for asset sets

This system goes far beyond basic CRUD operations — it provides ownership intelligence and historical tracking.

---

# 🏗 Architecture

The project follows a **Layered Architecture**:

```
API Layer (Routes)
        ↓
Service Layer (Business Logic)
        ↓
Database Layer (SQLAlchemy Models)
        ↓
PostgreSQL Database
```

This ensures:

* Separation of concerns
* Maintainability
* Scalability
* Clean business logic

---

# 🗄 Database Structure

---

## 👤 Agents Table

Represents employees who receive assets.

### Fields

* `agent_id` (Primary Key)
* `employee_no` (Unique)
* `full_name`
* `designation`
* `department`
* `contact_number`
* `email`
* `current_address`
* `status`
* `created_at`
* `assignments` (relationship)

### Relationship

```
One Agent → Many Assignments
```

An employee can own multiple assets over time or simultaneously.

---

## 💻 Assets Table

Represents physical inventory items.

### Fields

* `asset_id` (Primary Key)
* `asset_type`
* `asset_tag` (Unique)
* `brand`
* `model`
* `serial_number`
* `serial_number_2`
* `memory`
* `condition`
* `status`
* `created_at`
* `assignments` (relationship)

### Relationship

```
One Asset → Many Assignments
```

An asset can be assigned to multiple agents throughout its lifecycle.

### 🔑 Important Design Concept

The **asset table stores static device information**.

Ownership is NOT stored in the asset table.

Ownership is stored in the **Assignment table**.

So ownership changes:

* ❌ Do NOT modify asset records
* ✅ Create new assignment records

This preserves full ownership history.

---

## 📜 AssetAssignment Table (Core Logic)

This is the most important table in the system.

### Fields

* `assignment_id` (Primary Key)
* `asset_id` (Foreign Key → assets)
* `agent_id` (Foreign Key → agents)
* `assigned_at`
* `returned_at`
* `remarks`
* `is_deleted`
* `asset` (relationship)
* `agent` (relationship)

### Purpose

This table functions as an:

> 📜 Ownership History Ledger

### Key Rules

* `returned_at = NULL` → Asset is currently assigned
* `returned_at != NULL` → Historical record
* `is_deleted = TRUE` → Soft-deleted mistake entry

### Relationship

```
Agent ⇄ Assignment ⇄ Asset
```

This creates a **many-to-many relationship with history tracking**.

---

# 🔧 Modules & Endpoints

---

# 📦 ASSIGNMENT MODULE

## Service Functions

### `assign_asset()`

Validations:

* Asset exists
* Agent exists
* Asset is available
* Agent is active
* No active assignment exists

Updates asset status → **Assigned**

---

### `return_asset()`

* Sets `returned_at`
* Restores asset status → **Available**

---

### `update_assignment()`

Allows:

* Agent reassignment
* Remarks update

---

### `delete_assignment()`

Soft delete with integrity rules:

* Prevents deleting historical records improperly
* Prevents deleting active ownership incorrectly
* Restores asset status if needed

---

### Query Functions

* `get_all_assignments()`
* `get_asset_history(asset_id)`
* `get_current_owner(asset_id)`
* `get_agent_current_assets(agent_id)`
* `get_all_current_asset_owners()`

---

## Assignment Endpoints

| Method | Endpoint                   | Description            |
| ------ | -------------------------- | ---------------------- |
| POST   | `/assignments/`            | Assign asset           |
| POST   | `/assignments/return/{id}` | Return asset           |
| GET    | `/assignments/`            | Read all assignments   |
| PUT    | `/assignments/{id}`        | Update assignment      |
| DELETE | `/assignments/{id}`        | Soft delete assignment |

---

# 💻 ASSET MODULE

## Service Functions

* `create_asset`
* `get_all_assets`
* `get_asset_by_id`
* `delete_asset`

Ownership-related queries handled via assignment service:

* `get_asset_history`
* `get_current_owner`
* `get_all_current_asset_owners`

---

## Asset Endpoints

| Method | Endpoint                           | Description        |
| ------ | ---------------------------------- | ------------------ |
| POST   | `/assets/`                         | Create asset       |
| GET    | `/assets/`                         | Get all assets     |
| GET    | `/assets/current-owners`           | Assets with owners |
| GET    | `/assets/{asset_id}`               | Get asset          |
| DELETE | `/assets/{asset_id}`               | Delete asset       |
| GET    | `/assets/{asset_id}/history`       | Asset history      |
| GET    | `/assets/{asset_id}/current-owner` | Current owner      |

---

# 👤 AGENT MODULE

## Service Functions

* `create_agent`
* `get_all_agents`
* `get_agent_by_id`
* `delete_agent`

Ownership query:

* `get_agent_current_assets`

---

## Agent Endpoints

| Method | Endpoint                    | Description           |
| ------ | --------------------------- | --------------------- |
| POST   | `/agents/`                  | Create agent          |
| GET    | `/agents/`                  | Get all agents        |
| GET    | `/agents/{agent_id}`        | Get agent             |
| DELETE | `/agents/{agent_id}`        | Delete agent          |
| GET    | `/agents/{agent_id}/assets` | Assets owned by agent |

---

# 🔍 Advanced Features

### ✅ Asset Lifecycle Tracking

Every assignment is recorded with timestamps.

### ✅ Ownership Intelligence

Query:

* Who owns this asset?
* What assets does this agent own?
* Full asset history

### ✅ Soft Delete Strategy

Prevents data loss while preserving history integrity.

### ✅ Data Integrity Protections

* Prevent duplicate active assignments
* Prevent improper deletion
* Maintain accurate asset status

---

# 🛣 Future Feature — Asset Set Ownership

Planned feature:

Example:

```
Desktop Set:
PC + Monitor + Keyboard + Mouse → Agent
```

Will likely require:

* `asset_set` table
* `set_assignment` table

---

# What was implemented:

* ✅ Relational database with ownership history
* ✅ Asset lifecycle tracking
* ✅ Ownership intelligence layer
* ✅ Soft delete strategy
* ✅ Scalable architecture
* ✅ Enterprise-style service layer
* ✅ Beyond basic CRUD implementation
* 
---

# ⚙️ Running the Project (Example Setup)

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 📌 Final Notes

SAGAP Inventory Backend is designed for:

* Maintainability
* Historical accuracy
* Ownership tracking
* Future scalability
