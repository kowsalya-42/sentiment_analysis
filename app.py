import streamlit as st
from openai import OpenAI
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def preprocess_review(review):
    review = review.strip()
    review = re.sub(r"\s+", " ", review)
    review = re.sub(r"[^a-zA-Z0-9.,!?\s]", "", review)
    return review


def analyze_review(review):
    review = preprocess_review(review)
    prompt = f"""
You are an expert sentiment analysis AI for a retail company. Analyze the review below and do two things:
1. Classify the sentiment as Positive, Negative, or Neutral.
2. Give a rating from 1 to 5, based on how the customer feels. Think like a human—don't be too robotic. Consider emotion, tone, and sarcasm.

Review: "{review}"

Respond in the format:
Sentiment: <sentiment>
Rating: <rating>/5
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You're skilled at detecting sentiment and mimicking how real humans would rate experiences, including sarcasm and subtle tone.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )
    print(response)
    return response.choices[0].message.content.strip()


st.set_page_config(page_title="Sentiment ", page_icon="")

st.title("💬 Sentiment & Rating Analyzer")
st.markdown(
    "Give me a customer review, darling, and I'll tell you how it *feels*—with a little star-rated heat."
)

user_review = st.text_area(
    "Enter your review:",
    placeholder="Type your review... and let me take care of rest.",
    height=150,
)

if st.button("Analyze Me"):
    if user_review.strip() == "":
        st.warning("You’ve got to give me *something* to work with...")
    else:
        with st.spinner("Reading the vibes..."):
            result = analyze_review(user_review)
            st.success("Analysis Complete!")
            st.markdown(f"**Result:**\n\n{result}")

with st.expander("Need a little inspiration?"):
    st.markdown(
        """
**Try these:**
- *Absolutely loved it! Exceeded all my expectations.*
- *I was excited, but this was such a letdown.*
- *It’s flawed, sure—but I weirdly love it.*
- *Oh joy, another amazing product that barely lasts a day. Bravo.*
    """
    )
