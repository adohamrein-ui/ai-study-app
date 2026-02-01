import streamlit as st
import google.generativeai as genai
import os

st.title("🛠 マナブくん診断モード")

# ==========================================
# 1. 鍵のチェック（画面に見せます）
# ==========================================
api_key = None
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ クラウドの金庫(Secrets)から鍵を取り出しました！")
except:
    # PC用の設定（もしPCで動かすならここを書き換える）
    # api_key = "AIzaSy..." 
    st.warning("⚠️ Secretsが見つかりません。PC設定を見に行きます。")

if not api_key:
    st.error("❌ APIキーがありません！設定を確認してください。")
    st.stop()

# モデル設定
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 2. 接続テスト（画像なしで会話できるか？）
# ==========================================
st.write("---")
st.write("まずは「画像なし」でテストしてみよう。")
if st.button("マナブくん、元気？（接続テスト）"):
    try:
        response = model.generate_content("一言で挨拶して！")
        st.success(f"🤖 マナブくんの返事: {response.text}")
        st.info("🙆‍♂️ AIとの通信は成功です！鍵は合っています。")
    except Exception as e:
        st.error(f"❌ 通信エラー: {e}")

# ==========================================
# 3. 本番テスト（画像あり）
# ==========================================
st.write("---")
uploaded_file = st.file_uploader("問題の画像をアップロード", type=["jpg", "png", "jpeg", "webp"])
user_explanation = st.text_area("解説を入力")

if st.button("画像付きで教える"):
    if uploaded_file and user_explanation:
        st.write("🔄 画像を処理中...")
        
        # 画像情報の表示（デバッグ用）
        st.write(f"ファイル形式: {uploaded_file.type}")
        st.write(f"ファイルサイズ: {uploaded_file.size} bytes")

        try:
            image_data = {'mime_type': uploaded_file.type, 'data': uploaded_file.getvalue()}
            
            st.write("🔄 Geminiに送信中...")
            response = model.generate_content(
                ["この画像について、先生（ユーザー）がこう言っています: " + user_explanation, image_data]
            )
            st.success("✅ 返信が来ました！")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"❌ エラー発生: {e}")
            st.write("ヒント: iPhoneの写真は「HEIC」という形式かもしれません。スクショを撮って、そのスクショを送ってみてください。")
    else:
        st.warning("画像と文字を入れてね")
        