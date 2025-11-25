import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Aurora.1", page_icon="🔒")

# ===============================
# 登录状态初始化
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ===============================
# 登录界面
# ===============================
if not st.session_state.logged_in:
    st.title("🔒 Multifunctional Website")

    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        if username == "xlw" and password == "000000":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("用户名或密码错误！")
    st.stop()

# ===============================
# 登录后界面状态初始化
# ===============================
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False

# ===============================
# 登录后主界面
# ===============================
if not st.session_state.quiz_started:

    st.title("🔒 Multifunctional Website")
    st.success("Login succeeded！Aurora welcomes you 🎉")

    feature = st.selectbox(
        "✨ 请选择功能：",
        ["", "📝 刷题系统", "🚀 其他功能（待更新）"]
    )

    if feature == "":
        st.stop()

    # ------------------------
    # 刷题系统
    # ------------------------
    if feature == "📝 刷题系统":
        st.subheader("📘 刷题系统")

        uploaded_file = st.file_uploader("上传 Excel 题库", type=["xlsx"])

        if uploaded_file and not st.session_state.mode_selected:

            df = pd.read_excel(uploaded_file)
            st.session_state.df_cache = df

            st.success("文件上传成功！")

            # 自动识别列名
            question_type_col = None
            question_col = None
            answer_col = None
            option_cols = []

            for col in df.columns:
                col_lower = str(col).lower()
                if "题型" in col_lower:
                    question_type_col = col
                elif "题目" in col_lower:
                    question_col = col
                elif "答案" in col_lower:
                    answer_col = col
                elif col_lower in ["a", "b", "c", "d", "e", "f"]:
                    option_cols.append(col)

            st.write("🧭 自动识别字段：")
            st.write(f"- 题型列：{question_type_col}")
            st.write(f"- 题目列：{question_col}")
            st.write(f"- 答案列：{answer_col}")
            st.write(f"- 选项列：{option_cols}")

            if st.button("字段无误，继续 →"):
                st.session_state.question_col = question_col
                st.session_state.answer_col = answer_col
                st.session_state.question_type_col = question_type_col
                st.session_state.option_cols = option_cols
                st.session_state.mode_selected = True
                st.rerun()

        # 第二步：选择模式
        if st.session_state.mode_selected and not st.session_state.quiz_started:
            st.subheader("📌 请选择刷题模式")

            mode = st.radio("选择模式：", ["顺序刷题", "随机刷题（整套洗牌）"])

            if st.button("开始刷题 🚀"):
                st.session_state.order_mode = mode
                st.session_state.quiz_started = True

                total = len(st.session_state.df_cache)

                if mode == "顺序刷题":
                    st.session_state.quiz_index = 0

                else:
                    # 随机洗牌模式 B
                    st.session_state.random_order = list(range(total))
                    random.shuffle(st.session_state.random_order)
                    st.session_state.random_pos = 0
                    st.session_state.quiz_index = st.session_state.random_order[0]

                st.rerun()

    if feature == "🚀 其他功能（待更新）":
        st.info("敬请期待…")

    # 退出登录
    if st.button("退出登录"):
        st.session_state.logged_in = False
        st.rerun()

    st.stop()


# ===============================
#          纯净刷题界面
# ===============================

df = st.session_state.df_cache
idx = st.session_state.quiz_index
total = len(df)
row = df.iloc[idx]

# 当前题目编号
st.write(f"### 🎯 题目 {idx + 1}/{total}")

# 题型
if st.session_state.question_type_col:
    st.write(f"**题型：{row[st.session_state.question_type_col]}**")

# 题干
st.write(f"**{row[st.session_state.question_col]}**")

# --- 用户输入答案 ---
option_cols = st.session_state.option_cols

if option_cols:
    # 不默认选第一项："请选择" 占位项
    options_display = ["请选择"] + option_cols
    user_choose = st.radio(
        "请选择一个选项：",
        options_display,
        format_func=lambda c: " " if c == "请选择" else f"{c}. {row[c]}",
        key=f"radio_{idx}"
    )
    user_answer = "" if user_choose == "请选择" else user_choose
else:
    user_answer = st.text_input("请输入你的答案：", key=f"input_{idx}")

# --- 提交答案 ---
if st.button("提交答案 ✔"):
    st.session_state.user_answer = user_answer
    st.session_state.show_result = True

# ===============================
# 显示正确性 + 上一题/下一题
# ===============================
if st.session_state.get("show_result", False):

    # 支持多选题，例如 ACD
    correct = "".join(sorted(str(row[st.session_state.answer_col]).strip().upper()))
    your_ans = "".join(sorted(str(st.session_state.user_answer).strip().upper()))

    if your_ans == correct:
        st.success("🎉 回答正确！")
    else:
        st.error(f"❌ 回答错误！正确答案是：{correct}")

    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⬅ 上一题"):
            if st.session_state.order_mode == "顺序刷题":
                st.session_state.quiz_index = max(0, idx - 1)
            else:
                st.session_state.random_pos = max(0, st.session_state.random_pos - 1)
                st.session_state.quiz_index = st.session_state.random_order[
                    st.session_state.random_pos
                ]
            st.session_state.show_result = False
            st.rerun()

    with col_next:
        if st.button("下一题 ➡"):
            if st.session_state.order_mode == "顺序刷题":
                if idx + 1 < total:
                    st.session_state.quiz_index = idx + 1
            else:
                if st.session_state.random_pos + 1 < total:
                    st.session_state.random_pos += 1
                    st.session_state.quiz_index = st.session_state.random_order[
                        st.session_state.random_pos
                    ]
                else:
                    st.success("🎉 已经是最后一题啦！")
            st.session_state.show_result = False
            st.rerun()


# ===============================
# 返回/重置/退出
# ===============================
st.markdown("---")
st.subheader("⚙️ 操作")

col1, col2, col3 = st.columns(3)

# 返回功能选择
with col1:
    if st.button("返回功能选择 🔙"):
        st.session_state.quiz_started = False
        st.session_state.mode_selected = False
        st.rerun()

# 重新上传题库
with col2:
    if st.button("重新上传题库 📁"):
        st.session_state.clear()
        st.rerun()

# 退出系统
with col3:
    if st.button("退出系统 🚪"):
        st.session_state.clear()
        st.rerun()
