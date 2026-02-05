import flet as ft
import datetime
import os

# --- CORES E ESTILO ---
COR_FUNDO = "#121212"     # Preto suave
COR_CARD = "#1E1E1E"      # Cinza escuro para os cartões
COR_PRIMARIA = "#536DFE"  # Azul Indigo (Botões)
COR_TEXTO = "#FFFFFF"

# --- DADOS DOS TREINOS ---
TREINOS_PADRAO = {
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
    # 1. Configuração da Janela (Android)
    page.bgcolor = COR_FUNDO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    # Impede o teclado de quebrar o layout
    page.window_prevent_close = True 

    # 2. Vacina contra Fechamento Inesperado (Crash Fix)
    def handle_lifecycle(e):
        if e.data == "detach":
            os._exit(1)
    page.on_app_lifecycle_state_change = handle_lifecycle

    # --- FUNÇÕES DE NAVEGAÇÃO ---
    def mudar_para_home(e=None):
        page.clean()
        
        # Conteúdo da Home
        conteudo = ft.Column([
            ft.Container(height=50), # Espaço topo
            ft.Icon(ft.icons.FITNESS_CENTER, size=80, color=COR_PRIMARIA),
            ft.Text("GYM TOMATE", size=30, weight="bold", color="white"),
            ft.Text("V26 - FINAL STABLE", size=12, color="green", weight="bold"),
            ft.Container(height=30),
            
            ft.ElevatedButton(
                "INICIAR TREINO",
                icon=ft.icons.PLAY_ARROW,
                bgcolor=COR_PRIMARIA,
                color="white",
                height=60,
                width=280,
                on_click=mudar_para_selecao
            )
        ], horizontal_alignment="center", alignment="center", spacing=10)

        # Container centralizado
        page.add(ft.Container(content=conteudo, alignment=ft.alignment.center, expand=True))

    def mudar_para_selecao(e=None):
        page.clean()
        
        lista_treinos = ft.Column(spacing=15, horizontal_alignment="center")
        
        for nome_treino in TREINOS_PADRAO:
            # Botão do Treino (Cartão Grande)
            btn = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.SPORTS_GYMNASTICS, color="white"),
                    ft.Text(nome_treino, size=18, weight="bold", color="white"),
                ], alignment="center"),
                bgcolor=COR_CARD,
                padding=25,
                border_radius=15,
                width=320,
                on_click=lambda e, x=nome_treino: mudar_para_execucao(x), # Ação do clique
                ink=True # Efeito de clique visual
            )
            lista_treinos.controls.append(btn)

        # Estrutura da tela
        page.add(
            ft.Column([
                ft.Container(height=20),
                ft.Text("QUAL O TREINO DE HOJE?", size=18, color="grey"),
                ft.Container(height=10),
                lista_treinos,
                ft.Container(height=20),
                ft.TextButton("Voltar para Início", on_click=mudar_para_home)
            ], horizontal_alignment="center", scroll="auto", expand=True)
        )

    def mudar_para_execucao(nome_treino):
        page.clean()
        
        lista_exercicios = ft.Column(scroll="auto", expand=True)
        inputs_salvar = [] # Para guardar as referências dos campos

        # Título do Treino
        lista_exercicios.controls.append(
            ft.Container(
                content=ft.Text(nome_treino, size=22, weight="bold", color=COR_PRIMARIA),
                padding=15
            )
        )

        # Monta os Exercícios
        dados_treino = TREINOS_PADRAO[nome_treino]
        
        for ex in dados_treino:
            linhas_series = ft.Column()
            series_refs = []

            for s in ex['series']:
                # Campos de entrada
                txt_carga = ft.TextField(width=70, text_align="center", hint_text="Kg", border_color="#333", keyboard_type="number", content_padding=5, text_size=14)
                txt_reps = ft.TextField(width=70, text_align="center", hint_text="Reps", border_color="#333", keyboard_type="number", content_padding=5, text_size=14)
                
                series_refs.append({"c": txt_carga, "r": txt_reps})

                linha = ft.Row([
                    ft.Text(s, size=12, width=80, color="white", no_wrap=False),
                    txt_carga,
                    txt_reps
                ], alignment="spaceBetween")
                
                linhas_series.controls.append(linha)
            
            inputs_salvar.append(series_refs)

            # Cartão do Exercício
            card = ft.Container(
                content=ft.Column([
                    ft.Text(ex['nome'], size=16, weight="bold"),
                    ft.Divider(color="#333"),
                    linhas_series
                ]),
                bgcolor=COR_CARD, padding=15, border_radius=10, margin=ft.margin.only(bottom=10)
            )
            lista_exercicios.controls.append(card)

        # Botão Salvar (Função Interna)
        def salvar_finalizar(e):
            # Lógica simples de salvar (apenas simulação visual para não travar)
            
            # --- CÓDIGO CORRIGIDO PARA FLET 0.22 (ANDROID) ---
            page.snack_bar = ft.SnackBar(ft.Text(f"Treino {nome_treino} Concluído!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            # -------------------------------------------------
            
            mudar_para_home()

        btn_concluir = ft.ElevatedButton("FINALIZAR TREINO", bgcolor="green", color="white", width=300, height=50, on_click=salvar_finalizar)
        
        # Adiciona tudo na tela
        page.add(
            ft.Column([
                lista_exercicios,
                ft.Container(content=btn_concluir, padding=20, alignment=ft.alignment.center)
            ], expand=True)
        )

    # Inicia na Home
    mudar_para_home()

ft.app(target=main)
