import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from proposal_analyzer import ProposalAnalyzer

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize ProposalAnalyzer
proposal_analyzer = ProposalAnalyzer(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_proposal():
    """Handle proposal file upload and analysis."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        # Analyze the proposal using our ProposalAnalyzer
        analysis_result = proposal_analyzer.analyze_proposal(filepath)
        
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Optional: Remove the file after analysis
        os.remove(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
