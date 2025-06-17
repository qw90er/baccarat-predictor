import streamlit as st
from collections import Counter

st.set_page_config(page_title="百家樂分邊預測", layout="wide")

# 🧠 分邊進階加權預測邏輯
def score_side(cards):
    score = 0
    for c in cards:
        if c in ['4', '5', '6']:
            score += 1.5
        elif c == '7':
            score += 1
        elif c in ['A', '2', '3']:
            score -= 1
    if sum(c in ['4', '5', '6'] for c in cards) >= 2:
        score += 1
    return score

def predict_result(banker_cards, player_cards):
    b_score = score_side(banker_cards)
    p_score = score_side(player_cards)
    diff = b_score - p_score
    if diff >= 1:
        return "莊"
    elif diff <= -1:
        return "閒"
    else:
        return "和或不下"

# 初始化狀態
for key in ["banker_cards", "player_cards", "records", "history"]:
    if key not in st.session_state:
        st.session_state[key] = []
        st.title("🎴 百家樂分邊選牌預測")

# 模式選擇（單局 / 累積）
mode = st.radio("模式選擇", ["單局預測", "累積預測"], horizontal=True)

# 分左右兩邊選牌
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟥 選擇莊的牌（最多3張）")
    for card in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        if st.button(card + "（莊）", key="B_" + card):
            if len(st.session_state.banker_cards) < 3:
                st.session_state.banker_cards.append(card)

    st.write("已選牌：", "、".join(st.session_state.banker_cards))
    if st.button("🔁 清除莊牌"):
        st.session_state.banker_cards = []

with col2:
    st.subheader("🟦 選擇閒的牌（最多3張）")
    for card in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        if st.button(card + "（閒）", key="P_" + card):
            if len(st.session_state.player_cards) < 3:
                st.session_state.player_cards.append(card)

    st.write("已選牌：", "、".join(st.session_state.player_cards))
    if st.button("🔁 清除閒牌"):
        st.session_state.player_cards = []

# 預測與紀錄
if len(st.session_state.banker_cards) > 0 and len(st.session_state.player_cards) > 0:
    result = predict_result(st.session_state.banker_cards, st.session_state.player_cards)
    color = {"莊": "red", "閒": "blue", "和或不下": "green"}[result]
    st.markdown(f"### 🎯 **預測結果：<span style='color:{color}'>{result}</span>**", unsafe_allow_html=True)

    if st.button("✅ 記錄此局預測結果"):
        st.session_state.records.append({
            "banker": st.session_state.banker_cards.copy(),
            "player": st.session_state.player_cards.copy(),
            "result": result
        })
        if mode == "累積預測":
            st.session_state.history.append(result)
        # 清除當局
        st.session_state.banker_cards = []
        st.session_state.player_cards = []
        st.experimental_rerun()
        if st.session_state.history:
    total = len(st.session_state.history)
    win_counts = Counter(st.session_state.history)
    banker_win = win_counts.get("莊", 0)
    player_win = win_counts.get("閒", 0)
    tie = win_counts.get("和或不下", 0)

    b_pct = banker_win / total * 100
    p_pct = player_win / total * 100
    t_pct = tie / total * 100

    st.markdown(f"""
    <div style='font-size:18px; line-height:1.8'>
        <b>📈 累積下注統計（共 {total} 局）</b><br>
        🟥 <b style='color:red'>莊</b>：{banker_win} 局（<b>{b_pct:.1f}%</b>)<br>
        🟦 <b style='color:blue'>閒</b>：{player_win} 局（<b>{p_pct:.1f}%</b>)<br>
        🟩 <b style='color:green'>和或不下</b>：{tie} 局（<b>{t_pct:.1f}%</b>)
    </div>
    """, unsafe_allow_html=True)
