from nestipy.common import Module
from .mailer_builder import ConfigurableClassBuilder
from .mailer_service import MailerService


@Module(
    providers=[
        MailerService
    ],
    exports=[
        MailerService
    ]
)
class MailerModule(ConfigurableClassBuilder):
    pass
