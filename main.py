import flet as ft
from convert_to_xlsx import convert_quiz_pdf_to_xlsx


def main(page: ft.Page):
    files = []
    files_list_ref = ft.Ref[ft.Column]()

    def update_files(new_files: list[str]):
        nonlocal files
        files = new_files
        files_list_ref.current.controls = [ft.Text(text) for text in new_files] if new_files else [
            ft.Text('Sem arquivos selecionados')]
        page.update()

    def on_result_files(e: ft.FilePickerResultEvent):
        nonlocal files
        files = list(map(lambda f: f.path, e.files)) if e.files else []
        update_files(files)
        page.update()

    def convert(e):
        nonlocal files
        new_files = []
        for file in files:
            try:
                new_files.append(convert_quiz_pdf_to_xlsx(file))
            except PermissionError as error:
                update_files(error.__notes__)
            except:
                update_files(["Erro: arquivo inválido"])

    file_picker = ft.FilePicker(on_result=on_result_files)
    page.title = "Conversor de quiz em pdf para xlsx"
    page.scroll = ft.ScrollMode.ALWAYS
    page.padding = ft.padding.all(20)
    page.overlay.append(file_picker)

    page.add(file_picker)
    page.add(
        ft.Column(
            controls=[
                ft.ElevatedButton(
                    text='Selecionar arquivos',
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda x: file_picker.pick_files(
                        allow_multiple=True, allowed_extensions=['pdf'])
                ),
                ft.ElevatedButton(
                    text='Converter',
                    icon=ft.icons.REFRESH,
                    on_click=convert
                ),
                ft.Column(
                    ref=files_list_ref,
                    controls=[ft.Text('Sem arquivos selecionados')]
                )
            ]
        )
    )


ft.app(target=main)
