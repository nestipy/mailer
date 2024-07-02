from nestipy.common import Module

from app_controller import AppController
from app_service import AppService

from nestipy_mailer import MailerModule, MailerOption


@Module(
    imports=[
        MailerModule.for_root(
            MailerOption(
                server="localhost",
                port=1035
            )
        )
    ],
    controllers=[AppController],
    providers=[AppService]
)
class AppModule:
    ...
