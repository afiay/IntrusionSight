from tkinter import ttk
from database import insert_network_traffic  # Make sure to import this function
from datetime import datetime
import tkinter as tk
from threading import Thread
import queue
from scapy.all import sniff, IP, TCP, UDP, Raw
import requests
from database import insert_network_traffic

# Define a queue for thread-safe GUI updates
update_queue = queue.Queue()

# Initialize the main application window
app = tk.Tk()
app.title("Network Traffic Monitor")

# Define global variables for the entry, label widgets, and packet listbox
username_entry = None
password_entry = None
response_label = None
packet_listbox = None


def submit_login(username_entry, password_entry, response_label, show_welcome_callback):
    # Placeholder for your login logic
    username = username_entry.get()
    password = password_entry.get()
    # Here, you should implement your actual login logic
    print(f"Logging in with username: {username} and password: {password}")
    # Update the response_label with the result or next steps
    response_label.config(text="Login successful! Redirecting...")
    # Call the welcome page or appropriate next step
    show_welcome_callback()


def submit_create_account(username_entry, password_entry, response_label):
    # Placeholder for your account creation logic
    username = username_entry.get()
    password = password_entry.get()
    print(f"Creating account for username: {username}")
    response_label.config(text="Account created successfully!")


def process_packet(packet):
    if IP in packet:
        # Basic packet info
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet.sprintf('%IP.proto%')

        # Initialize default values
        src_port = dst_port = checksum = length = 'N/A'
        flags = 'None'  # Default value for flags
        payload = 'No Payload'

        # Check for TCP or UDP layers and extract relevant information
        if TCP in packet or UDP in packet:
            src_port = packet.sport
            dst_port = packet.dport
            checksum = packet.chksum
            length = packet.len
            if TCP in packet:
                flags = packet[TCP].sprintf('%TCP.flags%')

            # Extract payload
            payload = packet[Raw].load if packet.haslayer(
                Raw) else 'No Payload'

            # Check if payload is bytes and decode if necessary
            if isinstance(payload, bytes):
                payload = payload.decode(errors='ignore')[
                    :50]  # Decode and truncate
            else:
                payload = payload[:50]  # Truncate if it's already a str

        # Additional IP layer fields
        ttl = packet[IP].ttl
        ihl = packet[IP].ihl
        tos = packet[IP].tos

        # Placeholder for ML model's prediction
        label = 'normal'

        # Current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Assemble packet data into a dictionary
        data = {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": proto,
            "src_port": src_port,
            "dst_port": dst_port,
            "packet_length": length,
            "flags": flags,
            "checksum": checksum,
            "ttl": ttl,
            "ihl": ihl,
            "tos": tos,
            "payload": payload,
            "timestamp": timestamp,
            "label": label
        }

        # Database function call simplified using the data dictionary
        insert_network_traffic(data)

        # Prepare and queue packet info for GUI update
        packet_info = f"{timestamp}: IP: {src_ip} -> {dst_ip}, Proto: {proto}, " \
            f"Ports: {src_port} -> {dst_port}, Flags: {flags}, Checksum: {checksum}, " \
            f"Length: {length}, TTL: {ttl}, IHL: {
                ihl}, TOS: {tos}, Payload: {payload[:30]}..."

        update_queue.put(packet_info)




def setup_main_page():
    global packet_listbox

    for widget in app.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(app)
    main_frame.pack(fill='both', expand=True)

    # Frame for displaying packet information and analysis results
    packet_frame = tk.Frame(main_frame)
    packet_frame.pack(fill='both', expand=True, padx=5, pady=5)

    scroll_bar = tk.Scrollbar(packet_frame)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    packet_listbox = tk.Listbox(
        packet_frame, yscrollcommand=scroll_bar.set, width=100)
    packet_listbox.pack(side=tk.LEFT, fill='both', expand=True)
    scroll_bar.config(command=packet_listbox.yview)

    # Start packet capture in a new thread
    Thread(target=packet_capture, daemon=True).start()

    # Start the GUI update queue processing
    update_gui_from_queue()


def packet_capture():
    sniff(filter="ip", prn=process_packet, store=False)


def update_gui_from_queue():
    while not update_queue.empty():
        packet_info = update_queue.get()
        packet_listbox.insert(tk.END, packet_info)
        packet_listbox.see(tk.END)  # Scroll to the last item
        update_queue.task_done()
    # Schedule this function to be called again after 100ms
    app.after(100, update_gui_from_queue)


status_label = None


def show_welcome_page():
    # Declare as global if you need to access them from outside this function
    global packet_listbox, status_label

    # Clear previous widgets
    for widget in app.winfo_children():
        widget.destroy()

    # Setup the main frame with padding for aesthetics
    main_frame = tk.Frame(app, bg='white', padx=10, pady=10)
    main_frame.pack(fill='both', expand=True)

    # Welcome label with elegant font
    welcome_label = tk.Label(main_frame, text="Network Traffic Monitor",
                             font=('Helvetica', 18, 'bold'), bg='white')
    welcome_label.pack(pady=(10, 20))

    # Frame for packet information with subtle background color and relief
    packet_frame = tk.Frame(main_frame, bg='#f0f0f0', bd=1, relief=tk.GROOVE)
    packet_frame.pack(fill='both', expand=True)

    # Scrollbar for the listbox with a modern style
    packet_scrollbar = ttk.Scrollbar(packet_frame, orient='vertical')
    packet_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Listbox to display packet data with a monospaced font for better readability
    packet_listbox = tk.Listbox(packet_frame, font=('Consolas', 10),
                                yscrollcommand=packet_scrollbar.set, bd=1, relief=tk.FLAT)
    packet_listbox.pack(side=tk.LEFT, fill='both', expand=True)
    packet_scrollbar.config(command=packet_listbox.yview)

    # Barometer-like widget (a Progressbar in indeterminate mode)
    barometer = ttk.Progressbar(main_frame, orient='horizontal',
                                length=200, mode='indeterminate')
    barometer.pack(pady=(10, 0))
    barometer.start(10)  # Starts the animation of the barometer

    # Status label for updates, with a modern look
    status_label = tk.Label(main_frame, text="Ready to capture packets",
                            font=('Helvetica', 10), bg='white', fg='black')
    status_label.pack(pady=(5, 10))

    # Button frame to hold control buttons
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(fill='x', pady=(5, 0))

    # Refresh button to manually update the listbox with the latest data
    refresh_button = tk.Button(button_frame, text="Refresh",
                               command=refresh_packet_list, relief=tk.GROOVE)
    refresh_button.pack(side=tk.RIGHT)

    # Start the packet capture thread
    Thread(target=packet_capture, daemon=True).start()

    # Update routine to run periodically
    app.after(100, update_gui_from_queue)




def refresh_packet_list():
    # Ideally, this function would pull data from your database or source
    # For demonstration, let's pretend it adds a dummy entry to the listbox
    packet_listbox.insert(tk.END, "New packet info...")

    # Update the status label with the new time
    status_label.config(text="Last updated at: " +
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'))




def setup_login_page():
    global username_entry, password_entry, response_label

    for widget in app.winfo_children():
        widget.destroy()

    username_label = tk.Label(app, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(app)
    username_entry.pack(pady=5)

    password_label = tk.Label(app, text="Password:")
    password_label.pack()

    password_entry = tk.Entry(app, show="*")
    password_entry.pack(pady=5)

    response_label = tk.Label(app, text="")
    response_label.pack(pady=5)
    # Button for login action
    login_button = tk.Button(app, text="Login", command=lambda: submit_login(
        username_entry, password_entry, response_label, show_welcome_page))
    login_button.pack(fill='x', pady=5)

    # Button for account creation action
    create_account_button = tk.Button(app, text="Create Account", command=lambda: submit_create_account(
        username_entry, password_entry, response_label))
    create_account_button.pack(fill='x', pady=5)

# Function to handle public IP fetching and sending it to the server


# Call this function at the appropriate place in your code where you want to fetch and send the public IP
# handle_public_ip()
# Initial setup to display the login page
setup_login_page()

# Start the GUI update queue processing
update_gui_from_queue()

# Main loop to run the application
app.mainloop()
