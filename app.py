import streamlit as st
from collections import Counter

st.set_page_config(page_title="百家樂預測系統", layout="centered")

# 🧠 進階預測邏輯
def smart_count(cards):
    count = 0
    for c in cards:
        if c in ['4', '5', '6']:
            count += 1.5
        elif c == '7':
            count += 1
        elif c in ['A', '2', '3']:
            count -= 1
    if sum(c in ['4', '5', '6'] for c in cards) >= 2:
        count += 1
    return count

def predict_result(score):
    if score >= 1:
        return "莊"
    elif score <= -1:
        return "閒"
    else:
        return "和或不下"

# 初始化狀態
if 'selected_cards' not in st.session_state:
    st.session_state.selected_cards = []

if 'records' not in st.session_state:
    st.session_state.records = []

if 'history' not in st.session_state:
    st.session_state.history = []
    st.title("🃏 百家樂預測系統 v2")

st.markdown("### 請點選最多 6 張牌：")
card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
card_cols = st.columns(len(card_values))

for i, val in enumerate(card_values):
    with card_cols[i]:
        if st.button(val, key=f"card_btn_{val}", use_container_width=True, type="secondary"):
            if len(st.session_state.selected_cards) < 6:
                st.session_state.selected_cards.append(val)

# 顯示目前已選的牌
st.markdown("**你目前選的牌：**")
st.write("、".join(st.session_state.selected_cards) if st.session_state.selected_cards else "尚未選擇")

colA, colB = st.columns(2)
if colA.button("🔙 移除最後一張"):
    if st.session_state.selected_cards:
        st.session_state.selected_cards.pop()

if colB.button("🧹 清除全部選牌"):
    st.session_state.selected_cards = []

mode = st.radio("預測模式", ["單局預測", "累積加減"])

if mode == "累積加減":
    if st.button("➕ 加入累積"):
        st.session_state.records.extend(st.session_state.selected_cards)
        st.session_state.selected_cards = []

    total_score = smart_count(st.session_state.records)
    result = predict_result(total_score)
    st.markdown(f"累積牌數：{len(st.session_state.records)} 張")

else:
    score = smart_count(st.session_state.selected_cards)
    result = predict_result(score)

# 顏色顯示結果
color_map = {"莊": "red", "閒": "blue", "和或不下": "green"}
st.markdown(f"### 🤖 預測建議：<span style='color:{color_map.get(result)}'>{result}</span>", unsafe_allow_html=True)

if st.button("📥 紀錄此預測"):
    st.session_state.history.append(result)
    # 統計紀錄區
if st.session_state.history:
    st.markdown("---")
    st.markdown("## 📊 預測紀錄與統計")

    counter = Counter(st.session_state.history)
    total = len(st.session_state.history)
    banker = counter.get("莊", 0)
    player = counter.get("閒", 0)

    col1, col2, col3 = st.columns(3)
    col1.metric("總預測次數", total)
    col2.metric("莊 次數", banker)
    col3.metric("閒 次數", player)

    st.markdown("#### 勝率：")
    st.progress(banker / total if total > 0 else 0, text="莊 勝率", color="red")
    st.progress(player / total if total > 0 else 0, text="閒 勝率", color="blue")

    if st.button("🧽 清除所有紀錄"):
        st.session_state.history = []
        st.session_state.records = []
        st.session_state.selected_cards = []
        st.experimental_rerun()
else:
    st.info("目前尚無預測紀錄，請先選牌後紀錄。")
