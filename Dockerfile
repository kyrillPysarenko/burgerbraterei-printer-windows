FROM python:3.9

# Install necessary packages
RUN apt-get update && apt-get install -y cups libcups2-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app
WORKDIR /app

# Start your FastAPI application or other services
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
