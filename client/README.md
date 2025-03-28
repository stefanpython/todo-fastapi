# Project: Next.js & FastAPI Todo App

This project is a simple Todo application built as part of my learning process. It features a frontend built with Next.js and Tailwind CSS, while the backend is implemented using FastAPI with Python. The application supports CRUD operations,todos, login and register that are stored in memory.

## Features

- **Next.js Frontend**: A modern, responsive UI built using React and Tailwind CSS.
- **FastAPI Backend**: A lightweight and fast backend using Python and FastAPI.
- **CRUD Operations**:
  - Create a new todo
  - Read existing todos
  - Update a todo
  - Delete a todo
- **In-Memory Storage**: Todos are stored in memory for simplicity.
- **User Authentication**:
  - Register new users
  - Login functionality

## Technologies Used

### Frontend:

- Next.js
- Tailwind CSS

### Backend:

- Python
- FastAPI

## Setup Instructions

### Backend:

1. Install dependencies:
   \`\`\`sh
   npm install fastapi uvicorn
   \`\`\`
2. Run the FastAPI server:
   \`\`\`sh
   uvicorn main:app --reload
   \`\`\`

### Frontend:

1. Install dependencies:
   \`\`\`sh
   npm install
   \`\`\`
2. Run the Next.js development server:
   \`\`\`sh
   npm run dev
   \`\`\`

## API Endpoints

- \`GET /todos\` - Retrieve all todos
- \`POST /todos\` - Create a new todo
- \`PUT /todos/{id}\` - Update a specific todo
- \`DELETE /todos/{id}\` - Delete a specific todo
- \`POST /register\` - Register a new user
- \`POST /login\` - User login

## Notes

- This project is part of my learning journey and does not include database persistence.
- Improvements such as authentication and persistent storage can be added in the future.

## License

This project is open-source and free to use.
