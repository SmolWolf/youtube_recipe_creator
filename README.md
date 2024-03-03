# YouTube Recipe Extractor

This Python application utilizes the OpenAI API and YouTube's video subtitles to automatically extract and generate structured recipes from YouTube cooking videos. It's designed to demonstrate the power of combining natural language processing capabilities with accessible video content to simplify recipe documentation.

## Features

- **Automatic Extraction**: Fetches subtitles and descriptions from YouTube videos to source recipe content.
- **AI-Powered Analysis**: Leverages OpenAI's GPT-4 model to interpret and structure the extracted content into a coherent recipe format.
- **Streamlit Interface**: Provides an easy-to-use web interface for users to input YouTube URLs and receive formatted recipes.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.6 or newer
- An OpenAI API key
- Streamlit installed in your Python environment
- The `pytube` library for fetching YouTube video subtitles


## Installation

Before installation, it's recommended to create and activate a virtual environment to avoid conflicts with other Python projects.

- add your OpenAI API key to the .env file: OPENAI_API_KEY=your_openai_api_key_here
- Install required Python packages: pip install -r requirements.txt

## Usage

To run the application, execute the following command in your terminal:

streamlit run main.py

After running the command, Streamlit will start the web application. Open the provided URL in your web browser, paste the YouTube URL you wish to extract the recipe from, and click "Run Assistant".

## Acknowledgments

- OpenAI for the GPT model and API.
- The creators of the `youtube_text_converter` and `dotenv` Python packages.
- This project was inspired by and utilizes content from the following YouTube video: [OpenAI Assistants API – Course for Beginners](https://www.youtube.com/watch?v=qHPonmSX4Ms&pp=ygUTZnJlZWNvZGVjYW1wIG9wZW5haQ%3D%3D).
