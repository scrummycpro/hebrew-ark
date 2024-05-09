Sure, I've added a section listing the dependencies in the README. Here's the updated version:

---

# Hebrew Studies Command Executor

The Hebrew Studies Command Executor is a Python GUI application designed to execute a specific command using CURL, retrieve JSON data from the Sefaria API, display the results with proper Unicode decoding for Hebrew text, and save the results to a JSON file. Additionally, it saves executed commands along with timestamps and Hebrew topics to a SQLite database for future reference.

## Features

- Execute a predefined CURL command to fetch JSON data from the Sefaria API.
- Display the executed command and the retrieved JSON results.
- Decode Unicode escape sequences in Hebrew text for proper display.
- Save the results as a JSON file with UTF-8 encoding.
- Record executed commands along with timestamps and Hebrew topics to a SQLite database.
- User-friendly GUI with buttons for executing commands and saving results.

## Requirements

- Python 3.x
- Tkinter (should be included in standard Python distribution)
- SQLite3 (should be included in standard Python distribution)

## Installation

1. Clone or download the repository to your local machine:

    ```
    git clone https://github.com/scrummycpro/hebrew-ark.git
    ```

2. Navigate to the project directory:

    ```
    cd hebrew-ark
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Dependencies

The Hebrew Studies Command Executor relies on the following Python packages:

- Tkinter: A standard GUI toolkit for Python.
- SQLite3: A built-in SQLite database module for Python.

## Usage

1. Run the program by executing the `hebrew_studies.py` file:

    ```
    python hebrew_studies_executor.py
    ```

2. Click on the "Execute Command" button to fetch JSON data from the Sefaria API using CURL.

3. The executed command and the retrieved JSON results will be displayed in the GUI. Hebrew text will be properly decoded for display.

4. You can save the results as a JSON file by clicking the "Save as JSON" button. Choose a location and filename for the JSON file and click "Save".

5. The executed command along with the timestamp and Hebrew topic will be recorded in the SQLite database `hebrew_studies.db` for future reference.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The Hebrew Studies Command Executor uses the Sefaria API to fetch JSON data related to Hebrew topics.
- Special thanks to the developers of Tkinter, SQLite, and other libraries used in this project.

---

Feel free to modify and expand upon this README as needed for your project!