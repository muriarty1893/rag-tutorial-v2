from datetime import datetime

def log_interaction(user_input, llm_output):
    start_time = datetime.now()
    
    with open("interaction_log.log", "a", encoding="utf-8") as file:
        file.write(f"Date and Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"User Input: {user_input}\n")
        file.write(f"LLM Output: {llm_output}\n")
        file.write("-" * 50 + "\n")
