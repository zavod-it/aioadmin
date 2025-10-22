from aiogram import Router
from aiogram_dialog import setup_dialogs

from aioadmin.adapter import Adapter
from aioadmin.aiogram.middleware import AdaperMiddleware
from aioadmin.aiogram.handlers.menu import menu_window


class AdminRouter(Router):
    def __init__(self, *, name = None, adapter: Adapter):
        super().__init__(name=name)
        self.message.middleware.register(AdaperMiddleware(adapter=adapter))
        self.include_routers(
            menu_window
        )
        setup_dialogs(self)