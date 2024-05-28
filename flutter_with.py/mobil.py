import flet as ft
from flet import TextField
from flet_core.control_event import ControlEvent

def main(page: ft.Page) -> None:
    page.title = 'Increment Counter'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'dark'


    text_number: TextField = TextField(value='0', text_align=ft.TextAlign.RIGHT, width=100, color= 'purple')

    def decrement(e: ControlEvent) -> None:
        text_number.value = str(int(text_number.value) - 1)
        page.update()

    def increment(e: ControlEvent) -> None:
        text_number.value = str(int(text_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.REMOVE, on_click=decrement),
                text_number,
                ft.IconButton(icon=ft.icons.ADD, on_click=increment)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)
