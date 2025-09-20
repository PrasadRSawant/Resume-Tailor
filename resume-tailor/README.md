# Resume Tailor

A FastAPI application that uses LangGraph with Google Gemini LLM to tailor resumes based on job opportunity descriptions.

## Features

- **Job Description Parsing**: Utilizes Gemini LLM to extract key requirements from job descriptions.
- **Resume Tailoring**: Adapts your resume content to match the job opportunity.
- **PDF Output**: Generates a tailored `resume.pdf` (planned).

## Project Structure

```
resume-tailor/
├── .env.example
├── Dockerfile
├── README.md
├── main.py
├── requirements.txt
├── langgraph_agent.py
├── config.py
└── pyproject.toml
```

## Setup

### Prerequisites

- Python 3.9+
- pip
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd resume-tailor
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the `resume-tailor/` directory based on `.env.example` and add your Google Gemini API key:

   ```
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   ```

5. **Run the FastAPI application:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be accessible at `http://localhost:8000`.

## API Endpoints

- **POST `/tailor_resume/`**: Tailors a resume based on a provided job description.
  - **Request Body**: 
    ```json
    {
      "description": "string",
      "resume_file": "string (base64 encoded PDF content, optional)"
    }
    ```
  - **Response**: Tailored resume content (planned to be a PDF).

- **GET `/health`**: Health check endpoint.
  - **Response**: `{"status": "ok"}`

## Docker Deployment

1. **Build the Docker image:**

   ```bash
   docker build -t resume-tailor .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -d --name resume-tailor-app -p 8000:8000 -e GEMINI_API_KEY="YOUR_GEMINI_API_KEY" resume-tailor
   ```

   The API will be accessible at `http://localhost:8000`.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.