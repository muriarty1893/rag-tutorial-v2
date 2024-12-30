from nicegui import ui
from datetime import datetime
from log_utils import log_interaction
from main import query_rag
import asyncio
import time
import random

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

    placeholders = [
        "How many years of experience do you have?",
        "What is your favorite programming language?",
        "Tell me about your projects.",
        "What are your skills?",
        "Describe your career goals.",
        "What was your last project about?",
        "Which programming frameworks do you use?",
        "What motivates you to code?",
        "Have you worked in a team before?",
        "What is your strongest skill?",
        "How do you solve complex problems?",
        "What are your future learning plans?",
        "Can you describe a challenging project?",
        "What is your favorite tech tool?",
        "What do you like most about coding?"
    ]

    random_number = random.randint(1, 15)

    current_p = placeholders[random_number - 1]


    # CSS
    ui.add_head_html("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #FFFBE9; /* Light background color */
            color: #AD8B73; /* Primary text color */
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .center-card {
            width: 400px;
            max-width: 90%;
            padding: 20px;
            border-radius: 15px;
            background-color: #E3CAA5; /* Card background color */
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .query-label {
            color: #000000; /* Primary text color for queries */
            font-weight: bold;
        }
        .output-label {
            color: #000000; /* Accent color for outputs */
            font-size: 1.1em;
        }
        .timestamp-label {
            font-size: 0.9em;
            color: #000000; /* Secondary text color */
        }
        .response-time-label {
            color: #000000; /* Primary color for response time */
            font-weight: bold;
        }
        .separator {
            border-color: #E3CAA5; /* Soft separator color */
        }
        .loading-label {
            font-size: 1.2em;
            font-weight: bold;
            color: #000000; /* Accent color for loading text */
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
            ui.label('My Personal AI Guide!').style("font-size: 1.5em; font-weight: bold; margin-bottom: 20px; color: #000000;")
            input_box = ui.input(label='Type your question here, It will answer it. ', placeholder=current_p).style("width: 100%; margin-bottom: 20px;")
            loading_label = ui.label('Generating output, please wait...').style('visibility: hidden;').classes("loading-label")
            with ui.row():
                ui.button('Submit', on_click=lambda: asyncio.create_task(handle_query())).style("margin-right: 10px;")
                ui.button('Reset', on_click=lambda: output_column.clear())
            output_column = ui.column().style("margin-top: 20px; display: flex; flex-direction: column-reverse;")

    ui.run(port=8080) # nicegui server <- http://localhost:8080

if __name__ in {"__main__", "__mp_main__"}:
    main()
