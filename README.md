# UML Activity Diagrams

## Purpose of Each Diagram

### 1. User Authentication Activity Diagram
The **User Authentication** activity diagram visualizes the login process for users in the RevoBank system. It captures:
- The process of entering login credentials.
- Verification of credentials by the system.
- Handling of incorrect login attempts (logging the attempt and sending an email notification).
- Successful authentication leading to token generation.
- The final outcome, whether the login succeeds or fails.

### 2. Transaction Handling Activity Diagram
The **Transaction Handling** activity diagram represents the process of handling financial transactions in the RevoBank system. It details:
- How a user initiates a transaction.
- The verification of the account balance before proceeding.
- The transaction process if the balance is sufficient.
- Handling of failed transactions due to insufficient funds.
- The generation of transaction history for successful transactions.

---

## Key Decisions and Processes Represented

### User Authentication:
- **Decision:** Is the entered credential valid?
  - Yes → Generate token and log in.
  - No → Record failed attempt and send an email notification.
- **Process:** 
  - If valid, the system generates a token and grants access.
  - If invalid, the system records the failed login attempt and notifies the user.

### Transaction Handling:
- **Decision:** Does the user have sufficient funds?
  - Yes → Process the transaction and update transaction history.
  - No → Decline the transaction and notify the user.
- **Process:**
  - The user initiates the transaction, and the system verifies account balance.
  - If the balance is sufficient, the transaction is processed and recorded.
  - If insufficient, the transaction fails, and the user is notified.

---

## UML Activity Diagrams
The UML activity diagrams were created using **Lucidchart**:
- **User Authentication:** [Lucidchart Diagram](https://lucid.app/lucidchart/e0641486-acc9-4f04-b759-d0b92dcd568a/edit?viewport_loc=-24%2C-64%2C1730%2C1001%2C0_0&invitationId=inv_41aaa07b-f7cc-44d3-9419-ce6a93b1eeb5)
- **Transaction Handling:** [Lucidchart Diagram](https://lucid.app/lucidchart/afdb94bf-f4ec-40e0-84c1-3ac1ec25fcc0/edit?viewport_loc=420%2C-25%2C1617%2C936%2C0_0&invitationId=inv_4dbfd3cf-634b-4c6f-8cda-576621a6ad42)

---
# RESTful API Endpoints
## User Management
- **POST /users**
``bash
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "StrongP@ssw0rd"
}
``
- **POST /users/login**
Verify credentials and return JWT token.
- **GET /users/me**
To retrieve logged-in user's profile
``bash
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com"
}
``
- **PUT /users/me**
To update current user's profile which require JWT.
``bash
{
  "username": "john_doe_new",
  "password": "NewStr0ngP@ssw0rd"
}
``

## Account Management
- **GET /accounts**
- **GET /accounts/<id>**
- **POST /accounts**
- **PUT /accounts/<id>**
- **DELETE /accounts/<id>**

## Transaction Management
- **GET /transactions**
- **GET /transactions/<id>**
- **POST /transactions**

# Database Connection & Models (Schema Design)
API uses Flask-SQLAlchemy for ORM and managing the database.

## Models
- **User**
  Fields: id, username, email, password_hash, created_at, updated_at
  Relationships: One-to-many with `Account`
- **Account**
  Fields: id, user_id, account_type, account_number, balance, created_at, updated_at
  Relationships: One-to-many with `Transaction`
- **Transaction**
  Fields: id, account_id, transaction_type, amount, description, created_at

## Setting Up the Database
### Configuration
``bash
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///revobank.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
``
### Initialization
Run init_db.py

## CRUD Operations Using SQLAlchemy
1. Create - Endpoints for registering a user (POST /users), creating an account (POST /accounts), and initiating transactions (POST /transactions) use db.session.add() and db.session.commit() to save new records.
2. Read - Endpoints like GET /accounts, GET /accounts/<id>, and GET /transactions/<id> query the database using SQLAlchemy’s query interface.
3. Update - Endpoints (PUT /users/me and PUT /accounts/<id>) fetch the existing record, update fields, and commit changes.
4. Delete - The DELETE /accounts/<id> endpoint removes records using db.session.delete() and db.session.commit().

## Secure Authentication & Authorization
- JWT Authentication - requiring authentication are decorated with @jwt_required(). The authenticated user is identified using get_jwt_identity(), and this ID is used to ensure users can only access or modify their own data.
- Authorization Checks - when updating or deleting an account, the endpoint checks if the authenticated user owns the account. Unauthorized attempts return 403 Forbidden.

# Testing & Troubleshooting
## Testing Tools
Use Postman, cURL, or similar tools to send HTTP requests to the API.

## Test Scenarios
1. User Operations
2. Account Operations
3. Transaction Operations

## Common Errors
1. 401 Unauthorized
2. 403 Forbidden
3. 404 Not Found
4. 400 Bad Request

# Environment Setup & Deployment
1. Install Dependencies
2. Environment Variables
3. Database Initialization
4. Running the Application using Flask
5. Deployment
