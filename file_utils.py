import os
import subprocess

DATA_PATH = "data"

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

def handle_upload(event, upload_label):
    uploaded_file = event
    result = save_uploaded_file(uploaded_file)
    upload_label.set_text(result)
