
# YouTube Video Summarizer

This application allows users to enter a YouTube URL, fetches the video's transcript, summarizes the content, and provides an option to translate the summary into a specified language.

## Prerequisites

- Python 3.6 or higher
- pip and virtualenv

## Setup and Installation

### Clone the repository:

```bash
git clone https://github.com/Err0r789/Youtube-transcript-summarizer.git

cd Youtube-transcript-summarizer
```

### Create and activate a virtual environment:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
macOS/Linux::
```bash
python3 -m venv venv
source venv/bin/activate
```
Install the requirements::
```bash
pip install -r requirements.txt
```
Running the Application:

Once the setup is complete, you can start the application using:
```bash
python Summerizer.py
```

# Using the Application

- Enter a YouTube URL in the text field.

- Click Summarize to get a summary of the video.

- To translate, enter an ISO language code (e.g., 'hi' for Hindi) and click Translate.
