![Python](https://img.shields.io/badge/python-3.12.2-blue.svg)

# IntrusionSight: Advanced Network Anomaly Detection

**IntrusionSight**  is an anomaly detection tool for network security, perfect for those who are learning or working in cybersecurity. It quickly identifies unusual network behavior, signaling possible security threats, using machine learning for real-time threat monitoring.


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
git clone https://github.com/afiay/IntrusionSight/tree/main

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
## Saving the Trained Model

Save the trained model to a file only if it doesn't already exist

```python
# Save the trained model to a file only if it doesn't already exist
model_filename = 'saved_model.pkl'
if not os.path.exists(model_filename):
    dump(model, model_filename)
    print(f"Model saved to {model_filename}")
else:
    print(f"Model file {model_filename} already exists. Skipping save.")
```
