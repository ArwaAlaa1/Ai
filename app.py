from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import pandas as pd
import threading

app = Flask(__name__)

# Load your data into a DataFrame
data = pd.read_csv("data.csv")

class VoiceRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_recording = False
        self.latest_text = ""

    def start_recording(self):
        if not self.is_recording:
            print("Started recording...")
            self.is_recording = True
            threading.Thread(target=self.record_audio).start()

    def stop_recording(self):
        if self.is_recording:
            print("Stopped recording...")
            self.is_recording = False

    def record_audio(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(source, timeout=10)
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print(f"You said: {text}")
                        self.latest_text = text
                    except sr.UnknownValueError:
                        print("Could not understand the audio.")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                except Exception as e:
                    print(f"Error: {e}")

    def search_data(self, query):
        results = data[data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        if not results.empty:
            results_str = results.to_string(index=False)
            return results_str
        else:
            return "No matching results found."

voice_recorder = VoiceRecorder()

@app.route('/start_recording', methods=['POST'])
def start_recording():
    voice_recorder.start_recording()
    return jsonify({'status': 'Recording started'})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    voice_recorder.stop_recording()
    return jsonify({'status': 'Recording stopped'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        results = voice_recorder.search_data(query)
        return jsonify({'results': results})
    return jsonify({'error': 'No query provided'})

@app.route('/latest_text', methods=['GET'])
def latest_text():
    if voice_recorder.latest_text:
        results = voice_recorder.search_data(voice_recorder.latest_text)
        return jsonify({'latest_text': voice_recorder.latest_text, 'results': results})
    return jsonify({'error': 'No latest text available'})

if __name__ == "__main__":
    app.run(debug=True)
