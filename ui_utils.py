from nicegui import ui
from datetime import datetime
from log_utils import log_interaction
from main import query_rag
import asyncio

def main():
    async def handle_query():
        user_input = input_box.value
        loading_label.visible = True
        ui.update()  # UI'yi hemen güncelleyin

        # LLM'den yanıt almak için asenkron çağrı
        llm_output = await asyncio.to_thread(query_rag, user_input)
        log_interaction(user_input, llm_output)

        # UI güncellemelerini ana iş parçacığında yapın
        loading_label.visible = False
        output_text.text = f"Output: {llm_output}"
        log_status.text = f"Log entry created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        ui.update()

    with ui.card():
        ui.label('LLM Query Interface')
        input_box = ui.input(label='Enter your query', placeholder='Type your question here...')
        ui.button('Submit', on_click=lambda: asyncio.create_task(handle_query()))
        loading_label = ui.label('Loading...').style('display: none;')  # Başlangıçta gizli
        output_text = ui.label()
        log_status = ui.label()

    # NiceGUI sunucusunu başlat
    ui.run(port=8080)

# Multiprocessing uyumluluğu için gerekli guard
if __name__ in {"__main__", "__mp_main__"}:
    main()
