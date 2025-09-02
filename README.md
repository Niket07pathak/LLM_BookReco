# 📚 LLM Book Recommendation System

An end-to-end **Book Recommendation System** powered by **Large Language Models (LLMs)**, **sentiment analysis**, and a **Qdrant vector database**.  
This project processes book metadata, classifies them into categories, analyzes sentiments from descriptions, and serves personalized recommendations through a **Flask web application**.

---

## 🚀 Features
- Uses an open-source Kaggle dataset of ~7,000 books  
- Classifies books as *Fiction* or *Nonfiction* using zero-shot classification  
- Performs sentiment analysis on book descriptions across multiple emotions  
- Stores vector embeddings in **Qdrant** for efficient similarity-based recommendations  
- Provides an interactive **Flask web application** for querying and receiving book recommendations  

---

## 📂 Dataset Preparation
- Load and clean the Kaggle books dataset (~7k books)  
- Perform analysis and manipulation of data including book titles, authors, and descriptions  
- Prepare processed data for classification, sentiment analysis, and embedding generation  

---

## 🧠 Book Classification
- Utilizes a zero-shot classification pipeline to categorize books into *Fiction* or *Nonfiction*  
- Enables flexible classification without requiring a task-specific dataset  

---

## 🎭 Sentiment Analysis
- Applies an emotion-based sentiment analysis model to evaluate book descriptions  
- Generates probability scores across seven emotions: *anger, disgust, fear, joy, neutral, sadness, surprise*  
- Enhances book metadata with emotional context for better recommendations  

---

## 🔎 Vector Database with Qdrant
- Converts book descriptions into dense embeddings using **Sentence Transformers**  
- Stores embeddings in a **Qdrant vector database** for scalable similarity search  
- Enables retrieval of semantically relevant books based on user queries  

---

## 🌐 Flask Web Application
- Built with **Flask (backend)** and **HTML/CSS (frontend)**  
- Users enter queries through a web interface  
- Fetches recommendations from Qdrant and displays them with classification labels and sentiment scores  

---

## ⚙️ Installation & Setup
1. Clone the repository and install dependencies from `requirements.txt`  
2. Configure environment variables for Qdrant connection (URL, API key, and collection name)  
3. Run the Flask server to start the application  

---

## 📊 Tech Stack
- **Python**: Data processing, model integration, and backend  
- **Hugging Face Transformers**: Zero-shot classification and sentiment analysis  
- **Sentence Transformers**: Embedding generation  
- **Qdrant**: Vector database for similarity search  
- **Flask**: Web application framework (with HTML/CSS frontend)  

---

## 🙌 Acknowledgments
- **Dataset**: Kaggle *7k Books Dataset*  
- **Models**: Hugging Face Transformers  
- **Database**: Qdrant Vector Search Engine  
