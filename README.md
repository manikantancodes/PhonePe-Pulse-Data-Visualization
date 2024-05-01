# PhonePe Data Visualization and Exploration

This project aims to visualize and explore data related to PhonePe, India's leading digital payment platform. It utilizes Streamlit, a Python library for building interactive web applications, to create an intuitive user interface for data exploration and analysis.

## Features

- Visualize transaction data (amount and count) at different levels (state, district, and pincode)
- Analyze user data (registered users and app opens)
- Explore insurance-related transactions
- Generate interactive charts and maps for better understanding of data

## Prerequisites

- Python
- PostgreSQL (with the appropriate database and tables set up)

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Create a virtual environment (optional but recommended).
4. Install the required Python packages.
5. Set up the PostgreSQL database and tables by running the SQL script available in the `data` directory.
6. Update the database connection details in `phonepe/phonepe.py` with your PostgreSQL credentials.

## Usage

To run the Streamlit app, use the following command from the project root directory.
streamlit run phonepe.py

This will launch the Streamlit app in your default web browser. You can then interact with the app by selecting different options and visualizations.

## Project Structure
- `data/`: Contains the SQL script for creating the database tables and sample data (if any).
- `phonepe/`: The Python package containing the main application code.
  - `__init__.py`: Package initialization file.
  - `phonepe.py`: The main Streamlit app file.
- `README.md`: This file, containing project information and instructions.
- `requirements.txt`: List of required Python packages and their versions.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the Creative Commons Licenses.


   
