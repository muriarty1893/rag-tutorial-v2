from nicegui import ui
from datetime import datetime
from log_utils import log_interaction
from main import query_rag
import asyncio

def main():
    async def handle_query():
        user_input = input_box.value
        loading_label.style('visibility: visible;')  # "Loading..." görünür yap
        ui.update()  # UI'yi güncelle

        # LLM'den yanıt almak için asenkron çağrı
        llm_output = await asyncio.to_thread(query_rag, user_input)
        log_interaction(user_input, llm_output)

        # Yeni cevapları sütuna ekle
        with output_column:
            ui.label(f"Query: {user_input}")
            ui.label(f"Output: {llm_output}").style("font-weight: bold; color: #007BFF;")
            ui.label(f"Logged at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").style("font-size: small; color: gray;")
            ui.separator()

        loading_label.style('visibility: hidden;')  # "Loading..." tekrar gizle
        ui.update()  # UI'yi tekrar güncelle

    with ui.card():
        ui.label('LLM Query Interface')
        input_box = ui.input(label='Enter your query', placeholder='Type your question here...')
        loading_label = ui.label('Loading, please wait...').style('visibility: hidden; color: black;')  # CSS ile görünmez
        ui.button('Submit', on_click=lambda: asyncio.create_task(handle_query()))
        output_column = ui.column()  # Cevapların biriktiği sütun

    # NiceGUI sunucusunu başlat
    ui.run(port=8080)

# Multiprocessing uyumluluğu için gerekli guard
if __name__ in {"__main__", "__mp_main__"}:
    main()
