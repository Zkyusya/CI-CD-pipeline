# Use the official Python image
FROM python:3.9-slim

# Set environment variables (modern KEY=VALUE syntax)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
# (we know requirements.txt lives in backend/ within the build context)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only your backend code into /app
COPY backend/ ./

# Prepare static folder (if your Flask app needs it)
RUN mkdir -p /app/static

# Expose the port your app will listen on
EXPOSE 8080

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
