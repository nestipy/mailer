from dataclasses import dataclass
from typing import Any

from nestipy.dynamic_module import ConfigurableModuleBuilder, DynamicModule


@dataclass
class MailerOption:
    server: str
    port: int
    sender: str = None
    password: str = None
    template_dir: str = None
    ssl: bool = False
    default_sender: str = None


def _extra_callback(dynamic_module: DynamicModule, extras: dict[str, Any]):
    if is_global := extras.get('is_global'):
        dynamic_module.is_global = is_global


ConfigurableClassBuilder, MAILER_CONFIG_TOKEN = (
    ConfigurableModuleBuilder[MailerOption]()
    .set_method('for_root').set_extras(
        {'is_global': True}, _extra_callback
    ).build())
