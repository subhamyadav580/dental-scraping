# Dental Products Scraper with FastAPI

This project is a web scraping tool built using the FastAPI framework. The tool scrapes product information from a target website and stores it in a local JSON file. It also includes features like proxy support, page limit configuration, and token-based authentication.


# Steps for Usage of Code

 ## Requiremets
- Python 3.8+
- Redis (for caching)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/subhamyadav580/dental-scraping.git
    ```

2. **Navigate to the Project Folder**

    ```bash
    cd dental-scraping
    ```

3. **Create and Activate a Virtual Environment**

    ```bash
    python3 -m venv myvenv
    source myvenv/bin/activate
    ```

4. **Install Python Dependencies**

    ```bash
    pip3 install -r requirements.txt
    ```

5. **Install and Start Redis**

    - **On macOS (using Homebrew):**

        ```bash
        brew install redis
        brew services start redis
        ```

    - **On Ubuntu:**

        ```bash
        sudo apt update
        sudo apt install redis-server
        sudo systemctl enable redis-server.service
        sudo systemctl start redis-server.service
        ```

6. **Start the FastAPI Server**

    ```bash
    python3 main.py
    ```

## Testing the API

1. **Send a POST request to the `/scrape` endpoint:**

    - **Without Proxy:**

        ```bash
        curl --location 'http://127.0.0.1:8000/scrape' \
        --header 'accept: application/json' \
        --header 'Authorization: Bearer 543gf5432122asdffds2345654323456786' \
        --header 'Content-Type: application/json' \
        --data '{
            "page_limit": 5
        }'
        ```

    - **With Proxy:**

        ```bash
        curl --location 'http://127.0.0.1:8000/scrape' \
        --header 'accept: application/json' \
        --header 'Authorization: Bearer 543gf5432122asdffds2345654323456786' \
        --header 'Content-Type: application/json' \
        --data '{
            "page_limit": 5,
            "proxy": "https://proxy:port"
        }'
        ```

2. **Check the Console Output**

   The console will show the status of the scraping process, including the number of products scraped.

## Explanation of Important Files

- **main.py**: Contains the FastAPI application and endpoint definitions.
- **scraper.py**: Contains the `Scraper` class that performs the web scraping.
- **requirements.txt**: Lists the Python packages required for the project.
- **products.json**: The file where scraped products are stored.
- **images/**: Directory where product images are saved.
