import os.path
import traceback
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Annotated, Sequence

from aiosmtplib import SMTP
from nestipy.common import Injectable, TemplateEngine, logger
from nestipy.core.template import MinimalJinjaTemplateEngine
from nestipy.ioc import Inject

from .mailer_builder import MailerOption, MAILER_CONFIG_TOKEN


@Injectable()
class MailerService:
    config: Annotated[MailerOption, Inject(MAILER_CONFIG_TOKEN)]
    template_engine: TemplateEngine

    def __init__(self):
        self.smtp = SMTP(
            hostname=self.config.server,
            port=self.config.port,
            use_tls=self.config.ssl,
            username=self.config.sender,
            password=self.config.password,
            start_tls=False
        )
        if self.config.template_dir and os.path.exists(self.config.template_dir):
            self.template_engine = MinimalJinjaTemplateEngine(self.config.template_dir)

    async def send_mail(
            self,
            to: str | Sequence[str],
            _from: str,
            subject: str,
            text: str = '',
            html: str = None,
            template: str = None,
            context: dict = None,
            attachments: list[str] = None
    ):
        from_address = _from or self.config.sender
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = from_address
        message["To"] = to
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        if html:
            message.attach(MIMEText(html, 'html', 'utf-8'))
        elif template and self.template_engine:
            html = self.template_engine.render(template, context or {})
            message.attach(MIMEText(html, 'html', 'utf-8'))

        if attachments:
            self._add_attachment(message, attachments)
        await self.smtp.connect()
        await self.smtp.send_message(message)
        self.smtp.close();

    @classmethod
    def _add_attachment(cls, message: MIMEMultipart, attachments: list[str]):
        for att in attachments:
            with open(att, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                attachment.close()
                message.attach(part)
