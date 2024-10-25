import pandas as pd
import streamlit as st
import pickle

# Load the apparel data and similarity matrix
apparel_dict = pickle.load(open('apparel_dict.pkl', 'rb'))
apparel = pd.DataFrame(apparel_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(data):
    index = apparel[apparel['title'] == data].index[0]
    distances = similarity[index]
    apparel_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_apparel = []
    recommended_images = []
    for i in apparel_list:
        recommended_apparel.append(apparel.iloc[i[0]].title)
        recommended_images.append(apparel.iloc[i[0]].images)  # Get image link(s)
    return recommended_apparel, recommended_images


# Streamlit app
st.title('Recommender System')

# Select apparel from the dropdown
select_apparel = st.selectbox(
    'Select the apparel you like:',
    apparel['title'].values
)

if st.button('Recommend'):
    recommendations, images = recommend(select_apparel)

    # Display recommendations in a 3x2 grid layout
    cols = st.columns(3)  # Create 3 columns

    for i, (title, img_links) in enumerate(zip(recommendations, images)):
        first_img_url = img_links.split(' | ')[0]  # Get only the first image URL

        # Assign each image to a column in the current row
        with cols[i % 3]:
            st.write(title)
            st.image(first_img_url, use_column_width=True)

        # Move to the next row after 3 images
        if (i + 1) % 3 == 0 and i < len(recommendations) - 1:
            cols = st.columns(3)
