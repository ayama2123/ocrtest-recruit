import streamlit as st
from PIL import Image
import pytesseract
import openai
import os

# OpenAI APIキーの設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# OCRを使って画像からテキストを抽出する関数
#def extract_text_from_image(image):
#    text = pytesseract.image_to_string(image, lang='jpn')
#    return text

def extract_text_from_image(image):
    prompt = f"""
    あなたは{image}から文字を読み取るOCRです。
    取得すべき情報は下記の項目です。
    -給与
    -勤務地
    -必要な資格・スキル
    -年間休日数
    -ボーナスの有無
    -福利厚生
    -交通費や賃料の補助
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"あなた{image}から必要な情報を取得するGPTです。"},
            {"role": "user", "content": prompt},
            {"role": "type", "image": prompt},
        ],
    )
    text = response.choices[0].message.content
    return text
    #return response.choices[0].message.content

# ChatGPTを使ってテキストから給与や勤務地を解析する関数
def parse_job_info_with_gpt(text):
    prompt = f"""
    あなたは高校生の就職活動をサポートするアドバイザーです。
    
    {text}から、以下の項目を取得します。また、それぞれの項目に評価を出力します。
    評価とは一般的にその情報が良い、普通、悪い3つの段階で測定し、注意すべき点または良いところがあれば出力します。
    -給与
    -勤務地
    -必要な資格・スキル
    -年間休日数
    -ボーナスの有無
    -福利厚生
    -交通費や賃料の補助
    これらの項目を出力したあと、採用面接の際に質問すべきことを3つ簡潔に出力します。
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"あなたは求人情報から必要な情報を取得するGPTです。"},
            {"role": "user", "content": prompt},
        ],
       #max_tokens=1500
    )
    return response.choices[0].message.content

# Streamlitアプリの設定
st.title("求人情報抽出アプリ")

uploaded_file = st.file_uploader("画像を選択してください...", type=["jpg", "jpeg", "png"])

if st.button("分析開始（少し時間がかかります）"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='アップロードされた画像', use_column_width=True)
        
        st.write("情報を抽出しています...")
        
        text = extract_text_from_image(image)
        
        parsed_info = parse_job_info_with_gpt(text)
        
        st.write("**抽出された情報:**")
        st.write(parsed_info)
