# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from scraper import Scraper
import os

# Define constants
TOKEN = "543gf5432122asdffds2345654323456786"

# Initialize FastAPI app
app = FastAPI()
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )

class ScrapeSettings(BaseModel):
    page_limit: Optional[int] = None
    proxy: Optional[str] = None

@app.post("/scrape", dependencies=[Depends(verify_token)])
async def scrape(settings: ScrapeSettings):
    scraper = Scraper(page_limit=settings.page_limit, proxy=settings.proxy)
    scraper.scrape_catalogue()
    return {"message": f"Scraped {scraper.products_scraped} products."}

if __name__ == "__main__":
    os.system("uvicorn main:app --reload")


