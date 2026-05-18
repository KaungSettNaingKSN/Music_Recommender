# 🎵 Music Recommender System

A content-based music recommendation web application built using Python and Streamlit.
The app recommends similar songs by analyzing song lyrics using **TF-IDF Vectorization** and **Cosine Similarity**.

🌐 **Live Demo:**
https://musicrecommenderksn.streamlit.app

---

## 📸 Demo Preview

Try the live application and:

* 🎧 Select any song from the dropdown
* 🔍 Get 5 similar song recommendations
* 🖼️ View album cover art fetched from Spotify

---

## 🚀 Features

* 🎵 Content-based music recommendation system
* 🧠 TF-IDF Vectorization for lyric analysis
* 📊 Cosine Similarity for recommendation scoring
* 🖼️ Spotify API integration for album covers
* ⚡ Fast recommendation loading using Pickle
* 🌐 Interactive UI with Streamlit
* 📱 Simple and responsive design

---

## 🛠️ Tech Stack

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python 3.9+  | Core programming language  |
| Pandas       | Data preprocessing         |
| NLTK         | Text cleaning & stemming   |
| Scikit-learn | TF-IDF & Cosine Similarity |
| Spotipy      | Spotify API integration    |
| Streamlit    | Frontend web application   |
| Pickle       | Model serialization        |

---

## 📂 Project Structure

```bash
Music_Recommender/
│
├── app.py
├── Model_Traning.ipynb
├── df.pkl
├── similarity.pkl
├── requirements.txt
├── README.md
└── spotify_millsongdata.csv
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/KaungSettNaingKSN/Music_Recommender.git
cd Music_Recommender
```

---

### 2️⃣ Create Virtual Environment (Recommended)

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing:

```bash
pip install pandas nltk scikit-learn streamlit spotipy
```

---

### 4️⃣ Download NLTK Data

```python
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
```

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

The app will open at:

```bash
http://localhost:8501
```

---

## 🔑 Spotify API Setup

To display album cover images:

### Step 1

Go to Spotify Developer Dashboard:

https://developer.spotify.com/dashboard

### Step 2

Create a new Spotify application

### Step 3

Get your:

* Client ID
* Client Secret

### Step 4

Replace credentials inside `app.py`

```python
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
```

---

## 📊 Dataset

Dataset Source:
Spotify Million Song Dataset from Kaggle

* 🎵 57,650 songs
* 🧑‍🎤 Artist names
* 🎼 Song titles
* 📝 Song lyrics

Dataset Link:
https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset

---

## 🧠 Recommendation System Workflow

### 1. Text Preprocessing

* Lowercasing
* Tokenization
* Removing unnecessary characters
* Stemming using Porter Stemmer

### 2. TF-IDF Vectorization

Converts song lyrics into numerical vectors.

### 3. Cosine Similarity

Measures similarity between songs.

### 4. Recommendation

Returns the Top 5 most similar songs.

---

## 📌 Important Notes

* The model uses a random sample of 10,000 songs for memory optimization.
* Recommendations may vary if the notebook is retrained.
* Large `.pkl` files are excluded from GitHub because of GitHub file size limits.

---

## 🌐 Deployment

This project is deployed on Streamlit Cloud.

🔗 Live App:
https://musicrecommenderksn.streamlit.app

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Developer

Developed by Kaung Sett Naing

GitHub:
https://github.com/KaungSettNaingKSN
