import tkinter as tk
from tkinter import messagebox
import requests


class VoiceRecorderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Recorder")

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.latest_text_label = tk.Label(master, text="Latest Text: None")
        self.latest_text_label.pack(pady=10)

        self.search_results_label = tk.Label(master, text="Search Results: None", wraplength=400, justify="left")
        self.search_results_label.pack(pady=10)

    def start_recording(self):
        try:
            response = requests.post('http://127.0.0.1:5000/start_recording')
            if response.status_code == 200:
                messagebox.showinfo("Info", response.json().get('status'))
            else:
                messagebox.showerror("Error", "Failed to start recording")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_recording(self):
        try:
            response = requests.post('http://127.0.0.1:5000/stop_recording')
            if response.status_code == 200:
                messagebox.showinfo("Info", response.json().get('status'))
                self.get_latest_text()
            else:
                messagebox.showerror("Error", "Failed to stop recording")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_latest_text(self):
        try:
            response = requests.get('http://127.0.0.1:5000/latest_text')
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    self.latest_text_label.config(text="Latest Text: " + data['error'])
                else:
                    self.latest_text_label.config(text="Latest Text: " + data['latest_text'])
                    self.search_results_label.config(text="Search Results:\n" + data['results'])
            else:
                messagebox.showerror("Error", "Failed to get latest text")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderGUI(root)
    root.mainloop()
