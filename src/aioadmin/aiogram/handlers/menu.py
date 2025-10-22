from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Const, List, Format

from aioadmin.adapter import Adapter
from aioadmin.aiogram.handlers.states import Menu


async def get_tables(adapter: Adapter, dialog_manager: DialogManager, **kwargs):
    return { "tables": adapter.get_tables() }

menu_window = Dialog(
    Window(
        Const("Admin panel ⚙️"),
        Const("Tables: "),
        List(
            Format("- {item}"),
            items="tables",
        ),
        getter=get_tables,
        state=Menu.main
    )
)