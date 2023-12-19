import time
import threading
import os
import dotenv

from fren.listen import listen_for_a_sentence, speak

from pathlib import Path
HERE = Path(__file__).parent


################################
def check_env():
    if os.getenv("OPENAI_API_KEY", None) is None:
        return False

    if os.getenv("ASSEMBLYAI_API_KEY", None) is None:
        return False
    
    return True


#################################
def main():
    print("Looking in:", HERE.parent / ".env")
    dotenv.load_dotenv(HERE.parent / ".env")

    if not check_env():
        print("ENV vars not set in .env")
        exit(1)

    os.system(f"afplay {HERE / 'ready.mp3'}")

    # thread = threading.Thread(target=listen_for_a_sentence)
    # thread.start()
    input("\n\nPress Enter to speak...")

    try:
        while True:
            while threading.active_count() > 1:
                print("Waiting for previous thread to finish...")
                time.sleep(0.1)

            text = listen_for_a_sentence()
            thread = speak(text)

            input("\n\nPress Enter to speak...")
            if thread.is_alive():
                thread.join(0.01)

    except KeyboardInterrupt:
        print("Exiting ... bye fren!")
        os.system(f"afplay {HERE / 'goodbye.mp3'}")
        exit(0)
