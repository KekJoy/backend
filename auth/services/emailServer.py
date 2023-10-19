from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
import jwt

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME="valiullin.anton2003",
    MAIL_PASSWORD="unuozbrnvzgctdku",
    MAIL_FROM="valiullin.anton2003@yandex.ru",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def simple_send(email: EmailSchema, token: str) -> JSONResponse:
    html = f"""<a>Hi this test mail, thanks for using Fastapi-mail {token}</a> """

    token = jwt.encode(token)

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
