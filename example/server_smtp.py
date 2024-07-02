import asyncio
from aiosmtpd.controller import Controller


class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from:', envelope.mail_from)
        print('Message to:', envelope.rcpt_tos)
        print('Message data:', envelope.content.decode('utf8', errors='replace'))
        return '250 Message accepted for delivery'


async def run_server():
    handler = CustomHandler()
    controller = Controller(handler, hostname='localhost', port=1035)
    controller.start()

    print('SMTP server running at localhost:1035')
    try:
        await asyncio.Event().wait()
    finally:
        controller.stop()


asyncio.run(run_server())
