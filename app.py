import streamlit as st

# 功能函式：計算加減值
def calc_count(cards):
    count = 0
    for c in cards:
        if c in ['2','3','A']:
            count -= 1
        elif c in ['4','5','6','7']:
            count += 1
    return count

# 預測下注方向
def predict_bet(count):
    if count >= 1:
        return "🥇 建議下注：莊"
    elif count <= -1:
        return "🥉 建議下注：閒"
    else:
        return "🔄 建議下注：和 或 不下注"

st.title("百家樂下注預測工具")

# 模式選擇
mode = st.radio("選擇模式：", ["單局預測", "累積加減追蹤"])

if mode == "單局預測":
    st.write("❗ 輸入最多 6 張牌，空著的欄位請留空")
    cards = [
        st.selectbox(f"第 {i+1} 張牌", ["","A","2","3","4","5","6","7","8","9","10","J","Q","K"])
        for i in range(6)
    ]
    if st.button("預測單局"):
        filtered = [c for c in cards if c]
        cnt = calc_count(filtered)
        st.write("🂠 本局牌：", filtered)
        st.write("📊 加減值：", cnt)
        st.success(predict_bet(cnt))

else:
    if 'history' not in st.session_state:
        st.session_state.history = []

    cols = st.columns(7)
    cols[0].button("＋ 重置累積", key="reset")
    cols[0].on_click(lambda: st.session_state.history.clear())
    for i in range(6):
        card = cols[i+1].selectbox(f"第 {i+1}", ["","A","2","3","4","5","6","7","8","9","10","J","Q","K"], key=f"sel{i}")
    if st.button("補牌到累積"):
        new_cards = [st.session_state[f"sel{i}"] for i in range(6) if st.session_state[f"sel{i}"]]
        st.session_state.history += new_cards

    st.write("🗃 目前累積牌牆：", st.session_state.history)
    cnt = calc_count(st.session_state.history)
    st.write("📈 累積加減值：", cnt)
    st.success(predict_bet(cnt))
