from aiogram import Router

from aioadmin.adapter import Adapter
from aioadmin.aiogram.middleware import AdaperMiddleware


class AdminRouter(Router):
    def __init__(self, *, name = None, adapter: Adapter):
        super().__init__(name=name)
        self.message.middleware.register(AdaperMiddleware(adapter=adapter))
