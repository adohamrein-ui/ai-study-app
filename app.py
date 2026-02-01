import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 【修正版】鍵の設定エリア
# ==========================================
api_key = None

# 1. まず「Secrets（クラウドの金庫）」に鍵があるか確認
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# 2. なければ、直接コードに書かれた鍵を使う（PC用）
if not api_key:
    # ★重要：PCで動かす時は、下の "AIza..." を自分のキーに書き換えてね！
    api_key = "AIzaSy..." 

# 3. それでも鍵がなければ、画面に「鍵がないよ！」と出す
if not api_key or api_key == "AIzaSyBkk7vuX9__QhGCXAQNRi_2ieEZInRxSXo":
    st.error("⚠️ APIキーが見つかりません！PCで動かす場合はコード内の 'AIzaSy...' を自分のキーに書き換えてください。クラウドの場合はSecretsを設定してください。")
    st.stop() # ここで止める

# 鍵をセット！
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# ...（ここから下は変更なし）...

# ==========================================
# アプリの画面デザイン（ここは前と同じ）
# ==========================================
st.title("🎓 AI生徒 マナブくん")
st.write("画像をアップして、解説（テキスト）を入力してね！")

# 1. 画像アップロード
uploaded_file = st.file_uploader("問題の写真をアップロード", type=["jpg", "png", "jpeg"])

# 2. 解説入力
user_explanation = st.text_area("先生（あなた）の解説：", height=150)


# 3. 「教える」ボタン
# ==========================================
if st.button("マナブくんに教える"):
    if uploaded_file is not None and user_explanation:
        
        # 準備中の表示
        with st.spinner('マナブくんが画像を読んでいます...'):
            try:
                # 画像データを処理できる形にする
                image_data = {'mime_type': uploaded_file.type, 'data': uploaded_file.getvalue()}

                # AIへの指令（プロンプト）
                prompt = f"""
                あなたは数学・物理・化学が苦手で、少し理屈っぽい高校生「マナブ」です。
                ユーザーはあなたの先生です。
                
                1. アップロードされた「問題の画像」を見てください。
                2. 先生の「解説テキスト」を読んでください。
                3. 解説の中で「説明が飛躍している点」「初心者がつまづきそうな点」を見つけて、
                   「え、先生ここわかんない。なんで〇〇が△△になるの？」とタメ口で質問してください。
                4. もし解説が完璧なら、「なるほど！めっちゃわかった！」と褒めてください。
                
                先生の解説: {user_explanation}
                """

                # ★ここが変わった！ stream=True を追加
                response = model.generate_content([prompt, image_data], stream=True)
                
                # 結果を表示するエリア
                st.subheader("マナブくんの返答:")
                
                # ★ここも変わった！ 文字を少しずつ表示する魔法
                response_placeholder = st.empty() # 空の箱を用意
                full_text = "" # まだ何も喋ってない
                
                for chunk in response:
                    full_text += chunk.text # 新しい言葉を足す
                    response_placeholder.info(full_text) # 箱の中身を更新！

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("画像と解説の両方をセットしてね！")

        