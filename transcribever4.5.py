import os
import subprocess
import openai
import logging
import tkinter as tk
from tkinter import filedialog

# Initialize the logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_config():
    """Get configuration from the user using GUI dialogs and return as a dictionary."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Ask the user for the path to the audio file
    input_path = filedialog.askopenfilename(title="Select the audio file you want to transcribe")
    if not input_path:
        logger.error("No audio file selected. Exiting.")
        exit()

    # Ask the user where they'd like to store the transcribed output
    output_dir = filedialog.askdirectory(title="Select the directory where you'd like to store the transcribed output")
    if not output_dir:
        logger.error("No output directory selected. Exiting.")
        exit()
    
    # Configuration based on user input and predefined values
    config = {
        "openai_api_key": "sk-null",
        "input_path": input_path,
        "output_dir": output_dir,
        "temperature": 1,
        "language": "en",
        "ffmpeg_path": "C:/ffmpeg/bin/ffmpeg.exe",
    }
    return config

def split_audio(config):
    """Use FFmpeg to split the input file into 20 MB pieces."""
    try:
        os.makedirs(config["output_dir"], exist_ok=True)
        
        subprocess.run([
            config["ffmpeg_path"], 
            "-i", config["input_path"], 
            "-c", "copy", 
            "-map", "0", 
            "-segment_time", "900", 
            "-segment_format", "mp3", 
            "-segment_list", os.path.join(config["output_dir"], "segments.txt"), 
            "-f", "segment", 
            "-max_size", "20M", 
            os.path.join(config["output_dir"], "output_%03d.mp3")
        ])
        logger.info("Audio split successful.")
    except Exception as e:
        logger.error(f"Error splitting audio: {e}")

def transcribe_segments(config):
    """Transcribe each segment using the OpenAI Audio API."""
    openai.api_key = config["openai_api_key"]
    successes, failures = 0, 0
    
    for file in os.listdir(config["output_dir"]):
        if file.endswith(".mp3"):
            file_path = os.path.join(config["output_dir"], file)
            
            try:
                with open(file_path, "rb") as audio_file:
                    logger.info(f"Transcribing {file_path}")
                    transcription = openai.Audio.transcribe("whisper-1", audio_file, temperature=config["temperature"], language=config["language"])
                
                with open(file_path + ".txt", "w", encoding="utf-8") as text_file:
                    text_file.write(transcription.text)
                    logger.info(f"Transcription saved to {file_path}.txt")
                    successes += 1
            except Exception as e:
                logger.error(f"Error transcribing {file_path}: {e}")
                failures += 1

    return successes, failures

def main():
    config = get_config()
    split_audio(config)
    successes, failures = transcribe_segments(config)
    logger.info(f"Transcription complete. {successes} segments transcribed successfully, {failures} segments failed.")

if __name__ == "__main__":
    main()
