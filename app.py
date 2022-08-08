### KICKOFF - CODING AN APP IN STREAMLIT

### import libraries
import pandas as pd
import streamlit as st
import numpy as np
import joblib
import requests 
import plotly.express as px


#######################################################################################################################################

st.title("MTG Color Classifier")

#######################################################################################################################################
### DATA LOADING

# Load our models using joblib

encoder = joblib.load('models/subtype_encoder.pkl')
vectorizer = joblib.load('models/count_vectorizer.pkl')
model = joblib.load('models/mtg_logit.pkl')

coef_df = pd.read_csv('data/coef.csv').set_index('coef')

# Set all known types to create a dropdown
TYPES = ('Creature','Instant','Enchantment','Sorcery','Artifact'
        ,'Land','Artifact Creature','Planeswalker','Creature Enchantment','Instant Tribal'
        ,'Artifact Land','Sorcery Tribal','Enchantment Tribal','Artifact Tribal','Artifact Enchantment'
        ,'Creature Land','Enchantment Land')

class_color = {0: 'Colorless', 1: 'Green', 2: 'Blue', 3: 'Red', 4: 'Black', 5: 'White'}
color_img = {0: 'assets/colorless.png', 1: 'assets/green.png', 2: 'assets/blue.png'
            , 3: 'assets/red.png', 4: 'assets/black.png', 5: 'assets/white.png'}

tab1, tab2, tab3 = st.tabs(["Existing Cards", "Custom Cards", "Coefficients"])


#######################################################################################################################################

## EXISTING CARDS

#######################################################################################################################################

with tab1:
    st.subheader("Existing Card Database")

    all_cards_df = pd.read_csv('data/all_cards.csv').set_index('name')

    # Asking for cards
    card_name = st.selectbox('Choose a card:', all_cards_df.index)
    # Find card in database
    chosen_card = all_cards_df.loc[[card_name]]

    ## Find the image
    r = requests.get(f"https://api.scryfall.com/cards/search?q=!'{card_name}'")   
    try:
        image_link = r.json()['data'][0]['image_uris']['large']
    except:
        r = requests.get(f"https://api.scryfall.com/cards/search?q={card_name}")
        image_link = r.json()['data'][0]['image_uris']['large']

    ## Vectorizing...
    column_names = [('text_' + x) for x in vectorizer.get_feature_names()]
    chosen_card[column_names] = vectorizer.transform(chosen_card['name_text']).todense()
    chosen_card.drop('name_text', axis=1, inplace=True)

    # Predicting
    prediction = model.predict(chosen_card)
    probabilities = pd.DataFrame(model.predict_proba(chosen_card)).rename(columns=class_color)

    ## Rendering results    
    fig = px.bar(probabilities, barmode='group'
                ,color_discrete_sequence=["#964B00", "#00733e", "#0e67ab","#d3202a","#150b09", "#bdbdbd"]
                ,title=f'Probability Plot for {card_name}')
    fig.update_yaxes(range=[0,1.0],title='Probability')
    fig.update_xaxes(visible=False)
    fig.update_layout(legend_title_text='Color Identity')

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image_link)

    with col2:
        st.write(f'This looks like a **{class_color[prediction[0]]}** card.')
        st.write(f'#### Indicators for {class_color[prediction[0]]}')

            # Getting significant coefficents
        transposed_card = chosen_card.drop(columns=['manaValue','power','toughness'])
        transposed_card[transposed_card.columns] = transposed_card[transposed_card.columns].astype(int)
        transposed_card = transposed_card.T.rename(columns={card_name: 'Value'})
        transposed_card.index.name = 'coef'
        present_tokens = transposed_card[transposed_card['Value'] > 0]

        significant_tokens = pd.merge(present_tokens, coef_df, left_index=True, right_index=True).sort_values(str(prediction[0]),ascending=False)

        for index, row in significant_tokens.head(5).iterrows():
            st.markdown(f"- {row.name}")

#######################################################################################################################################

### CUSTOM CARD CREATION

#######################################################################################################################################

with tab2:
    st.subheader("Build a Custom Card")

    # B. Set up input fields

    col1, col2 = st.columns(2)

    with col1: 
        name = st.text_input('Card Name','Volcanic Giant')
        types = st.selectbox(
             'Type',
             TYPES)
        subtypes = st.text_input('Subtypes','Giant')

    with col2:

        if ('Creature' not in types):
            power = st.number_input('Power',-1,disabled=True)
            toughness = st.number_input('Toughness',-1,disabled=True)
        else:
            power = st.number_input('Power',0,value=6)
            toughness = st.number_input('Toughness',0,value=6)
        manaValue = st.number_input('Mana Value',6)

    description = st.text_input('Description','Trample. When Volcanic Giant enters the battlefield, deal 3 damage to all other \
                                creatures. ')

    # C. Preprocessing the data...


    mtg_df = pd.DataFrame(np.array([[manaValue,power,toughness]]),columns=['manaValue','power','toughness'])


    ## Encoding...

    if subtypes == "":
        subtype_baskets = np.array([list([])])
    else:
        subtype_baskets = np.array([list(subtypes.split(" "))])

    mtg_df[encoder.columns_] = encoder.transform(subtype_baskets)


    # Dummify Types

    type_dummies = [('types_' + x) for x in TYPES]
    mtg_df[type_dummies] = 0
    mtg_df['types_' + types] = 1


    ## Vectorizing...


    mtg_df[column_names] = vectorizer.transform([name + description]).todense()


    # C. Use the model to predict sentiment & write result

    prediction = model.predict(mtg_df)
    probabilities = pd.DataFrame(model.predict_proba(mtg_df)).rename(columns=class_color)

    ## Rendering results
    
    fig = px.bar(probabilities, barmode='group'
                ,color_discrete_sequence=["#964B00", "#00733e", "#0e67ab","#d3202a","#150b09", "#bdbdbd"]
                ,title=f'Probability Plot for {name}')
    fig.update_yaxes(range=[0,1.0],title='Probability')
    fig.update_xaxes(visible=False)
    fig.update_layout(legend_title_text='Color Identity')

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([1,2])

    with col1:
        st.image(color_img[prediction[0]])
    with col2:
        st.write(f'This looks like a **{class_color[prediction[0]]}** card.')
        st.write(f'#### Indicators for {class_color[prediction[0]]}')

            # Getting significant coefficents
        transposed_card = mtg_df.drop(columns=['manaValue','power','toughness'])
        transposed_card[transposed_card.columns] = transposed_card[transposed_card.columns].astype(int)
        transposed_card = transposed_card.T.rename(columns={0: 'Value'})
        transposed_card.index.name = 'coef'

        present_tokens = transposed_card[transposed_card['Value'] > 0]

        significant_tokens = pd.merge(present_tokens, coef_df, left_index=True, right_index=True).sort_values(str(prediction[0]),ascending=False)

        for index, row in significant_tokens.head(5).iterrows():
            st.markdown(f"- {row.name}")

#######################################################################################################################################

### VIEW COEFFICIENTS

#######################################################################################################################################

with tab3:

    st.subheader("Visualizations of Coefficients")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.selectbox("Class",class_color.values())
    with col2:
        st.selectbox("Sort by",('Ascending','Descending'))
    with col3:
        st.number_input("Number of Results",5, value=10)

    fig = px.bar()


#######################################################################################################################################
### MODEL PERFORMANCE ON CUSTOM CARDS


