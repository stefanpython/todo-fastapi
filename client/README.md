# Todo App 📝

This is a simple **To-Do List** web application built for learning purposes. It features a **Vite + React + Tailwind CSS** frontend and a **FastAPI + Python** backend.

## 🚀 Features

- Add, update, delete, and retrieve todos
- In-memory storage (data is lost on server restart)
- RESTful API with JSON responses
- Modern frontend with React, Vite, and Tailwind CSS
- Fast backend with FastAPI

## 🛠 Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** React, Vite, Tailwind CSS
- **State Management:** React Hooks

## 📦 Installation

### Backend Setup (FastAPI)

1. Clone the repository:

   ```sh
   git clone https://github.com/stefanpython/todo-fastapi.git
   cd todo-fastapi
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install fastapi uvicorn
   ```

4. Start the FastAPI server:

   ```sh
   uvicorn main:app --reload
   ```

5. The API will be available at:
   ```
   http://127.0.0.1:8000
   ```

### Frontend Setup (React + Vite)

1. Navigate to the frontend folder:

   ```sh
   cd frontend
   ```

2. Install dependencies:

   ```sh
   npm install
   ```

3. Start the development server:

   ```sh
   npm run dev
   ```

4. Open the frontend in your browser:
   ```
   http://localhost:5173
   ```

## 📌 API Endpoints

### Get all todos

```http
GET /todos
```

Response:

```json
[{ "id": 1, "title": "Sample task", "completed": false }]
```

### Get a single todo

```http
GET /todos/{id}
```

### Add a new todo

```http
POST /todos
```

Request body:

```json
{ "title": "New task" }
```

### Update a todo

```http
PUT /todos/{id}
```

Request body:

```json
{ "title": "Updated task", "completed": true }
```

### Delete a todo

```http
DELETE /todos/{id}
```

## 🏗 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature-branch`)
5. Open a pull request

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

💡 Happy coding! 🚀
