YouTube Video Summarizer and Translator
This application allows users to enter a YouTube URL, fetches the video's transcript, summarizes the content, and provides an option to translate the summary into a specified language.

Prerequisites
Python 3.6 or higher
pip and virtualenv
Setup and Installation
Clone the repository:

bash
Copy code
git clone https://your-repository-url
cd your-project-directory
Create and activate a virtual environment:

Windows:

Copy code
python -m venv venv
venv\Scripts\activate
macOS/Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install the requirements:

Copy code
pip install -r requirements.txt
Running the Application
Once the setup is complete, you can start the application using:

bash
Copy code
python app.py
Using the Application
Enter a YouTube URL in the text field.
Click Summarize to get a summary of the video.
To translate, enter an ISO language code (e.g., 'hi' for Hindi) and click Translate.
 
