# Expense Tracker API

A comprehensive REST API for managing personal expenses, built with Python Flask and MongoDB. This API provides secure user authentication, expense categorization, and powerful filtering capabilities.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication system
- **Expense Management**: Complete CRUD operations for expenses
- **Category Management**: Predefined expense categories with custom descriptions
- **Advanced Filtering**: Filter expenses by date ranges (past week, last month, last 3 months, custom)
- **Expense Analytics**: Summary reports with category breakdowns
- **Data Validation**: Comprehensive input validation and error handling
- **MongoDB Integration**: Efficient NoSQL database operations

## 📋 Predefined Expense Categories

- Groceries
- Leisure
- Electronics
- Utilities
- Clothing
- Health
- Others

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Validation**: Marshmallow
- **CORS**: Flask-CORS

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense-tracker-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI=mongodb://localhost:27017/expense_tracker
   JWT_SECRET_KEY=your_secure_secret_key_here
   FLASK_ENV=development
   ```

4. **Start MongoDB**
   Make sure MongoDB is running on your system.

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 🔐 Authentication

All expense and category endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/users/register` | Register a new user | No |
| POST | `/api/users/login` | Login user | No |
| GET | `/api/users/profile` | Get user profile | Yes |

### Categories

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/categories` | Get all user categories | Yes |
| GET | `/api/categories/{id}` | Get specific category | Yes |
| POST | `/api/categories` | Create new category | Yes |
| PUT | `/api/categories/{id}` | Update category | Yes |
| DELETE | `/api/categories/{id}` | Delete category | Yes |

### Expenses

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/expenses` | Get expenses with filtering | Yes |
| GET | `/api/expenses/{id}` | Get specific expense | Yes |
| POST | `/api/expenses` | Create new expense | Yes |
| PUT | `/api/expenses/{id}` | Update expense | Yes |
| DELETE | `/api/expenses/{id}` | Delete expense | Yes |
| GET | `/api/expenses/summary` | Get expense summary | Yes |

### Expense Filtering Options

The `/api/expenses` endpoint supports the following query parameters:

- `filter`: Predefined filters
  - `past_week`: Last 7 days
  - `last_month`: Previous calendar month
  - `last_3_months`: Last 90 days
  - `custom`: Use with start_date and end_date
- `start_date`: Start date (ISO format: YYYY-MM-DDTHH:MM:SS)
- `end_date`: End date (ISO format: YYYY-MM-DDTHH:MM:SS)
- `category_id`: Filter by specific category
- `limit`: Limit number of results
- `include_summary`: Include summary statistics (true/false)

## 📝 Request/Response Examples

### User Registration

**Request:**
```json
POST /api/users/register
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### User Login

**Request:**
```json
POST /api/users/login
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Create Category

**Request:**
```json
POST /api/categories
{
  "title": "Groceries",
  "description": "Food and household items"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Category created successfully",
  "data": {
    "category": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "title": "Groceries",
      "description": "Food and household items",
      "user_id": "64f1a2b3c4d5e6f7g8h9i0j1"
    }
  }
}
```

### Create Expense

**Request:**
```json
POST /api/expenses
{
  "amount": 45.50,
  "note": "Weekly grocery shopping",
  "expense_date": "2024-01-15T10:30:00",
  "category_id": "64f1a2b3c4d5e6f7g8h9i0j2"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Expense created successfully",
  "data": {
    "expense": {
      "_id": "64f1a2b3c4d5e6f7g8h9i0j3",
      "amount": 45.50,
      "note": "Weekly grocery shopping",
      "expense_date": "2024-01-15T10:30:00",
      "category_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
      "created_at": "2024-01-15T10:32:15.123456"
    }
  }
}
```

### Get Filtered Expenses

**Request:**
```
GET /api/expenses?filter=past_week&include_summary=true
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "expenses": [
      {
        "_id": "64f1a2b3c4d5e6f7g8h9i0j3",
        "amount": 45.50,
        "note": "Weekly grocery shopping",
        "expense_date": "2024-01-15T10:30:00",
        "category_id": "64f1a2b3c4d5e6f7g8h9i0j2",
        "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
        "created_at": "2024-01-15T10:32:15.123456"
      }
    ],
    "summary": {
      "total_amount": 45.50,
      "total_count": 1,
      "category_breakdown": {
        "64f1a2b3c4d5e6f7g8h9i0j2": {
          "amount": 45.50,
          "count": 1
        }
      }
    }
  }
}
```

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive validation using Marshmallow schemas
- **Authorization**: User-specific data access controls
- **CORS Support**: Configurable cross-origin resource sharing

## ⚠️ Error Handling

The API returns consistent error responses:

```json
{
  "status": "error",
  "message": "Error description",
  "errors": {
    "field_name": ["Specific validation error"]
  }
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `404`: Not Found
- `500`: Internal Server Error

## 🧪 Testing

### Using curl

1. **Register a user:**
```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

2. **Login and get token:**
```bash
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

3. **Create a category:**
```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Groceries",
    "description": "Food and household items"
  }'
```

4. **Create an expense:**
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "amount": 45.50,
    "note": "Weekly grocery shopping",
    "expense_date": "2024-01-15T10:30:00",
    "category_id": "YOUR_CATEGORY_ID"
  }'
```

5. **Get expenses with filter:**
```bash
curl -X GET "http://localhost:5000/api/expenses?filter=past_week&include_summary=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🚀 Deployment

### Using Docker

1. **Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

2. **Build and run:**
```bash
docker build -t expense-tracker-api .
docker run -p 5000:5000 expense-tracker-api
```

### Environment Variables for Production

```env
MONGO_URI=mongodb://your-mongodb-connection-string
JWT_SECRET_KEY=your-very-secure-secret-key
FLASK_ENV=production
```



# snapshot for your view
---

# Run the API
```python simple_working_api.py```
```Register```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c5f615c4-3107-4888-b071-5035b6b51428" />


``` Set the Postman Header```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9bbdff11-7762-4b9c-867e-a650452dd6ac" />



```Login```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/30c104b6-356a-448a-b3e1-912833afa3fe" />


```MongoDBConnection```
<img width="1920" height="1080" alt="Screenshot (411)" src="https://github.com/user-attachments/assets/715b137e-1065-45cf-84f6-725a9ef38c08" />

## Categories
```Groceries```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8a7aa056-920b-4f01-bf15-0444b4555ff1" />

```Loded data innto MongoDB```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/409e514b-880a-4a1a-a14d-f39593433cfb" />

```Leisure```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/29d52a47-1b6a-41b7-8bcd-9805e6d96314" />

```Electronics```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/313c3ce5-9308-43b8-9ca2-a8fa43c9ee0b" />

```Utilities```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a03a5ed6-3892-4a53-94b8-202440d5a2ba" />

```Clothing```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ff3b8857-6b73-4715-84e3-211aff0d64eb" />

```Heath```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b1cebe10-526c-4c4a-acd8-0ae25c16b789" />

```Miscellaneous```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d93af8ed-4bac-45e2-9f2c-8996b2600ace" />

# Get the categories list
```All the categories listed```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/58e2009f-6a78-4a82-8c1c-5da7211a6488" />

# Set Monthly Income

```IntialAmount```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5858bff8-361b-4bb4-8c4a-f4ccf4adb353" />

# Added the Expenses

```Object Id -> Category Id```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/88e0661d-90e8-4319-b134-ad14fe736616" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c788a466-2779-4c51-9b32-b7104c09a98b" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a40063c2-a282-4594-9587-2c436f1bff97" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/93de3cfb-4e05-43e0-9f92-da8a40026e29" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6fee2b24-784e-4af1-9a58-f4e3e7cdc750" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d64f2fb6-723e-4618-88ec-e274c754a6c4" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5d5f18c6-bfd8-44bc-bb66-b5bb085761ae" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/26b6f8fb-b952-491f-8751-c1293f8b79f7" />


# Expense Filtering

```Past_week_Filtering```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/83aaad58-c074-485c-8156-9461a62fdf1b" />

```Last_Month_Filtering```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a4ae9dc4-83c9-44a4-8c92-4c3d6e6a19a4" />

```Last_three_month_Filtering```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f65fb371-1d46-4377-9a22-c196553d11fd" />

```Custom Date Range Filter```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5e4cf3ae-5572-4fe5-a2c6-05d37a3f0367" />

```Category Filter (Groceries)```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5319d90d-1808-460f-8611-d830c7f6c0c9" />


# Update Expense

```Grocery```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c389987d-f4de-4725-8b1a-097ce5b316a8" />

# Calculate Savings & Balance

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fba54200-f19f-4cdd-be48-e003fe9c789b" />

# Delete Expense
```Grocery_Lastly_update```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/39e5a26a-c0d4-4832-b052-c9857e8fcc1f" />

# Check Final Saving
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/083a3572-6b8b-4ce4-9c12-32c50db4855d" />

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

