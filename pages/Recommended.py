
import pandas as pd
import streamlit as st
from bokeh.models.widgets import Div
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
    
st.set_page_config(layout='centered', initial_sidebar_state='expanded')
st. sidebar.image('Data/App_icon.png')
st.markdown("<h1 style='text-align: center;'>Recommend</h1>", unsafe_allow_html=True)

df = pd.read_csv("./Data/TripAdvisor_RestauarantRecommendation.csv")

df["Location"] = df["Street Address"] +', '+ df["Location"]
df = df.drop(['Street Address',], axis=1)

df = df[df['Comments'].notna()]
df = df.drop_duplicates(subset='Name')
df = df.reset_index(drop=True)

name = st.selectbox('Select the Restaurant you like', (list(df['Name'].unique())))

def recom(dataframe,name):
    dataframe = dataframe.drop(["Trip_advisor Url", "Menu"], axis=1)
    
    # Creating recommendations

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(dataframe.Comments)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)    
    indices = pd.Series(dataframe.index, index=dataframe.Name).drop_duplicates()
    idx = indices[name]
    if isinstance(idx, pd.Series) == True:
        idx = idx[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    restaurant_indices = [i[0] for i in sim_scores]
    
    recommended = list(dataframe['Name'].iloc[restaurant_indices])
    st.markdown("## Top 10 Restaurants you might like:")

    title = st.selectbox('Restaurants most simlar', recommended)
    if title in dataframe['Name'].values:
        Reviews = (dataframe.at[dataframe['Name'].eq(title).idxmax(), 'Reviews'])
        st.markdown("### Restaurant Rating:-")

        #REVIEWS
        if Reviews == '4.5 of 5 bubbles':
            image = Image.open('Data/Ratings/Img4.5.png')
            st.image(image, use_column_width=True)


        elif Reviews == '4 of 5 bubbles':
            image = Image.open('Data/Ratings/Img4.0.png')
            st.image(image, use_column_width=True)


        elif Reviews == '5 of 5 bubbles':
            image = Image.open('Data/Ratings/Img5.0.png')
            st.image(image, use_column_width=True)

        else:
            pass
        
        #COMMENTS
        if 'Comments' not in dataframe.columns:
            pass
        else:
            comment = (dataframe.at[dataframe['Name'].eq(title).idxmax(), 'Comments'])
            if comment != "No Comments":
                st.markdown("### Comments:-")
                st.warning(comment)
            else:
                    pass

        #TYPE OF RESTURANT
        Type = (dataframe.at[dataframe['Name'].eq(title).idxmax(), 'Type'])
        st.markdown("### Restaurant Category:-")
        st.error(Type)

        #LOCATION
        Location = (dataframe.at[dataframe['Name'].eq(title).idxmax(), 'Location'])
        st.markdown("### The Address:-")
        st.success(Location)

        #CONTACT DETAILS
        contact_no = (dataframe.at[dataframe['Name'].eq(title).idxmax(), 'Contact Number'])
        if contact_no == "Not Available":
            pass

        else:
            st.markdown("### Contact Details:-")
            st.info('Phone:- '+ contact_no)
    

    st.text("")
    image = Image.open('Data/enjoy_your_meal.jpg')
    st.image(image, use_column_width=True)




recom(df,name)







