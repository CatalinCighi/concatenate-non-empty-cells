# Microservice: Concatenate Non-Empty CSV Cells

## Overview

This microservice reads a CSV file, concatenates non-empty cells from each row, and returns the processed data either as a local file or as a JSON response via a REST API. It is useful as a first step in working with dirty data (e.g. bank statement CSV provided by low tech bank is garbled, has variable number of columns per each row, and requires extensive transformations).

## Features

- **Local Mode**: Processes a specified CSV file on the local filesystem.
- **API Mode**: Provides an HTTP endpoint for real-time file uploads and processing.
- **Configurable Input/Output**: Supports local files and HTTP-based data exchange.
- **Error Handling**: Includes robust error handling for malformed input.
- **Scalability**: Can run as a standalone service or in a containerized environment with Docker.

---

## Prerequisites

- **Python**: Version 3.11+
- **Dependencies**: Managed via `requirements.txt` (e.g., Flask, pandas, gunicorn)
- **Docker** (optional for containerized deployment)

---

## Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Local Mode

1. Set the `MODE` environment variable to `local`.
2. Specify the path to the input CSV file in `app.py`:

```python
if __name__ == "__main__":
    mode = os.getenv("MODE", "api")
    if mode == "local":
        df = concatenate_non_empty_cells_from_file("path/to/your/input.csv")
        save_to_file(df, "path/to/your/input.csv")
```

3. Run the script:

```bash
MODE=local python app.py
```

4. The output file will be saved in the same directory as the input file.

### API Mode

1. Start the Flask server:

```bash
python app.py
```

2. Use a tool like `curl` or Postman to send a POST request:

```bash
curl -X POST -F file=@your_input.csv http://localhost:5000/concatenate
```

3. The API will return the concatenated data as JSON.

---

## Running with Docker

### 1. Build the Docker Image

```bash
docker build -t concatenate-microservice .
```

### 2. Run the Docker Container

```bash
docker run -p 5000:5000 --env MODE=api --name concatenate-service concatenate-microservice
```

### 3. Access the API

Send a POST request to:

```
http://localhost:5000/concatenate
```

---

## Healthcheck

The Docker container includes a healthcheck to ensure the API is responsive. To check the health status:

```bash
docker inspect --format='{{json .State.Health.Status}}' concatenate-service
```

---

## Project Structure

```
project/
│
├── app.py        # Main application logic (REST API, mode switching)
├── utils.py      # Core functionality (CSV processing, file handling)
├── requirements.txt  # Python dependencies
└── Dockerfile    # Container configuration
```

---

## Testing

- **Local Mode**: Ensure input files are valid CSV files.
- **API Mode**: Test with different file sizes and malformed data.

---

## Best Practices Followed

- **Dependency Isolation**: Uses a virtual environment and `requirements.txt`.
- **Error Handling**: Robust handling of malformed input and file operations.
- **Logging**: Logs errors and status for debugging.
- **Non-Root User**: Docker container runs with a non-root user for security.
- **Healthcheck**: Ensures the container's service is running properly.

---

## Future Enhancements

- Add support for large file streaming in local mode.
- Implement advanced validation for CSV content.
- Extend input/output options (e.g., cloud storage, message queues).

---

## License

MIT License

---

## Author

Developed by Catalin Cighi
