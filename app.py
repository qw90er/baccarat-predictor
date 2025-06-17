import streamlit as st
from collections import Counter

st.set_page_config(page_title="百家樂預測系統", layout="centered")

# 🧠 進階預測邏輯（非單純 +1/-1）
def smart_count(cards):
    count = 0
    for c in cards:
        if c in ['4', '5', '6']:
            count += 1.5
        elif c in ['7']:
            count += 1
        elif c in ['A', '2', '3']:
            count -= 1
        # 8~K 為中性牌，不加減
    # 額外邏輯：若有兩張以上 4~6，加強莊方信號
    if sum(c in ['4', '5', '6'] for c in cards) >= 2:
        count += 1
    return count

# 預測下注方向
def predict_result(score):
    if score >= 1:
        return "莊"
    elif score <= -1:
        return "閒"
    else:
        return "和或不下"

# 初始化 session 狀態
if 'records' not in st.session_state:
    st.session_state.records = []

if 'history' not in st.session_state:
    st.session_state.history = []
    st.title("🎴 百家樂下注預測系統 V2")

st.markdown("請選擇本局牌（最多 6 張）：")

cols = st.columns(6)
cards = []
for i in range(6):
    with cols[i]:
        card = st.selectbox(f"第{i+1}張", ["", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"], key=f"card_{i}")
        if card != "":
            cards.append(card)

mode = st.radio("預測模式", ["單局預測", "累積加減"])

# 加總分數
score = smart_count(cards)

if mode == "累積加減":
    if st.button("加入此局牌值"):
        st.session_state.records.extend(cards)

    total_score = smart_count(st.session_state.records)
    result = predict_result(total_score)
    st.markdown(f"目前累積牌數：{len(st.session_state.records)} 張")

else:
    result = predict_result(score)

# 顏色顯示結果
color_map = {"莊": "red", "閒": "blue", "和或不下": "green"}
st.markdown(f"### 🤖 預測建議：<span style='color:{color_map.get(result, 'black')}'>{result}</span>", unsafe_allow_html=True)

# 存入歷史紀錄
if st.button("紀錄此預測"):
    st.session_state.history.append(result)
    # 統計資料
if st.session_state.history:
    st.markdown("## 📊 預測紀錄與統計")

    counter = Counter(st.session_state.history)
    total = len(st.session_state.history)

    col1, col2, col3 = st.columns(3)
    col1.metric("總預測次數", total)
    col2.metric("莊 次數", counter.get("莊", 0))
    col3.metric("閒 次數", counter.get("閒", 0))

    st.progress(counter.get("莊", 0) / total if total > 0 else 0.01, text="莊 勝率")
    st.progress(counter.get("閒", 0) / total if total > 0 else 0.01, text="閒 勝率")

    if st.button("🧹 清除所有紀錄"):
        st.session_state.history = []
        st.session_state.records = []
        st.experimental_rerun()
else:
    st.info("目前尚無紀錄，請先預測並紀錄。")
