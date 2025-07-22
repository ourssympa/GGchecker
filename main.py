from typing import Union

from fastapi import FastAPI
from database import engine, Base
from Controller import router as url_router
from url_checker_controller import send_mail_notification , check_url
from database import get_db
from fastapi_utilities import repeat_every
app = FastAPI()

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app.include_router(url_router, prefix="/api/urls")

@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # Exécute toutes les 5 minutes
async def read_root():
    db_gen = get_db()
    db = next(db_gen)
    response = await check_url(db)
    if(len(response["error_urls"]) > 0 or len(response["warning_urls"]) > 0):
        
        warning_lines = [
        f"- URL : {item['url']} | Status : {item['status_code']}"
        for item in response['warning_urls']
        ]
        warning_text = "\n".join(warning_lines)
        
        error_lines = [
            f"- URL : {item['url']} | Status : {item['status_code']}"
            for item in response['error_urls']
        ]
        error_text = "\n".join(error_lines)

        send_mail_notification(
            subject="ERROR REPORT",
            body=f"nous avons une erreur sur le(s) URL(s) suivant(s): {error_text}\n\nAvertissements: {warning_text}"
        )
    else:
        send_mail_notification(
        subject="SUCCESS REPORT",
        body="All URLs are OK"
        )
    return {"message": "Welcome to the URL Checker API"}
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}