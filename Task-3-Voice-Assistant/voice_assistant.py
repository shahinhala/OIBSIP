import datetime
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox, scrolledtext

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None


BG = "#F3F5FB"
CARD = "#FFFFFF"
TEXT = "#20243A"
MUTED = "#737A91"
ACCENT = "#6558D3"
BORDER = "#E2E6F0"


class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Voice Assistant")
        self.root.geometry("720x650")
        self.root.minsize(560, 540)
        self.root.configure(bg=BG)

        self.command_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.engine = None

        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
            except Exception:
                self.engine = None

        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=26, pady=(22, 16))

        tk.Label(header, text="OIBSIP • PYTHON PROGRAMMING",
                 font=("Segoe UI", 9, "bold"), bg=BG, fg=ACCENT).pack(anchor="w")
        tk.Label(header, text="Voice Assistant",
                 font=("Segoe UI", 26, "bold"), bg=BG, fg=TEXT).pack(anchor="w", pady=(4, 2))
        tk.Label(header, text="Type a command or use your microphone.",
                 font=("Segoe UI", 10), bg=BG, fg=MUTED).pack(anchor="w")

        card = tk.Frame(self.root, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=26, pady=(0, 14))

        bar = tk.Frame(card, bg=CARD)
        bar.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(bar, text="Assistant console", font=("Segoe UI", 12, "bold"),
                 bg=CARD, fg=TEXT).pack(side="left")
        tk.Label(bar, textvariable=self.status_var, font=("Segoe UI", 9),
                 bg=CARD, fg=ACCENT).pack(side="right")

        self.output = scrolledtext.ScrolledText(
            card, wrap=tk.WORD, state="disabled", font=("Segoe UI", 10),
            bg="#FAFBFE", fg=TEXT, relief="flat", padx=12, pady=10
        )
        self.output.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self.add_output("Assistant", "Hello! I'm your Python Voice Assistant.")
        self.add_output("Assistant", "Try: time, date, open YouTube, open Google, search Python, or help.")

        composer = tk.Frame(card, bg=CARD)
        composer.pack(fill="x", padx=16, pady=(0, 16))
        self.command_entry = tk.Entry(
            composer, textvariable=self.command_var, font=("Segoe UI", 10),
            relief="solid", bd=1
        )
        self.command_entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.command_entry.bind("<Return>", lambda event: self.send_typed_command())

        self.send_button = tk.Button(
            composer, text="Run", command=self.send_typed_command,
            font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="white",
            activebackground="#5145B8", activeforeground="white",
            relief="flat", cursor="hand2", padx=16, pady=9
        )
        self.send_button.pack(side="left", padx=(8, 0))

        controls = tk.Frame(self.root, bg=BG)
        controls.pack(fill="x", padx=26, pady=(0, 10))

        self.listen_button = tk.Button(
            controls, text="🎙 Listen", command=self.start_listening,
            font=("Segoe UI", 10, "bold"), bg="#E7E4FF", fg=ACCENT,
            activebackground="#DAD5FF", relief="flat", cursor="hand2",
            padx=16, pady=10
        )
        self.listen_button.pack(side="left")

        tk.Button(
            controls, text="Clear", command=self.clear_output,
            font=("Segoe UI", 10), bg=BG, fg=MUTED, activebackground=BG,
            relief="flat", cursor="hand2", padx=12, pady=10
        ).pack(side="left", padx=(8, 0))

        tk.Label(
            self.root,
            text="Voice input requires a microphone and SpeechRecognition + PyAudio. Typed commands work without them.",
            font=("Segoe UI", 8), bg=BG, fg=MUTED, wraplength=650
        ).pack(padx=20, pady=(0, 12))

    def add_output(self, speaker, message):
        self.output.configure(state="normal")
        self.output.insert(tk.END, f"{speaker}: {message}\n\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def speak(self, text):
        if self.engine is None:
            return
        def worker():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()

    def send_typed_command(self):
        command = self.command_var.get().strip()
        if not command:
            return
        self.command_var.set("")
        self.process_command(command)

    def process_command(self, command):
        self.add_output("You", command)
        normalized = command.lower().strip()

        if normalized in {"help", "commands", "what can you do"}:
            response = (
                "Available commands:\n"
                "• time — tell the current time\n"
                "• date — tell today's date\n"
                "• open Google / open YouTube / open Gmail\n"
                "• search <words> — search the web\n"
                "• help — show this list\n"
                "• exit / quit — close the assistant"
            )
        elif "time" in normalized and len(normalized) < 40:
            response = "The time is " + datetime.datetime.now().strftime("%I:%M %p")
        elif "date" in normalized or "today" in normalized:
            response = "Today's date is " + datetime.datetime.now().strftime("%d %B %Y")
        elif normalized in {"exit", "quit", "close assistant"}:
            response = "Goodbye! Closing the assistant."
            self.add_output("Assistant", response)
            self.speak(response)
            self.root.after(900, self.close_app)
            return
        elif normalized.startswith("open "):
            site = normalized[5:].strip()
            sites = {
                "google": "https://www.google.com",
                "youtube": "https://www.youtube.com",
                "gmail": "https://mail.google.com",
                "wikipedia": "https://www.wikipedia.org",
                "github": "https://github.com",
            }
            if site in sites:
                webbrowser.open(sites[site])
                response = f"Opening {site.title()} in your browser."
            else:
                response = "I don't have that shortcut. Try Google, YouTube, Gmail, Wikipedia, or GitHub."
        elif normalized.startswith("search "):
            query = command[7:].strip()
            if query:
                webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
                response = f"Searching the web for {query}."
            else:
                response = "Please tell me what you want to search for."
        else:
            response = "Sorry, I didn't recognize that command. Type 'help' to see what I can do."

        self.add_output("Assistant", response)
        self.speak(response)

    def start_listening(self):
        if sr is None:
            messagebox.showinfo(
                "Voice input not installed",
                "Typed commands are available now. To enable microphone input, run:\n\n"
                "python -m pip install SpeechRecognition pyaudio\n\n"
                "If PyAudio fails to install on Windows, use typed commands or install a compatible PyAudio wheel."
            )
            return
        self.listen_button.configure(state="disabled", text="Listening...")
        self.status_var.set("Listening…")
        threading.Thread(target=self.listen_worker, daemon=True).start()

    def listen_worker(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            self.root.after(0, lambda: self.status_var.set("Recognizing…"))
            # Google speech recognition requires an internet connection.
            command = recognizer.recognize_google(audio)
            self.root.after(0, lambda c=command: self.process_command(c))
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.add_output("Assistant", "I didn't hear anything. Please try again."))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.add_output("Assistant", "Sorry, I couldn't understand that. Please try again."))
        except sr.RequestError:
            self.root.after(0, lambda: self.add_output("Assistant", "Speech recognition service is unavailable. Check your internet connection."))
        except (OSError, AttributeError) as exc:
            self.root.after(0, lambda error=str(exc): self.add_output("Assistant", f"Microphone error: {error}"))
        finally:
            self.root.after(0, self.finish_listening)

    def finish_listening(self):
        self.listen_button.configure(state="normal", text="🎙 Listen")
        self.status_var.set("Ready")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")

    def close_app(self):
        try:
            if self.engine is not None:
                self.engine.stop()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
