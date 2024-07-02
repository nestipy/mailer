from typing import Annotated

from nestipy.common import Injectable
from nestipy.ioc import Inject

from nestipy_mailer import MailerService


@Injectable()
class AppService:
    mailer: Annotated[MailerService, Inject()]

    async def get(self):
        await self.mailer.send_mail(
            to='test@mail.test',
            _from='test_sender@mail.com',
            subject="Hello ",
            text="test message"
        )
        return "test"

    @classmethod
    async def post(cls, data: dict):
        return "test"

    @classmethod
    async def put(cls, id_: int, data: dict):
        return "test"

    @classmethod
    async def delete(cls, id_: int):
        return "test"
