# 🎬 AI Movie Recommender System

A **Netflix-style Movie Recommendation System** built with **Python, Machine Learning, and Streamlit** — deployed live on Streamlit Cloud.  
This app recommends movies based on content similarity and integrates with TMDB to fetch posters, trailers, and trending movies.

---

## 🚀 Live Demo

👉 **Try the app live here:**  
🔗 https://movierecommenderap.streamlit.app/

---

## ✨ Features

- 📌 Content-based movie recommendations  
- 🎨 Netflix-inspired dark UI  
- 🌟 Trending movies section (powered by TMDB API)  
- 🖼️ Movie posters with fallback handling  
- 🎥 Trailer previews directly inside the app  
- 🔍 Fast similarity search with optimized algorithms  
- 🚀 Deployed on Streamlit Cloud  

---

## 🧠 How It Works

1. Movie metadata is pre-processed into vectors.  
2. Similarity scores are computed using cosine similarity.  
3. Top recommendations are retrieved quickly using optimized search.  
4. TMDB API is used to fetch poster images and trailers for UI enrichment.

---

## 🛠 Tech Stack

- **Python 3**
- **Streamlit** for the web interface
- **NumPy & pandas** for data handling
- **Scikit-learn** for similarity computation
- **TMDB API** for movie metadata, images, and trailers
- **Git LFS** for handling large model artifacts
- **Streamlit Cloud** for deployment

---

## 📁 Project Structure
├── app.py # Main application code
├── movies_dict.pkl # Movie metadata
├── similarity.pkl # Precomputed similarity matrix
├── requirements.txt # Dependencies
├── README.md # Project documentation


> **Note:** The `similarity.pkl` is large and tracked using Git LFS. It may not appear in the GitHub web UI.

---

## 🧠 Key Code Concepts

### 🔹 Fast Recommendation Logic

Only top candidates are considered for API lookup, reducing latency dramatically.  
Similarity computation is done locally using pre-computed vectors.

---


## 🧪 What This Project Demonstrates

✔ Real-world ML system design  
✔ Performance-optimized recommendation logic  
✔ API reliability & fallback handling  
✔ Production deployment mindset  
✔ Clean, readable ML code  

---

## 🎯 Future Improvements

- Collaborative filtering (user-based / item-based)
- Hybrid recommendation engine
- User profiles & personalization
- Approximate Nearest Neighbors (FAISS)
- Model retraining pipeline

---

