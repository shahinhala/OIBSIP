# Chat Application — Python (Tkinter + Sockets)

A desktop group-chat project for the Oasis Infobyte Python Programming internship. It uses Python sockets for networking, threads to handle multiple clients, and Tkinter for the graphical user interface.

## Features
- Desktop chat window with display name and server IP fields
- Real-time text messaging
- Multiple clients can connect to one server
- Connection status, scrollable message history, and Send button
- Basic input validation and connection error messages
- Uses Python standard-library modules; no pip packages are required

## Project files
- `server.py` — starts the chat server and relays messages
- `client.py` — graphical chat client
- `README.md` — setup and usage instructions

## Requirements
- Python 3
- Tkinter support (usually included with Python on Windows)
- Computers on the same network if chatting across different computers

## Run locally on one computer
1. Extract this folder.
2. Open a terminal in the project folder.
3. Start the server in Terminal 1:

   ```bash
   python server.py
   ```

4. Start a client in Terminal 2:

   ```bash
   python client.py
   ```

5. Start another client by running `python client.py` in a third terminal.
6. In each client, enter a different display name and use server IP `127.0.0.1`, then click **Connect**.

## Connect from another computer on the same Wi-Fi/LAN
1. Run `server.py` on the host computer.
2. Find the host computer's local IPv4 address (on Windows, run `ipconfig` and look for IPv4 Address).
3. In the client on another computer, enter that IPv4 address as the Server IP.
4. Allow Python through the firewall on a trusted private network if Windows asks.
5. Both computers must be able to reach the host on TCP port `5000`.

Do not expose this simple demo server directly to the public internet. It does not use encryption or authentication, and it is intended for learning/demo use on a trusted local network.

## Troubleshooting
- **Connection refused:** Start `server.py` first and check the server IP and port.
- **Port already in use:** Close any other server using port 5000 or change `PORT` in `server.py` and `DEFAULT_PORT` in `client.py` to the same new port.
- **Tkinter missing:** Reinstall Python with Tcl/Tk support enabled.
- **Messages not appearing:** Confirm both clients are connected to the same running server.

## Concepts demonstrated
- TCP sockets and client-server architecture
- Multithreading
- GUI programming with Tkinter
- Input validation and exception handling

## Internship submission checklist
- Run the server and at least two clients to test messaging.
- Capture screenshots showing the working application.
- Keep the source files and README in the folder structure required by your internship instructions.
- Add a `screenshots/` folder if required.
- Follow the exact repository and submission requirements in your orientation/offer email.
