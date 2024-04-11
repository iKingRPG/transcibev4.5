# transcibev4.5
Transcribes .mp3s
It imports necessary modules: os for interacting with the operating system, subprocess for running external commands (like FFmpeg), openai for accessing the OpenAI API, logging for logging messages, and tkinter for creating a simple GUI.

It defines a function get_config() which creates a GUI window using Tkinter to prompt the user to select an input audio file and an output directory. It then returns a dictionary containing the configuration details.

It defines a function split_audio(config) which uses FFmpeg to split the input audio file into segments of approximately 20 MB each. It saves the segments in the output directory specified in the configuration.

It defines a function transcribe_segments(config) which transcribes each segment using the OpenAI Audio API. It loops through each file in the output directory, transcribes the audio, and saves the transcription as a text file with the same name as the audio file.

It defines the main() function which orchestrates the execution of the script. It gets the configuration details, splits the audio file into segments, transcribes each segment, and logs the success and failure counts.

Finally, it checks if the script is being run directly (__name__ == "__main__") and if so, it calls the main() function to start the transcription process.
