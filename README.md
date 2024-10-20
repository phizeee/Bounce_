
---

# FastAPI Application

This is a simple FastAPI application that uses a backend API and a frontend interface to serve web content. The application is structured with separate directories for the frontend and backend components.

## File Structure

```bash
├── frontend/         # Contains the frontend files (HTML, CSS, JavaScript, Bootstrap, Images)
├── backend/          # Contains the FastAPI backend application (Python code and ML model)
└── README.md         # Documentation for the project
```

### Frontend Directory (`frontend/`)

This directory holds all the assets for the user interface, including:

- **HTML**: The main structure of the web pages.
- **CSS**: Styling and layout information.
- **JavaScript**: Handles dynamic behavior on the web pages (e.g., form submissions, API calls).
- **static/**: Contains any static files (images, CSS, JS) served by the FastAPI app.

### Backend Directory (`backend/`)

This directory contains the FastAPI backend code, which includes:

- **main.py**: The main FastAPI app where routes and API endpoints are defined.
- **rag.py**: Openai powered RAG model for data analysis and comparison
- **embeddings.py**: For creating vector embeddings of the datasets
- **routes/**: A subfolder containing different route files for organizing your API endpoints.
- **static/**: Contains any static files (images, CSS, JS) served by the FastAPI app.

---

## Requirements

To run this project, ensure you have the following installed:

- **Python 3.8+**
- **FastAPI**
- **Uvicorn** (for serving the FastAPI app)
- **Openai** 

You can install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```

### Add OpenAI key to .env file
```bash
OPENAI_API_KEY=your_openai_key
```
---

## How to Run the Application

### 1. Backend

The FastAPI app is located in the `backend/` folder. To run the backend server:

```bash
# Navigate to the backend directory
cd backend/

# Run the FastAPI application using uvicorn
uvicorn app:app --reload
```

The backend server will be available at `http://127.0.0.1:8000/` by default.

### 2. Frontend

The `frontend/` folder contains the static files (HTML, CSS, and JavaScript) for the user interface. You can serve the static files from the FastAPI backend using the `StaticFiles` middleware or by hosting them separately via another service (e.g., Nginx or a simple Python server).

#### Example for Serving Static Files:

In your `backend/app.py`:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the frontend directory as static files
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
```

Once mounted, you can access the frontend files via `http://127.0.0.1:8000/frontend/`.

---

## API Endpoints

Below are some example API endpoints you can expect from the FastAPI backend:

- `GET /`: Returns a welcome message.
- `POST /analyze/ -d {'text': "How do consumer preferences differ between Christmas shopping and sustainable shopping?"}`: Returns a welcome message.
- `POST /submit/`: Accepts form data and returns a response from html

You can find additional routes in the `backend/main.py` file
The application has many more endpoints than what is being served in the html script.

---

## Deployment

For production, you may want to use a more robust server setup. Here’s an example using `gunicorn` with `uvicorn` workers:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

---

## Contributing

If you want to contribute to this project:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request for review.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For any inquiries, please reach out at `peterchithambo.pc@gmail.com`.

---
