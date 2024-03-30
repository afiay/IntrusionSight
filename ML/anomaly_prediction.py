import logging
import os
import subprocess
import threading
from tkinter import messagebox, Tk, Label, Button, ttk, Scrollbar
from datetime import datetime
from joblib import load
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import struct
import numpy as np
import ipaddress
from anomaly_detection import predict_anomaly, load_model

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class DatabaseWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if 'users.db' in event.src_path:
            logging.info("Database has been updated. Retraining model...")
            train_model()
            global loaded_model
            loaded_model = load('saved_model.pkl')
            logging.info("Model reloaded.")


def train_model():
    logging.info("Starting model training...")
    subprocess.run(['python', 'model_training.py'], check=True)
    logging.info("Model training completed.")


model_path = 'saved_model.pkl'
if os.path.exists(model_path):
    loaded_model = load(model_path)
else:
    train_model()
    loaded_model = load(model_path)

observer = Observer()
observer.schedule(DatabaseWatcher(), path='../', recursive=False)
observer.start()

root = Tk()
root.title("Anomaly Detection")

# Treeview Setup
treeview = ttk.Treeview(root, columns=('Index', 'Time', 'IP',
                        'DNS', 'Requests', 'Anomaly', 'Port'), show='headings')
for col in treeview['columns']:
    treeview.heading(col, text=col)
    treeview.column(col, width=100, anchor='center')
treeview.pack(fill='both', expand=True)

# Scrollbar for Treeview
scrollbar = Scrollbar(root, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbar.set)


def update_gui_with_prediction(index, ip, dns, requests, prediction, network):
    logging.info(f"Updating GUI with prediction for IP {ip}.")
    treeview.insert('', 'end', values=(
        index,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ip, dns, requests,
        'Anomaly detected' if prediction == -1 else 'Normal',
        network
    ))


processed_ips = set()  # Keep track of processed IPs to avoid duplicates
new_features = []  # Initialize new_features as an empty list


def test_predict_anomaly():
    logging.info("test_predict_anomaly called")
    global processed_ips, new_features

    if not new_features:  # Ensure there's at least one feature set available
        logging.info("No new features available for prediction.")
        return

    features = new_features[-1]  # Get the most recent set of features

    try:
        # Assuming features[0] is the integer representation of the IP
        ip_int = features[0]
        ip_str = socket.inet_ntoa(struct.pack('!I', ip_int))
    except struct.error as e:
        messagebox.showerror("Error", f"IP address conversion failed: {e}")
        logging.error(f"IP address conversion failed: {e}")
        return

    if ip_str in processed_ips:
        logging.info(f"IP {ip_str} has already been processed.")
        return

    processed_ips.add(ip_str)

    # Attempt DNS lookup
    dns_name = 'DNS not found'
    try:
        dns_name = socket.gethostbyaddr(ip_str)[0]
    except socket.herror:
        logging.info(f"No DNS entry found for IP {ip_str}.")

    try:
        # Example indices, adjust as necessary
        numeric_features = [features[1], features[3]]
        result = predict_anomaly(numeric_features, loaded_model)
        logging.info(f"Anomaly prediction made for IP {ip_str}: {
                     'Anomaly detected' if result == -1 else 'Normal'}")

        # Only update GUI if an anomaly is detected
        if result == -1:
            # Assuming the port information is at this index
            port = features[2]
            update_gui_with_prediction(
                len(processed_ips), ip_str, dns_name, features[1], result, port)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during anomaly prediction: {e}")

def generate_ip():
    octets = np.random.randint(0, 256, 4)
    return '.'.join(str(octet) for octet in octets)


def refresh_data():
    logging.info("refresh_data called")
    new_ip_str = generate_ip()
    new_ip = int(ipaddress.IPv4Address(new_ip_str))
    new_requests = np.random.randint(1, 1000)
    # Randomly generating a port for the example
    port = np.random.randint(1024, 65536)
    time_delta = 10  # Example value
    avg_time_delta = 15  # Example value
    avg_requests = 500  # Example value
    # Appending port instead of network
    new_features.append([new_ip, new_requests, port,
                        time_delta, avg_time_delta, avg_requests])
    test_predict_anomaly()

def periodic_predict():
    refresh_data()
    root.after(5000, periodic_predict)


root.after(0, periodic_predict)


def on_closing():
    observer.stop()
    observer.join()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
