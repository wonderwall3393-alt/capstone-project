# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements first (for better caching)
RUN echo "flask==3.0.0" > requirements.txt && \
    echo "flask-cors==4.0.0" >> requirements.txt && \
    echo "numpy==1.24.3" >> requirements.txt && \
    echo "pandas==1.5.3" >> requirements.txt && \
    echo "scikit-learn==1.2.2" >> requirements.txt && \
    echo "pickle5==0.0.12" >> requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=hybrid_ml_survey_server.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application
CMD ["python", "-u", "hybrid_ml_survey_server.py"]