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
# kullancı adı şifre 2FA 
#
# IK cılar için itedikleri özellikleri yazması için alan hangilerini karşıladığımız ve nasıl karşıladığımızı anlatacak 
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

        with ui.row().style('justify-content: center; align-items: center;'):
            with ui.card().classes('center-card'):
                ui.label("Upload PDF File for QNA").style("font-size: 1.5em; font-weight: bold; color: #000000; margin-bottom: 20px;")
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

    ui.run(port=8070)

if __name__ in {"__main__", "__mp_main__"}:
    main()
