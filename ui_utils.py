from nicegui import ui
from datetime import datetime
from log_utils import log_interaction
from main import query_rag
import asyncio
import time

def main():
    async def handle_query():
 
        start_time = time.time()

        user_input = input_box.value
        loading_label.style('visibility: visible;')
        ui.update()

        llm_output = await asyncio.to_thread(query_rag, user_input)
        log_interaction(user_input, llm_output)

        elapsed_time = time.time() - start_time

        with output_column:
            ui.label(f"Query: {user_input}").classes("query-label")
            ui.label(f"Output: {llm_output}").classes("output-label")
            ui.label(f"Logged at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").classes("timestamp-label")
            ui.label(f"Response Time: {elapsed_time:.2f} seconds").classes("response-time-label")
            ui.separator()

        loading_label.style('visibility: hidden;')
        ui.update()

    ui.add_head_html("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9; /* Hafif gri arka plan */
            color: #333; /* Metin rengi */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .center-card {
            width: 400px;
            max-width: 90%;
            padding: 20px;
            border-radius: 15px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .query-label {
            color: #333;
            font-weight: bold;
        }
        .output-label {
            color: #007BFF; /* Açık mavi */
            font-size: 1.1em;
        }
        .timestamp-label {
            font-size: 0.9em;
            color: #888;
        }
        .response-time-label {
            color: #ff5722; /* Turuncu */
            font-weight: bold;
        }
        .separator {
            border-color: #ddd;
        }
        .loading-label {
            font-size: 1.2em;
            font-weight: bold;
            color: #007BFF;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
    </style>
    """)

    with ui.row().style('justify-content: center; align-items: center; max-height: 90%;'):
        with ui.card().classes('center-card'):
            ui.label('LLM Query Interface').style("font-size: 1.5em; font-weight: bold; margin-bottom: 20px; color: #333;")
            input_box = ui.input(label='Enter your query', placeholder='Type your question here...').style("width: 100%; margin-bottom: 20px;")
            loading_label = ui.label('Generating output, please wait...').style('visibility: hidden;').classes("loading-label")
            with ui.row():
                ui.button('Submit', on_click=lambda: asyncio.create_task(handle_query())).style("margin-right: 10px;")
                ui.button('Clear', on_click=lambda: output_column.clear())
            output_column = ui.column().style("margin-top: 20px;")

    
    ui.run(port=8080) # nicegui server

if __name__ in {"__main__", "__mp_main__"}:
    main()
