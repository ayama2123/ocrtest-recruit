import streamlit as st
from PIL import Image
import pytesseract
import openai

# OpenAI APIキーの設定
openai.api_key = 'YOUR_OPENAI_API_KEY'

# OCRを使って画像からテキストを抽出する関数
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='jpn')
    return text

# ChatGPTを使ってテキストから給与や勤務地を解析する関数
def parse_job_info_with_gpt(text):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"以下のテキストから給与や勤務地の情報を抽出してください。\n\n{text}\n\n給与情報:\n勤務地情報:",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlitアプリの設定
st.title("求人情報抽出アプリ")

uploaded_file = st.file_uploader("画像を選択してください...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像。', use_column_width=True)
    
    st.write("情報を抽出しています...")
    
    text = extract_text_from_image(image)
    
    parsed_info = parse_job_info_with_gpt(text)
    
    st.write("**抽出された情報:**")
    st.write(parsed_info)
