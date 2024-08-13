from flask import Flask, request, render_template
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.form['text']
    num_sentences = request.form.get('num_sentences', type=int, default=5)

    # Tokenizing the text
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Frequency distribution of words
    freq_dist = FreqDist(filtered_words)
    ranking = {sent: sum((freq_dist[word] for word in word_tokenize(sent.lower()) if word in freq_dist)) for sent in sentences}

    # Sorting sentences by frequency and picking the top N sentences
    ranked_sentences = sorted(ranking, key=ranking.get, reverse=True)
    summary = ' '.join(ranked_sentences[:num_sentences])

    return render_template('index.html', original_text=text, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
