import streamlit as st
import requests
from base64 import b64encode
import os

# Segmind API Key (Replace with your key)
API_KEY = os.getenv("SEGMIND_API_KEY")
API_URL = "https://api.segmind.com/v1/llama-v3p2-90b-vision-instruct"


# Function to convert image to base64
def encode_image(image_file):
    return b64encode(image_file.read()).decode("utf-8")


# Function to call Segmind's Vision LLM for plant analysis
def analyze_plant_leaf(image_data):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": """
                **Task:** Identify the type of plant leaf and diagnose nutrient deficiency from the given image.

                **Instructions:**
                - Accept **only plant leaf images**. If the uploaded image is not a plant leaf, reject it.
                - First, **identify the plant species** or provide the closest possible match.
                - Next, **analyze the leaf condition** and determine if there are any **nutrient deficiencies or diseases**.
                - If a deficiency is found, provide a structured markdown-formatted report covering:
                  1. **What is the deficiency?** (Name the deficient nutrient)
                  2. **Why does this happen?** (Scientific and environmental causes)
                  3. **How does this affect the plant?** (Impact on growth, yield, symptoms)
                  4. **What should be done?** (Recommended treatments, fertilizers, soil correction)
                  5. **How to prevent it?** (Long-term soil health & preventive measures)
                - If the image is **unclear** and the leaf **cannot be properly analyzed**, request a **higher-resolution image** but do NOT add unnecessary disclaimers.
                
                **Output Format:**
                - Provide a **concise, structured report** in Markdown format.
                - Ensure the response is **clear, technical, and practical** without redundant statements.
                """
            },
            {
                "role": "assistant",
                "content": "Analyzing the image and generating the nutrient deficiency report..."
            }
        ]
    }

    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        print(response.status_code, response.text)

        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"


st.title("🌱 Plant Nutrient Deficiency Detector")
st.subheader("**GeoGrow**")
st.markdown("<br><br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a **plant leaf image** (JPEG, PNG)", type=["png", "jpg", "jpeg"])
if st.button("Analyze Image"):
    if uploaded_file:
        image_data = encode_image(uploaded_file)
        response_text = analyze_plant_leaf(image_data)
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        st.markdown("### 🌿 Nutrient Deficiency Report")
        st.markdown(response_text)
    else:
        st.warning("Please upload a **plant leaf image**.")
