import flet as ft
from reader import convert_txt_to_xlxs

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
        error_files = []
        for file in files:
            try:
                new_files.append(convert_txt_to_xlxs(file))
            except PermissionError as error:
                error_files.append((file, error.__notes__))
            except Exception as error:
                error_files.append((file, 'Erro: Arquivo inválido'))
                print(error)
        page.snack_bar = ft.SnackBar(
            ft.Text(f'{len(new_files)} arquivos foram convertidos com sucesso'))
        page.snack_bar.open = True
        page.update()

    file_picker = ft.FilePicker(on_result=on_result_files)
    page.title = "Conversor de quiz em txt para xlsx"
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
                        allow_multiple=True, allowed_extensions=['txt'])
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
