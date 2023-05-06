import pandas as pd
import streamlit as st
import nltk
import uniq_token as uq
import numpy as np
import webbrowser
import streamlit.components.v1 as components
import evaluate as eval
import textrank as tr

from lex_rank import LexRank
from power_methods import stationary_distribution, connected_nodes, _power_method
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import MWETokenizer
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from chart import chart as charts
from PIL import Image

st.title('LexSumy')
st.write('Made by @Hardus Tukan')
image = Image.open(r"util/alun_alun.png")
link = r'https://drive.google.com/file/d/1KQbGHhnQWj60uOmehyaaNQZFvdSVyNQN/view?usp=sharing'
if st.button('Download Korpus File', help="Butuh file uji untuk meringkas ?  bisa didownload disini"):
    webbrowser.open_new_tab(link)

nltk.download('punkt')
file_names = []
# check row_text
raw_texts = []
upload_file = st.file_uploader(
    'Input Documents', type="txt", accept_multiple_files=True)
for upload_files in upload_file:
    byte_data = str(upload_files.read(), "utf-8")
    raw_texts.append(byte_data)
    title_file_name = upload_files.name.replace('.txt', '')
    file_names.append(title_file_name)

factory = StemmerFactory()
stemmer = factory.create_stemmer()
listStopwordID = set(stopwords.words('indonesian'))
listStopwordEN = set(stopwords.words('english'))

docs = [i.strip("[]").split("\n") for i in raw_texts]


remove_list = " ".join([str(t) for t in raw_texts])

expander = st.expander("Teks Awal")
expander.write(docs)


### Preprocessing ###
original_sentc = [sentence for sentence in sent_tokenize(remove_list)]


def preprocessing_text(text):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokenized = [tokenizer.tokenize(s.lower()) for s in text]
    important_token = []
    for sent in tokenized:
        important_token.append(sent)
    sw_removed = [' '.join(t) for t in important_token]
    stemmed_sent = [stemmer.stem(sent) for sent in sw_removed]
    return stemmed_sent


mwe = MWETokenizer([k.split() for k in uq.unique_token], separator='_')


def phrase_preprocessing_text(text):
    tokenized_paragraph = [
        token for token in mwe.tokenize(word_tokenize(text))
    ]
    tokenized_paragraph = ' '.join([str(t) for t in tokenized_paragraph])
    phrase_prepc = [
        sentence for sentence in sent_tokenize(tokenized_paragraph)
    ]
    return phrase_prepc


# sidebar
st.sidebar.image(image, use_column_width=True,
                 caption="Support by Alun-alun UKDW")

main_sentences = st.sidebar.selectbox(
    'Pilih Sentences',
    ('Original Sentences', "Preprocessing Sentences", 'Phrase Sentences'),
    help='Kamu bisa memilih jenis kalimat apa yang ingin diringkas'
)

set_stopwords = st.sidebar.selectbox(
    'Atur Stopwords',
    ('Indonesia', 'English', 'No Stopwords'),
    help='Kamu bisa mengatur stopwords, disesuaikan bahasa yang anda gunakan. Defaultnya Bahasa Indonesia'
)

set_threshold = st.sidebar.selectbox(
    'Atur Threshold',
    (0.1, 0.2, 0.3, 0.4, 0.5),
    help='Kamu bisa memilih ambang batas dari range 0.1-0.5'
)

set_summarize = st.sidebar.selectbox(
    "Atur Evaluasi Ringkasan",
    ('LexRank', 'TextRank'),
    help='Kamu bisa memilih hasil ringkasan yang ingin dievaluasi'
)

set_slider = st.sidebar.slider(
    'Atur Panjang Ringkasan',
    0, 100, 25,
    help='Kamu bisa mengatur panjang ringkasan dari range 0-100% , untuk defaultnya 25%'
)


def get_main_sentences(name, remove_list, original_sentc):
    sentc = None
    if name == 'Original Sentences':
        sentc = original_sentc
    elif name == 'Preprocessing Sentences':
        sentc = preprocessing_text(original_sentc)
    else:
        sentc = phrase_preprocessing_text(remove_list)
    return sentc


def get_threshold(number):
    numb = None
    if number == 0.1:
        numb = .1
    elif number == 0.2:
        numb = .2
    elif number == 0.3:
        numb = .3
    elif number == 0.4:
        numb = .4
    else:
        numb = .5
    return numb


def get_stopwords(text):
    name = None
    if text == 'Indonesia':
        name = listStopwordID
    elif text == 'English':
        name = listStopwordEN
    elif text == 'No Threshold':
        name = name
    return name

# html


def visualize(sentence_list, best_sentences):
    text = ''
    for sentence in sentence_list:
        if sentence in best_sentences:
            text += ' ' + str(sentence).replace(sentence,
                                                f"<mark>{sentence}</mark>")
        else:
            text += ' ' + sentence
    return text


sentences = get_main_sentences(main_sentences, remove_list, original_sentc)
th = get_threshold(set_threshold)
listStopword = get_stopwords(set_stopwords)

st.subheader("LexRank Summary")
sm1 = sentences  # teks query
sm2 = docs  # teks utama
sum_size = int(len(sm1) * (set_slider/100))


### LEXRANK LIBRARY ###
def main():
    try:
        lxr = LexRank(sm1, stopwords=listStopword)

        scores_cont = lxr.rank_sentences(
            sm1,
            threshold=th,
            fast_power_method=True,
        )

        column_table = pd.DataFrame({'Sentence': sm1})
        st.dataframe(column_table)

        top_scores = np.argsort(scores_cont)[-sum_size:]
        summ_index = sorted(top_scores)
        summarize = [sm1[i] for i in summ_index[:sum_size]]

        ordered_score = sorted(
            ((scores_cont[i], score) for i, score in enumerate(summarize)), reverse=True)
        st.caption("score")
        st.dataframe(ordered_score)

        # st.write(summary)
        sumLexRank = ' '.join(summarize)

        # if needed
        with st.expander("Code"):

            with st.echo():

                t_f = lxr.tokenize_sentence
                tf_scores = [
                    Counter(t_f(sentence)) for sentence in sm1
                ]

                tf = tf_scores
                st.write(tf)
                idfDocs = lxr._calculate_idf(sm2)
                idfSum1 = lxr._calculate_idf(tf)
                st.write(idfDocs)
                st.write(idfSum1)

            with st.echo():
                idf_modified_csn = lxr._calculate_similarity_matrix(tf)
                st.write(idf_modified_csn)

            with st.echo():
                markov_m = lxr._markov_matrix(idf_modified_csn)
                markov_m_w_th = lxr._markov_matrix_discrete(
                    idf_modified_csn, th)
                stat_distr_1 = stationary_distribution(markov_m)
                stat_distr_2 = stationary_distribution(markov_m_w_th)
                st.write(stat_distr_1)
                st.write(stat_distr_2)

            with st.echo():
                conect_matrix = connected_nodes(markov_m_w_th)
                st.write(conect_matrix)

            charts(remove_list, sumLexRank)

        # st.write(summ)
        st.caption("Summary")
        st.write(sumLexRank)

        st.download_button(label='Download Teks',
                           data=sumLexRank, file_name='Summary.txt')

        with st.expander("HTML"):
            html_object = visualize(sm1, sumLexRank)
            components.html(html_object, width=680, height=600, scrolling=True)

        st.caption("Comparison LexRank & TextRank")
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("LexRank"):
                components.html(sumLexRank, height=600, scrolling=True)

        sumTextRank = tr.textRank(sm1)
        with col2:
            with st.expander("TextRank"):
                components.html(sumTextRank, height=600, scrolling=True)

        # kurang rapi
        def getEval(name):
            temp = None
            if name == 'LexRank':
                temp = sumLexRank
            else:
                temp = sumTextRank
            return temp

        with st.expander("Evaluate"):
            user_text = st.text_area("Paste Text Here", height=250)
            # if st.button('Display'):
            #     st.write(user_text)
            graph = eval.evaluate(user_text, getEval(set_summarize))
            st.json(graph)

    except ValueError:
        if len(file_names) == 0:
            st.write('no data')
        else:
            st.write("")


if __name__ == '__main__':
    main()
