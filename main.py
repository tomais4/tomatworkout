import flet as ft
import datetime
import os

# --- DADOS E CONFIGURAÇÕES ---
COR_FUNDO = "#121212"
COR_CARD = "#1E1E1E"
COR_PRIMARIA = "#536DFE"
COR_TEXTO = "#E0E0E0"

TREINOS = {
    "A: EMPURRAR": [
        {"nome": "Supino Inclinado", "series": ["TOP 6-9", "BACK 6-9"]},
        {"nome": "Supino Máquina", "series": ["FALHA 8-12", "FALHA 8-12"]},
        {"nome": "Elevação Lateral", "series": ["3x 12-15"]},
        {"nome": "Tríceps Testa", "series": ["2x FALHA 10-12"]}
    ],
    "B: PUXAR": [
        {"nome": "Puxada Alta", "series": ["TOP 8-10", "BACK 8-10"]},
        {"nome": "Remada Apoiada", "series": ["2x FALHA 8-12"]},
        {"nome": "Crucifixo Inverso", "series": ["3x 12-15"]},
        {"nome": "Rosca Scott", "series": ["2x FALHA 8-12"]}
    ],
    "C: PERNAS": [
        {"nome": "Hack Squat", "series": ["TOP 5-8", "BACK 5-8"]},
        {"nome": "Extensora", "series": ["2x DROP-SET"]},
        {"nome": "Flexora", "series": ["2x FALHA 8-10"]},
        {"nome": "Panturrilha", "series": ["2x FALHA 10-15"]}
    ]
}

def main(page: ft.Page):
    # --- VACINA CONTRA CRASH (Essencial) ---
    def handle_lifecycle(e):
        if e.data == "detach":
            os._exit(1)
    page.on_app_lifecycle_state_change = handle_lifecycle
    # ---------------------------------------

    page.title = "Gym Tomate Legacy"
    page.bgcolor = COR_FUNDO
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK

    # Inicializa o banco de dados seguro
    if not page.client_storage.contains_key("gym_data"):
        page.client_storage.set("gym_data", {"historico": []})

    def salvar_treino(nome_treino, inputs):
        historico = page.client_storage.get("gym_data")["historico"]
        historico.append({
            "data": str(datetime.date.today()),
            "treino": nome_treino,
            "concluido": True
        })
        page.client_storage.set("gym_data", {"historico": historico})
        
        # --- COMANDO CORRIGIDO PARA FLET 0.22.0 ---
        page.snack_bar = ft.SnackBar(ft.Text("Treino Salvo com Sucesso!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()
        # ------------------------------------------
        
        menu()

    def abrir_treino(e):
        nome = e.control.data
        page.clean()
        
        lista = ft.Column(expand=True, scroll="auto")
        lista.controls.append(ft.Text(f"TREINO: {nome}", size=20, weight="bold", color="blue"))
        
        inputs_series = []
        
        for ex in TREINOS[nome]:
            col_series = ft.Column()
            for s in ex['series']:
                linha = ft.Row([
                    ft.Text(s, color="white", size=12, width=80),
                    ft.TextField(width=60, text_size=12, hint_text="Kg", border_color="#333", text_align="center"),
                    ft.TextField(width=60, text_size=12, hint_text="Reps", border_color="#333", text_align="center")
                ])
                col_series.controls.append(linha)
            
            card = ft.Container(
                content=ft.Column([ft.Text(ex['nome'], weight="bold"), col_series]),
                bgcolor=COR_CARD, padding=10, border_radius=10
            )
            lista.controls.append(card)
            inputs_series.append(col_series)

        btn_salvar = ft.ElevatedButton("SALVAR E FINALIZAR", 
            on_click=lambda _: salvar_treino(nome, inputs_series),
            bgcolor="green", color="white", height=50, width=300
        )
        
        page.add(lista, ft.Container(content=btn_salvar, alignment=ft.alignment.center, padding=10))

    def menu():
        page.clean()
        page.add(ft.Text("GYM TOMATE - V.FINAL", size=24, weight="bold", color="red"))
        for t in TREINOS:
            page.add(ft.Container(
                content=ft.Text(t, size=18, weight="bold"),
                bgcolor=COR_CARD, padding=20, border_radius=10,
                on_click=abrir_treino, data=t
            ))
        page.update()

    menu()

ft.app(target=main)
