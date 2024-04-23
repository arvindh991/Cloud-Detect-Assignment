# Cloud Detect

## Setup
Pre-requisites: VS Code (with the Python and Jupyter extensions), Docker, and Git.


### Development (outside a container)
1. Install mamba / micromamba ([see here](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) for instructions)
2. Create the enviroment
   ```
   mamba env create -f environment.yaml
   ```
3. Activate the environment
   ```
   mamba activate flask
   ```
4. Run the app
   ```
   python app.py
   ```
   Access the webpage on http://127.0.0.1:5000/  
   Test by going to http://127.0.0.1:5000/hello

### Production (with the container)
1. Build the container
   ```
   docker build --tag cloud-detect .
   ```
2. Run the container
   ```
   docker run -p 5000:5000 cloud-detect
   ```
   Access the webpage on http://127.0.0.1:5000/  
   Test by going to http://127.0.0.1:5000/hello


## Testing
Once you have the development environment setup and the server running, you can test the app in one of two ways. 

### Jupyter Notebook
1. Setup the development environment (as mentioned above).
2. Activate the environment
   ```mamba activate flask```
3. In VSCode open up and run the `notebooks/02_requests_01.ipynb` file.

### Locust
1. Setup the development environment (as mentioned above).
2. Activate the environment
   ```mamba activate flask```
3. Run Locust:
   ```  
   cd tests/locust
   locust
   ```
   Then go to the URL you see and run tests.