from nicegui import ui
from datetime import datetime
from log_utils import log_interaction
from main import query_rag
from main import get_exp_sum
from main import get_proj_sum
import asyncio
import time
import random
import os
import subprocess

DATA_PATH = "data"
file_uploaded = False

def run_reset_command():
    command = "python populate_database.py --reset"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("Komut başarıyla çalıştırıldı!")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Komut çalıştırılırken bir hata oluştu:")
        print(e.stderr)
        return e.stderr

def save_uploaded_file(uploaded_file):
    os.makedirs(DATA_PATH, exist_ok=True)
    file_path = os.path.join(DATA_PATH, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.content.read())
    return f"{uploaded_file.name} has been added to database!"

def handle_upload(event):
    uploaded_file = event
    result = save_uploaded_file(uploaded_file)
    upload_label.set_text(result)

def main():
    async def show_loading_and_execute(task_function, loading_label):
        loading_label.style('visibility: visible;')
        ui.update()
        result = await asyncio.to_thread(task_function)
        loading_label.style('visibility: hidden;')
        ui.update()
        return result

    async def handle_query():
        start_time = time.time()

        user_input = input_box.value
        llm_output = await show_loading_and_execute(lambda: query_rag(user_input), loading_label)
        log_interaction(user_input, llm_output)

        elapsed_time = time.time() - start_time

        with output_column:
            ui.label(f"Query: {user_input}").classes("query-label")
            ui.label(f"Output: {llm_output}").classes("output-label")
            ui.label(f"Logged at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").classes("timestamp-label")
            ui.label(f"Response Time: {elapsed_time:.2f} seconds").classes("response-time-label")
            ui.separator()
        
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
            background-color: #FFFBE9;
            color: #AD8B73;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .center-card, .left-card, .right-card {
            width: 400px;
            max-width: 90%;
            padding: 20px;
            border-radius: 15px;
            background-color: #E3CAA5; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .query-label {
            color: #000000;
            font-weight: bold;
        }
        .output-label {
            color: #000000;
            font-size: 1.1em;
        }
        .timestamp-label {
            font-size: 0.9em;
            color: #000000;
        }
        .response-time-label {
            color: #000000;
            font-weight: bold;
        }
        .separator {
            border-color: #E3CAA5;
        }
        .loading-label {
            font-size: 1.2em;
            font-weight: bold;
            color: #000000;
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

        global upload_label

        with ui.card().classes('left-card'):
            ui.label('Summary of My Experiences:').style("font-size: 1.5em; font-weight: bold; margin-bottom: 20px; color: #000000;")
            experience_loading_label = ui.label('Generating output, please wait...').style('visibility: hidden;').classes("loading-label")
            summary_output1 = ui.column().style("margin-top: 20px; display: flex; flex-direction: column-reverse;")
            async def fetch_and_display_summary1():
                summary1 = await show_loading_and_execute(get_exp_sum, experience_loading_label)
                with summary_output1:
                    ui.label(summary1).style("font-size: 1.2em; color: #000000; margin-bottom: 10px;")
            ui.button('Fetch Summary', on_click=lambda: asyncio.create_task(fetch_and_display_summary1()))

        with ui.card().classes('center-card'):
            ui.label('Ask My Personal AI Guide!').style("font-size: 1.5em; font-weight: bold; margin-bottom: 20px; color: #000000;")
            input_box = ui.input(label='Type your question here, It will answer it. ', placeholder=current_p).style("width: 100%; margin-bottom: 20px;")
            loading_label = ui.label('Generating output, please wait...').style('visibility: hidden;').classes("loading-label")
            with ui.row():
                ui.button('Submit', on_click=lambda: asyncio.create_task(handle_query())).style("margin-right: 10px;")
                ui.button('Reset', on_click=lambda: output_column.clear())
            output_column = ui.column().style("margin-top: 20px; display: flex; flex-direction: column-reverse;")

        with ui.card().classes('right-card'):
            ui.label('Summary of My Projects:').style("font-size: 1.5em; font-weight: bold; margin-bottom: 20px; color: #000000;")
            project_loading_label = ui.label('Generating output, please wait...').style('visibility: hidden;').classes("loading-label")
            summary_output = ui.column().style("margin-top: 20px; display: flex; flex-direction: column-reverse;")
            async def fetch_and_display_summary():
                summary = await show_loading_and_execute(get_proj_sum, project_loading_label)
                with summary_output:
                    ui.label(summary).style("font-size: 1.2em; color: #000000; margin-bottom: 10px;")
            ui.button('Fetch Summary', on_click=lambda: asyncio.create_task(fetch_and_display_summary()))

        with ui.row().style('justify-content: center; align-items: center;'):
            with ui.card().classes('center-card'):
                ui.label("Upload PDF File to Data Folder").style("font-size: 1.5em; font-weight: bold; color: #000000; margin-bottom: 20px;")
                upload_label = ui.label().style("color: green; margin-top: 10px;")
                
                ui.upload(on_upload=handle_upload, label="Select PDF File", multiple=False).style("margin-bottom: 20px;")
                upload_label.set_text("")

                def update_database():
                    if not file_uploaded:
                        upload_label.set_text("⚠️ Please upload a file before updating the database!")
                        return
                    result = run_reset_command()
                    upload_label.set_text("Database Updated!\n" + result)

                ui.button("Update Database", on_click=update_database).style("margin-top: 10px;")

    ui.run(port=8080)

if __name__ in {"__main__", "__mp_main__"}:
    main()
