# 🎯 YouTube Comment Analyzer

> An intelligent application that analyzes YouTube video comments to determine sentiment (Positive, Negative, Neutral) and provides actionable feedback to content creators.

---

## 📌 Features

- 🔍 **Sentiment Analysis** of comments using NLP techniques  
- 📈 **Analytics Dashboard** to show sentiment distribution  
- 🧠 **ML Model** trained with 95% accuracy using Multinomial Naive Bayes  
- 💬 **Feedback Generator** that suggests improvements based on comment analysis  
- 📂 Upload and analyze comments via **CSV or live YouTube API (optional)**  
- 📊 Visual insights with bar charts and pie charts

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **ML/NLP**: Scikit-learn, NLTK / SpaCy  
- **Deployment**: Render / Vercel / GCP (optional)  
- **Model**: Multinomial Naive Bayes (accuracy: 95%)

---

## 📦 Installation

```bash
git clone https://github.com/Dharunpandi/Youtube_comments_analyser.git
cd Youtube_comments_analyser
pip install -r requirements.txt
python app.py
