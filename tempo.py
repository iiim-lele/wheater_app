import flet as ft
import httpx
from datetime import datetime

API_KEY = "05f4ee67848cc2f2685db6e4c1cf5f3e"

# ===================== ESQUEMAS DE COR =====================

import flet as ft
import httpx
from datetime import datetime

API_KEY = "05f4ee67848cc2f2685db6e4c1cf5f3e"

# ===================== ESQUEMAS DE COR =====================
light_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE,
    on_primary=ft.Colors.WHITE,
    background=ft.Colors.WHITE,
    on_background=ft.Colors.BLACK,
    surface=ft.Colors.WHITE,
    on_surface=ft.Colors.BLACK,
)

dark_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE_700,
    on_primary=ft.Colors.WHITE,
    background=ft.Colors.BLACK,
    on_background=ft.Colors.WHITE,
    surface=ft.Colors.BLACK,
    on_surface=ft.Colors.WHITE,
)

light_theme = ft.Theme(color_scheme=light_color_scheme)
dark_theke = ft.Theme(color_scheme=dark_color_scheme)

def get_icon(icon_code):
    icon_map = {
        "01d": ft.Icons.SUNNY, "01n": ft.Icons.NIGHTLIGHT,
        "02d": ft.Icons.CLOUD, "01n": ft.Icons.CLOUD,
        "03d": ft.Icons.CLOUD, "01n": ft.Icons.CLOUD,
        "04d": ft.Icons.CLOUD, "01n": ft.Icons.CLOUD,
        "09d": ft.Icons.WATER_DROP, "01n": ft.Icons.WATER_DROP,
        "10d": ft.Icons.WATER_DROP, "01n": ft.Icons.WATER_DROP,
        "11d": ft.Icons.FLASH_ON, "01n": ft.Icons.FLASH_ON,
        "13d": ft.Icons.AC_UNIT, "01n": ft.Icons.AC_UNIT,
        "50d": ft.Icons.VISIBILITY, "01n": ft.Icons.VISIBILITY,
    }
    return icon_map.get(icon_code, ft.Icons.QUESTION_MARK)

def translate_weekday(weekday):
    translations = {
        "Mon": "Seg", "Tue": "Ter", "Wed": "Qua",
        "Thu": "Qui", "Fri": "Sex", "Sat": "Sáb", "Sun": "Dom"
    }
    return translations.get(weekday, weekday)

async def get_weather(city, country):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{city},{country}",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    return resp.json()

async def main(page: ft.Page):
    page.padding = ft.padding.only(left=10, right=10, top=40)
    page.title = "Previsão do Tempo"
    page.theme = light_theme
    page.dark_theme = dark_theke
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 360
    page.window_height = 760
    page.window_resizable = False

    city = "São Paulo"

    # Botão para alternar o tema
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.LIGHT_MODE
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        on_click=toggle_theme
    )

    # Dropdown de cidades
    async def on_city_change(e: ft.ControlEvent):
        await load_weather(e.control.value)

    city_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("São Paulo"),
            ft.dropdown.Option("Rio de Janeiro"),
            ft.dropdown.Option("Brasília"),
            ft.dropdown.Option("Salvador"),
            ft.dropdown.Option("Belo Horizonte"),
            ft.dropdown.Option("Fortaleza"),
            ft.dropdown.Option("Curitiba"),
            ft.dropdown.Option("Manaus"),
            ft.dropdown.Option("Recife"),
            ft.dropdown.Option("Porto Alegre")
        ],
        value=city,
        on_change=on_city_change,
        width=250,
        # Deixe "filled=True" para ter um fundo e borda
        filled=True,
        # Define a cor da borda usando "on_background",
        # que no tema escuro é branco
        border_color=lambda: page.theme.color_scheme.on_background,
        focused_border_color=lambda: page.theme.color_scheme.on_background,
    )

    top_bar = ft.Row(
        controls=[
            city_dropdown,
            ft.Container(expand=1),
            theme_button
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    current_weather_container = ft.Container()
    forecast_column = ft.Column()

    # Imagem Senai no rodapé
    # Deixe "Senai.png" na pasta raiz do projeto
    senai_logo = ft.Image(
        src="Senai.png",
        width=150,
        height=50,
        fit=ft.ImageFit.CONTAIN
    )

    async def load_weather(selected_city):
        data = await get_weather(selected_city, "BR")
        if "list" not in data:
            current_weather_container.content = ft.Container(
                content=ft.Text("Erro ao carregar dados"),
                bgcolor=page.theme.color_scheme.primary,
                border_radius=20,
                padding=20
            )
            forecast_column.controls.clear()
            page.update()
            return
        
        cw = data["list"][0]
        weather_desc = cw["weather"][0]["description"].capitalize()
        icon_code = cw["weather"][0]["icon"]

        # Cartao azul (primary) => texto/icons em on_primary
        current_weather_container.content = ft.Container(
            bgcolor=page.theme.color_scheme.primary,
            border_radius=20,
            padding=20,
            content=ft.Column(
                [
                    ft.Text(
                        f"{selected_city}, BR",
                        size=20,
                        color=page.theme.color_scheme.on_primary
                    ),
                    ft.Text(
                        "Hoje",
                        size=16,
                        color=page.theme.color_scheme.on_primary
                    ),
                    ft.Row(
                        [
                            ft.Icon(
                                get_icon(icon_code),
                                size=50,
                                color=page.theme.color_scheme.on_primary
                            ),
                            ft.Text(
                                f"{cw['main']['temp']:.0f}°C",
                                size=50,
                                color=page.theme.color_scheme.on_primary
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(
                        weather_desc,
                        size=16,
                        color=page.theme.color_scheme.on_primary
                    ),
                ],
                spacing=5
            )
        )

        # Lista de previsão => fundo padrão => cor padrão
        forecast_column.controls.clear()
        next_days = data["list"][1:8]
        for item in next_days:
            date = datetime.fromtimestamp(item["dt"])
            day_str = translate_weekday(date.strftime("%a"))
            desc = item["weather"][0]["description"].capitalize()
            ic = item ["weather"][0]["icon"]
            min_temp = f"{item['main']['temp_min']:.0f}°C"
            max_temp = f"{item['main']['temp_max']:.0f}°C"

            row = ft.Row(
                [
                    ft.Container(width=40, content=ft.Text(day_str)),
                    ft.Container(width=40, alignment=ft.alignment.center, content=ft.Icon(get_icon(ic))),
                    ft.Container(width=120, content=ft.Text(desc)),
                    ft.Container(width=40, alignment=ft.alignment.center_right, content=ft.Text(min_temp)),
                    ft.Container(width=40, alignment=ft.alignment.center_right, content=ft.Text(max_temp)),
                ],
                alignment=ft.MainAxisAlignment.START
            )
            forecast_column.controls.append(row)

        page.update()

    # Montagem final da página
    page.add(
        ft.Column(
            [
                top_bar,
                current_weather_container,
                ft.Container(height=10),
                forecast_column,
                # Rodapé com imagem do Senai centralizada
                ft.Container(
                    content=senai_logo,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=20)
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
    )

    await load_weather(city)

ft.app(target=main)