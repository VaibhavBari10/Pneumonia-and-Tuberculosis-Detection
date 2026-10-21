# Pneumonia and Tuberculosis Detection Using Deep Learning

A Python-based web application that uses deep learning and chest X-ray images to classify possible pneumonia and tuberculosis cases. The project combines a Flask web interface, TensorFlow/Keras image-classification models, and a MySQL database for user accounts and prediction history.

> **Medical disclaimer:** This project is for educational and research purposes only. It is not a medical device and must not be used as a substitute for professional diagnosis, medical advice, or treatment. Always consult a qualified healthcare professional.

## Project Overview

The application is designed to let users upload chest X-ray images and view model-generated classification results. The code includes separate prediction flows for pneumonia and tuberculosis, user registration/login, and a history page for previously submitted images.

## Features

- **Chest X-ray classification:** Predicts a class from an uploaded image using a trained TensorFlow/Keras model.
- **Pneumonia prediction:** Processes an X-ray image and returns a `NORMAL` or `PNEUMONIA` class.
- **Tuberculosis prediction:** Includes a separate prediction flow for tuberculosis classification.
- **Web interface:** Built with Flask and HTML templates.
- **User accounts:** Registration, login, logout, and session handling.
- **Prediction history:** Stores uploaded image paths, prediction results, and timestamps in MySQL.
- **Dataset upload interface:** Includes a page for uploading a ZIP dataset. The current `start_training()` function is a simulation and does not train a model.

## Technology Stack

- **Python 3.10**
- **Flask** — web application and routes
- **TensorFlow / Keras** — deep-learning model loading and inference
- **OpenCV** — image reading, color conversion, and resizing
- **NumPy** — numerical processing
- **MySQL** — user and prediction-history storage
- **Flask-MySQLdb / mysqlclient** — Flask-to-MySQL connection
- **HTML templates** — web pages rendered by Flask

## Repository Structure

The repository contains a project directory and supporting files. The main application and its dependencies are located under `project_tb_pneumonia/`.

```text
Pneumonia-and-Tuberculosis-Detection/
├── project_tb_pneumonia/
│   ├── app.py                    # Flask routes and prediction logic
│   ├── requirements.txt          # Python dependencies
│   ├── install_steps.txt         # Setup notes
│   ├── pneumonia_model.h5        # Saved model (if included locally)
│   ├── pneumonia_model_alex.h5   # Saved model (if included locally)
│   ├── pneumonia.ipynb           # Notebook for experiments
│   ├── output.csv                # Project output data
│   ├── tube.sql                  # Database-related SQL file
│   └── ...                       # Other templates, assets, and project files
├── Dataset/                      # Dataset directory
├── project report/               # Project reports
├── folder_structure.txt          # Recorded project tree
└── README.md
```

Some model, dataset, and template files may be provided separately or may be present only in a local copy. Confirm that the required files exist before running the application.

## Dataset and Model Files

- **Dataset:** https://www.kaggle.com/datasets/vaibhavsantoshbari/pneumonia-and-tuberculosis-datasets?select=Dataset
- **Model files:** [Download models from Google Drive](https://drive.google.com/drive/folders/17SHBMbyQKfA1UaapepB4-rTp7AW0NnrB?usp=drive_link)

Place model files in the location expected by `app.py`, or update the model paths in the code. The application currently refers to model files such as `pneumonia_model_alex.h5` and `64x3-CNN.model`; ensure all required models are available before starting the server.

## Prerequisites

- Windows is the environment described in the included installation notes.
- Python 3.10.x (the original setup notes specify Python 3.10.8).
- MySQL Server or XAMPP with MySQL/MariaDB enabled.
- The project database and tables configured before using account and history features.
- The required HTML templates, static assets, dataset/model files, and Python packages.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/VaibhavBari10/Pneumonia-and-Tuberculosis-Detection.git
cd Pneumonia-and-Tuberculosis-Detection/project_tb_pneumonia
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it in Windows Command Prompt:

```bat
venv\Scripts\activate
```

Or in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The repository's pinned dependencies include TensorFlow 2.15.0, NumPy 1.26.4, Flask, OpenCV, and MySQL-related packages. If installation fails, verify your Python version and platform compatibility, particularly for `mysqlclient` and TensorFlow.

### 4. Configure MySQL

1. Start MySQL through your local MySQL installation or XAMPP.
2. Create the database and tables expected by the application.
3. Review `tube.sql` and the SQL statements in `app.py` to confirm the expected database schema.
4. Configure database settings using environment variables or a local configuration file rather than committing passwords to source control.

The current code expects a database named `tube` on `localhost`. Update the configuration to match your local setup.

### 5. Check required files

Before launching, verify that:
- The HTML templates referenced by `render_template()` are available in the expected `templates/` directory.
- The model files referenced by `app.py` exist at their configured paths.
- The upload directory (for example, `static/uploads/`) exists and is writable.
- The MySQL tables for users and prediction history are created.

### 6. Run the application

From the `project_tb_pneumonia` directory, run:

```bash
python app.py
```

If the Flask development server is configured through the Flask CLI, you can alternatively use the following in Windows Command Prompt:

```bat
set FLASK_APP=app.py
flask run
```

Then open the local URL printed in the terminal, usually `http://127.0.0.1:5000`.

## How to Use

1. Start the web application and open it in your browser.
2. Register an account and log in if required.
3. Navigate to the relevant pneumonia or tuberculosis upload page.
4. Upload a supported chest X-ray image. The current code accepts PNG files for the tuberculosis route and PNG/JPG/JPEG files for the pneumonia route.
5. Review the predicted class and model score shown by the application.
6. Open the history page to view previously stored prediction records.

Prediction scores are model outputs, not validated clinical probabilities. Results can be wrong, especially for images that differ from the training data.

## Important Implementation Notes

- The current application code contains more than one model-loading and prediction path. Check the configured model filenames and class labels before relying on the output.
- The `/train` route currently calls a simulated training function that returns a fixed example score; it does not perform actual model training.
- The code expects a MySQL database and specific tables for account and history features. Database setup is required for those routes.
- The application uses a development-style Flask configuration. It should not be deployed publicly without security, privacy, and production-readiness improvements.

## Security and Privacy

Before running this project with real users or sensitive medical images:

- Replace the hard-coded Flask secret key with a secure environment variable.
- Never store plain-text passwords; use a strong password-hashing method.
- Configure database credentials securely and use a database account with limited permissions.
- Validate and safely rename uploaded files, restrict upload sizes, and check file contents rather than relying only on extensions.
- Add authentication and authorization checks to protected routes.
- Do not expose real patient data, credentials, or private datasets in a public repository.
- Use a production WSGI server and HTTPS for any legitimate deployment.

## Troubleshooting

| Issue | What to check |
|---|---|
| `ModuleNotFoundError` | Activate the virtual environment and install `requirements.txt`. |
| TensorFlow or NumPy installation fails | Use a compatible Python 3.10 environment and check platform support for the pinned versions. |
| MySQL connection error | Confirm the database service is running and credentials/database settings are correct. |
| Table does not exist | Review `tube.sql` and the SQL statements in `app.py`; create the expected schema. |
| Model file not found | Download the model files and place them at the paths expected by the application. |
| Template not found | Confirm that the HTML files exist in the Flask `templates/` directory. |
| Upload fails | Check the accepted image extensions and ensure the upload directory exists and is writable. |
| Prediction looks incorrect | Confirm the model's expected input size, preprocessing, class order, and training dataset. Do not use the output for clinical decisions. |

## Future Improvements

- Unify the pneumonia and tuberculosis prediction pipelines and model configuration.
- Add a reproducible training and evaluation workflow with documented metrics.
- Validate uploaded image content and handle corrupt or unsupported files safely.
- Improve authentication, password storage, session security, and database configuration.
- Add automated tests and a clear deployment guide.
- Document dataset provenance, licensing, class balance, model limitations, and evaluation methodology.

## Author

**Vaibhav Bari**

- GitHub: [VaibhavBari10](https://github.com/VaibhavBari10)

## Dataset Link -- https://www.kaggle.com/datasets/vaibhavsantoshbari/pneumonia-and-tuberculosis-datasets

## Models Link -- https://drive.google.com/drive/folders/17SHBMbyQKfA1UaapepB4-rTp7AW0NnrB?usp=drive_link

## License

No license could be verified from the repository information reviewed for this README. Add a `LICENSE` file if you intend to publish the project under a specific open-source license.
