import queue
import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


class ChatClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("720x620")
        self.root.minsize(560, 500)
        self.root.configure(bg="#F3F5FB")

        self.sock = None
        self.connected = False
        self.incoming = queue.Queue()

        self.name_var = tk.StringVar(value="Guest")
        self.host_var = tk.StringVar(value=DEFAULT_HOST)
        self.message_var = tk.StringVar()

        self.build_ui()
        self.root.after(100, self.process_incoming)
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_ui(self):
        header = tk.Frame(self.root, bg="#F3F5FB")
        header.pack(fill="x", padx=24, pady=(20, 14))

        tk.Label(header, text="PYTHON NETWORKING PROJECT",
                 font=("Segoe UI", 9, "bold"), fg="#6558D3",
                 bg="#F3F5FB").pack(anchor="w")
        tk.Label(header, text="Chat Application",
                 font=("Segoe UI", 25, "bold"), fg="#20243A",
                 bg="#F3F5FB").pack(anchor="w", pady=(4, 2))
        tk.Label(header, text="Connect to a server and chat in real time.",
                 font=("Segoe UI", 10), fg="#737A91",
                 bg="#F3F5FB").pack(anchor="w")

        connection = tk.Frame(self.root, bg="white",
                              highlightbackground="#E2E6F0",
                              highlightthickness=1)
        connection.pack(fill="x", padx=24, pady=(0, 12))

        tk.Label(connection, text="Display name", bg="white", fg="#20243A",
                 font=("Segoe UI", 9, "bold")).grid(
                     row=0, column=0, sticky="w", padx=(14, 6), pady=(12, 4))
        self.name_entry = tk.Entry(connection, textvariable=self.name_var,
                                   font=("Segoe UI", 10), width=16)
        self.name_entry.grid(row=1, column=0, sticky="ew", padx=(14, 8), pady=(0, 12))

        tk.Label(connection, text="Server IP", bg="white", fg="#20243A",
                 font=("Segoe UI", 9, "bold")).grid(
                     row=0, column=1, sticky="w", padx=6, pady=(12, 4))
        self.host_entry = tk.Entry(connection, textvariable=self.host_var,
                                   font=("Segoe UI", 10), width=18)
        self.host_entry.grid(row=1, column=1, sticky="ew", padx=6, pady=(0, 12))

        self.connect_button = tk.Button(
            connection, text="Connect", command=self.connect,
            font=("Segoe UI", 10, "bold"), bg="#6558D3", fg="white",
            activebackground="#5145B8", activeforeground="white",
            relief="flat", cursor="hand2", padx=16, pady=7
        )
        self.connect_button.grid(row=1, column=2, padx=(8, 14), pady=(0, 12))
        connection.grid_columnconfigure(0, weight=1)
        connection.grid_columnconfigure(1, weight=1)

        chat_card = tk.Frame(self.root, bg="white",
                             highlightbackground="#E2E6F0",
                             highlightthickness=1)
        chat_card.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        top_line = tk.Frame(chat_card, bg="white")
        top_line.pack(fill="x", padx=14, pady=(12, 8))
        tk.Label(top_line, text="Messages", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#20243A").pack(side="left")
        self.status_label = tk.Label(top_line, text="● Disconnected",
                                     font=("Segoe UI", 9), bg="white",
                                     fg="#B45353")
        self.status_label.pack(side="right")

        self.chat_area = scrolledtext.ScrolledText(
            chat_card, wrap=tk.WORD, state="disabled",
            font=("Segoe UI", 10), bg="#FAFBFE", fg="#20243A",
            relief="flat", padx=12, pady=10
        )
        self.chat_area.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        composer = tk.Frame(chat_card, bg="white")
        composer.pack(fill="x", padx=14, pady=(0, 14))
        self.message_entry = tk.Entry(
            composer, textvariable=self.message_var, font=("Segoe UI", 10),
            state="disabled", relief="solid", bd=1
        )
        self.message_entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(
            composer, text="Send", command=self.send_message,
            font=("Segoe UI", 10, "bold"), bg="#6558D3", fg="white",
            activebackground="#5145B8", activeforeground="white",
            relief="flat", cursor="hand2", padx=18, pady=9, state="disabled"
        )
        self.send_button.pack(side="left", padx=(8, 0))

        tk.Label(
            self.root,
            text="Tip: run server.py first. For another computer, enter the server computer's local IP.",
            font=("Segoe UI", 8), fg="#737A91", bg="#F3F5FB"
        ).pack(pady=(0, 12))

    def append_message(self, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.configure(state="disabled")

    def connect(self):
        if self.connected:
            return

        username = self.name_var.get().strip()
        host = self.host_var.get().strip()

        if not username:
            messagebox.showerror("Missing name", "Please enter a display name.")
            return
        if not host:
            messagebox.showerror("Missing server IP", "Please enter a server IP address.")
            return

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)
            client.connect((host, DEFAULT_PORT))
            client.settimeout(None)
            client.sendall((username[:24] + "\n").encode("utf-8"))
        except (OSError, UnicodeError) as exc:
            try:
                client.close()
            except (UnboundLocalError, OSError):
                pass
            messagebox.showerror(
                "Connection failed",
                f"Could not connect to {host}:{DEFAULT_PORT}.\n"
                "Make sure the server is running and the IP address is correct.\n\n"
                f"Details: {exc}"
            )
            return

        self.sock = client
        self.connected = True
        self.connect_button.configure(text="Connected", state="disabled")
        self.name_entry.configure(state="disabled")
        self.host_entry.configure(state="disabled")
        self.message_entry.configure(state="normal")
        self.send_button.configure(state="normal")
        self.status_label.configure(text="● Connected", fg="#21865B")
        self.append_message(f"[You joined as {username[:24]}]")
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.message_entry.focus_set()

    def receive_messages(self):
        buffer = ""
        try:
            while self.connected and self.sock:
                data = self.sock.recv(4096)
                if not data:
                    break
                buffer += data.decode("utf-8", errors="replace")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line:
                        self.incoming.put(line)
        except OSError:
            pass
        finally:
            self.incoming.put("[Server] Connection closed.")
            self.incoming.put("__DISCONNECTED__")

    def process_incoming(self):
        try:
            while True:
                message = self.incoming.get_nowait()
                if message == "__DISCONNECTED__":
                    self.set_disconnected()
                else:
                    self.append_message(message)
        except queue.Empty:
            pass
        self.root.after(100, self.process_incoming)

    def send_message(self):
        message = self.message_var.get().strip()
        if not message or not self.connected or not self.sock:
            return
        try:
            self.sock.sendall((message + "\n").encode("utf-8"))
            self.message_var.set("")
        except OSError:
            self.append_message("[Error] Message could not be sent.")
            self.set_disconnected()

    def set_disconnected(self):
        if not self.connected:
            return
        self.connected = False
        self.status_label.configure(text="● Disconnected", fg="#B45353")
        self.connect_button.configure(text="Connect", state="normal")
        self.name_entry.configure(state="normal")
        self.host_entry.configure(state="normal")
        self.message_entry.configure(state="disabled")
        self.send_button.configure(state="disabled")
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None

    def close_app(self):
        if self.connected and self.sock:
            try:
                self.sock.sendall(b"/quit\n")
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.sock.close()
            except OSError:
                pass
        self.connected = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientApp(root)
    root.mainloop()
