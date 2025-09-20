# Resume Tailor

**A production-ready Python FastAPI project for tailoring resumes using LangGraph with Gemini LLM.**

## Project Overview

This project provides a FastAPI application that takes a job opportunity description and a candidate's resume (PDF) as input. It then leverages the power of LangGraph and Google's Gemini LLM to parse the job description, analyze the resume, and generate a tailored resume that highlights the most relevant skills and experiences for the given job.

## Features

*   **FastAPI Backend:** Robust and scalable API built with FastAPI.
*   **LangGraph Integration:** Utilizes LangGraph for building dynamic and stateful LLM applications.
*   **Gemini LLM:** Leverages Google's Gemini Large Language Model for intelligent resume tailoring.
*   **PDF Processing:** Handles PDF resume uploads and generates tailored PDF outputs.
*   **Containerized:** Docker support for easy deployment and scalability.
*   **Modular Design:** Organized project structure for maintainability and extensibility.

## Getting Started

### Prerequisites

*   Python 3.10+
*   Docker (optional, for containerized deployment)

### Local Development

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/resume-tailor.git
    cd resume-tailor
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Create a `.env` file in the root directory and add your Google Gemini API key:

    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```

5.  **Run the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.
    Access the API documentation at `http://127.0.0.1:8000/docs`.

### Docker Deployment

1.  **Build the Docker image:**

    ```bash
    docker build -t resume-tailor .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 --env-file .env resume-tailor
    ```

    The API will be accessible at `http://localhost:8000`.

## API Endpoints

*   **GET /**: Welcome message.
*   **POST /tailor-resume/**: Tailors a resume based on a job description. Expects a JSON payload for the job description and a PDF file for the resume.

## Project Structure

```
resume-tailor/
├── .env
├── Dockerfile
├── README.md
├── main.py
├── requirements.txt
└── # Further directories for LangGraph agents, LLM integrations, PDF processing, etc.
```

## Next Steps (Planned Integrations)

*   **LangGraph Agent Development:** Implement a robust LangGraph agent to orchestrate the resume tailoring process.
*   **Gemini LLM Integration:** Integrate with Google's Gemini API for advanced natural language understanding and generation.
*   **PDF Parsing:** Implement a module for extracting text and structure from uploaded PDF resumes.
*   **PDF Generation:** Develop a module for generating new, tailored PDF resumes.
*   **Testing:** Comprehensive unit and integration tests.
*   **CI/CD:** Setup Continuous Integration and Continuous Deployment pipelines.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details (to be created).
