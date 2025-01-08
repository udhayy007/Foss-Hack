# Smart Resume AI 📄

An intelligent resume analyzer and builder powered by AI, designed to help you create and optimize your resume for different job roles.

## Features 🚀

- **Resume Analysis**
  - ATS Compatibility Score
  - Keyword Analysis
  - Role-specific Suggestions
  - Skills Gap Analysis

- **Resume Builder**
  - Professional Templates
  - Role-optimized Content
  - ATS-friendly Formatting
  - Custom Sections

- **AI-powered Optimization**
  - Smart Keyword Suggestions
  - Industry-specific Recommendations
  - Content Enhancement Tips
  - Format Optimization

## Setup Instructions 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-resume-ai.git
cd smart-resume-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage 📝

1. Open your browser and navigate to `http://localhost:8501`
2. Choose between Resume Analysis or Resume Building
3. Follow the intuitive interface to either:
   - Upload and analyze your existing resume
   - Create a new resume using our AI-powered builder

## Technologies Used 💻

- Streamlit
- spaCy
- Python-docx
- PyPDF2
- scikit-learn
- Plotly

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
