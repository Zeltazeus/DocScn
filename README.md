# Proposal Analyser Web Application

## Overview
A comprehensive web application designed to analyze various types of proposals including business, sales, marketing, grants, creative, and technical proposals.

## Features
- Multi-format proposal upload (PDF, DOCX, TXT)
- AI-powered proposal analysis
- Detailed insights and recommendations
- User-friendly interface

## Setup and Installation

### Prerequisites
- Python 3.9+
- pip

### Installation Steps
1. Clone the repository
2. Create a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file
5. Run the application
   ```
   flask run
   ```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for advanced analysis
- `SECRET_KEY`: Flask secret key

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
