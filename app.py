import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 【重要】ここが変わった部分です
# ==========================================
# GitHubに公開しても鍵が漏れないようにする設定
try:
    # Streamlit Cloud（本番）にいる時は、サーバーの金庫から鍵をもらう
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # 自分のPCで動かす時用
    # ★注意：ここに直接キーを書いてGitHubに上げると、キーが無効化されます！
    # PCでテストする時だけ自分のキーを書き、アップロード時は消すか空欄にしてください。
    # os.environ["GOOGLE_API_KEY"] = "あなたのAPIキー"
    pass

# AIモデルの準備
model = genai.GenerativeModel('gemini-1.5-flash')

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
if st.button("マナブくんに教える"):
    if uploaded_file is not None and user_explanation:
        
        with st.spinner('マナブくんが考え中...'):
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

                # AIにデータを渡して答えをもらう
                response = model.generate_content([prompt, image_data])
                
                # 結果を表示
                st.subheader("マナブくんの返答:")
                st.info(response.text)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("画像と解説の両方をセットしてね！")
        
        