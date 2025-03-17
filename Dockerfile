# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set a non-root user for better security
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory
WORKDIR /app

# Copy dependencies file and install required packages
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Expose the application port
EXPOSE 5000

# Use gunicorn for better performance in production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
