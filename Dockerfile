# Use a stable Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if required (git, build tools, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements or project files
COPY requirements.txt .

# Install Python dependencies (including hydrogram, tgcrypto, python-dotenv, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's source code into the container
COPY . .

# Command to run your bot
CMD ["python", "bot.py"]
