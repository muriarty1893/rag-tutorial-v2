from datetime import datetime

def log_interaction(user_input, llm_output):
    start_time = datetime.now()
    
    with open("interaction_log.log", "a", encoding="utf-8") as file:
        file.write(f"Tarih ve Saat: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Kullanıcı Girişi: {user_input}\n")
        file.write(f"LLM Çıktısı: {llm_output}\n")
        file.write("-" * 50 + "\n")
