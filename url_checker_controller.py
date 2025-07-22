from sqlalchemy.orm import Session
from model import Url
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def check_url(db: Session):
    error_url_list = []
    warning_url_list = []
    
    urls = db.query(Url).all()

    async with httpx.AsyncClient(timeout=3) as client:
        for url in urls:
            try:
                response = await client.get(url.url)
                if response.status_code == 200:
                    url.status = "up"
                else:
                    url.status = "down"
                    error_url_list.append({"url": url.url, "status_code": response.status_code})
            except httpx.TimeoutException:
                url.status = "warning"
                warning_url_list.append({"url": url.url, "status_code": "timeout"})
            except httpx.RequestError as e:
                url.status = "down"
                error_url_list.append({"url": url.url, "status_code": str(e)})
            
            db.commit()
    
    return {
        "message": "all url checked", 
        "error_urls": error_url_list, 
        "warning_urls": warning_url_list
    }


def send_mail_notification(subject: str, body: str):
     sender_email = "gracienfiomedon@gmail.com"
     sender_password = "jiihsmhuwsoyajrc"
     receiver_email = "hectorfiomedon@gmail.com"

     msg = MIMEMultipart()
     msg["From"] = sender_email
     msg["To"] = receiver_email
     msg["Subject"] = subject

     msg.attach(MIMEText(body, "plain"))

     try:
          with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
               server.login(sender_email, sender_password)
               server.sendmail(sender_email, receiver_email, msg.as_string())
          return {"message": "Email sent successfully"}
     except Exception as e:
          return {"error": str(e)}