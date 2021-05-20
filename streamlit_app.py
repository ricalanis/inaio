import streamlit as st
import requests
from io import BytesIO
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)


st.sidebar.title("Qué preguntamos durante COVID")
st.sidebar.write("Conoce a quién y cómo nos contestaron. Se muestran las palabras de las peticiones realizadas, grupos de preguntas, sujetos obligados contactados y la respuesta dada.")

st.sidebar.write('[Descargar la base de solicitudes de covid abierta](https://pnt-results.s3.us-east-2.amazonaws.com/requests.json.zip)')

st.sidebar.title("Selecciona los parametros que quieras usar: ")
state = st.sidebar.selectbox("Estado", ['Federación','Aguascalientes', 'Baja California', 'Baja California Sur',
       'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad De México', 'Coahuila',
       'Colima', 'Durango', 'Estado De México',
       'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán',
       'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla',
       'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa',
       'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz',
       'Yucatán', 'Zacatecas'])

date = st.sidebar.select_slider("Fecha de petición", ['03-2019', '07-2019', '08-2019', '10-2019', '11-2019', '12-2019',
       '01-2020', '02-2020', '03-2020', '04-2020', '05-2020', '06-2020',
       '07-2020', '08-2020', '09-2020', '10-2020', '11-2020', '12-2020',
       '01-2021', '02-2021', '03-2021', '04-2021', '05-2021'], '09-2020')

run = st.sidebar.button('Obtener')

if run:

    response = requests.get(f'https://pnt-results.s3.us-east-2.amazonaws.com/source_data/{state.lower()}/{date}.source')
    raw_pickle = BytesIO(response.content)
    input_data = pickle.load(raw_pickle)

    col1, col2 = st.beta_columns(2)


    wordcloud = WordCloud(background_color='white').generate(input_data['text'])

    with col1:

        fig, ax = plt.subplots(figsize=(5, 5))
        # Display the generated image:
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.title.set_text("Menciones de todos los temas")
        st.pyplot()

        f, axs = plt.subplots(2,2,figsize=(5,2))
        plt.subplot(1, 2, 1)
        sns.barplot(x=input_data['subject_counts'][0:10].index, y=input_data['subject_counts'][0:10])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=90)

        plt.subplot(1, 2, 2)
        sns.barplot(x=input_data['response_type_counts'][0:10].index, y=input_data['response_type_counts'][0:10])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=90)
        st.pyplot()


    with col2:
        lda_model = input_data['lda_model']
        fig = plt.figure()
        for t in range(lda_model.num_topics):
            ax = fig.add_subplot(3,2,t+1)
            ax.imshow(WordCloud(background_color='white').fit_words(dict(lda_model.show_topic(t, 200))))
            ax.title.set_text(f'Topico #{t+1}')
            ax.axis("off")
        st.pyplot()



