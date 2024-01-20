FROM python:3.11
WORKDIR /app
RUN pip install --no-cache-dir pytest
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest"]
