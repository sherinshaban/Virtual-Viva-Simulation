#  VIVASUM: AI-Powered Virtual Viva Simulation

**An AI-oriented platform designed to help students master their graduation project presentations through automated question generation and speech emotion analysis.**

##  Project Overview
Many students face anxiety and uncertainty before their graduation defense. **VIVASUM** leverages Generative AI and Computer Vision to create a realistic simulation environment. It analyzes project documentation to generate contextual questions and provides real-time feedback on the student's speech and delivery.

##  Key Features (AI-Oriented)
* ** Automated Question Generation (Gemini LLM):** * Uses **Google Gemini API** to analyze uploaded Project Documentation (PDF/Docs).
    * Generates defense-style questions (Technical & Theoretical) with reference "Model Answers".
* ** Speech Emotion Recognition (SER):**
    * Custom **CNN Model** trained on the **RAVDESS** dataset.
    * Analyzes audio to detect emotions (Confidence, Nervousness, Calmness) with **90.24% Accuracy**.
* ** Semantic Grading Engine:**
    * Compares student spoken responses against model answers using semantic similarity (not just keywords).

##  Tech Stack
* **AI/LLM:** Google Gemini API (Flash Model).
* **Machine Learning:** TensorFlow/Keras (CNN for Audio Analysis), SpeechRecognition API.
* **Backend:** Python (FastAPI/Flask).
* **Data Processing:** Librosa (Audio Feature Extraction), Pandas.

##  Methodology
1.  **Input:** Student uploads project report & records presentation audio/video.
2.  **Processing:** * **LLM** extracts key concepts to form questions.
    * **CNN** processes Log-Mel Spectrograms from audio to classify emotions.
3.  **Output:** A comprehensive feedback report covering technical accuracy and presentation confidence.


