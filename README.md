![Python](https://img.shields.io/badge/python-3.12.2-blue.svg)

# IntrusionSight: Advanced Network Anomaly Detection

**IntrusionSight** is an elegantly crafted anomaly detection system, tailor-made for educational exploration of network security. This application is adept at pinpointing aberrant network patterns that may signal potential security breaches. With its arsenal of state-of-the-art machine learning algorithms, IntrusionSight stands as a vigilant guardian, offering a robust solution for the real-time surveillance and identification of cybersecurity threats, ideal for students and professionals eager to delve into the realm of cybersecurity analytics.

## Core Features

- **Proactive Anomaly Detection**: Harnesses the power of advanced machine learning models to detect and notify users of unusual network activity instantaneously.
- **Streamlined Data Preprocessing**: Comes equipped with scripts that automate the scrubbing and preparation of network traffic data, setting the stage for analysis.
- **Adaptive Model Retraining**: Features an intelligent system that incrementally learns from new data, ensuring the model remains in lockstep with the evolving digital landscape.
- **Intuitive User Interface**: Boasts a clear and navigable graphical user interface, offering immediate insights through alerts and in-depth anomaly analysis.

## Quickstart Guide

Embark on your IntrusionSight journey with these simple setup instructions, designed for both development and experimental use.

### System Prerequisites

Before diving in, make sure your system is equipped with:
- Python (3.6 or newer)
- Pandas
- NumPy
- Scikit-learn
- SQLite3 (for database interactions)

### Installation

Begin by establishing your development environment:

```bash
# Clone the repository to your local machine
git clone [your-repository-url]

# Enter the IntrusionSight directory
cd IntrusionSight

# Install the dependencies from the requirements file
pip install -r requirements.txt
```
### Launching the Application
```bash
# Start the server script to begin data acquisition
python server.py

# In a new terminal, initiate the client script for data visualization
python client.py

# Navigate into the Machine Learning directory to engage the predictive functionalities
cd ML

# Activate the machine learning module to commence anomaly prediction
python anomaly_prediction.py

```
