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
# 登录后界面（非刷题状态）  
# ===============================
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False

# 如果已经进入刷题，则跳过所有欢迎界面
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

            # 自动识别
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

            mode = st.radio("选择模式：", ["顺序刷题", "随机刷题"])

            if st.button("开始刷题 🚀"):
                st.session_state.order_mode = mode
                st.session_state.quiz_started = True

                if mode == "顺序刷题":
                    st.session_state.quiz_index = 0
                else:
                    st.session_state.quiz_index = random.randint(
                        0, len(st.session_state.df_cache) - 1
                    )

                st.rerun()

    if feature == "🚀 其他功能（待更新）":
        st.info("敬请期待…")

    # 退出登录
    if st.button("退出登录"):
        st.session_state.logged_in = False
        st.rerun()

    st.stop()

# ===============================
#             纯净刷题模式
# ===============================

df = st.session_state.df_cache
idx = st.session_state.quiz_index
total = len(df)
row = df.iloc[idx]

st.write(f"### 🎯 题目 {idx + 1}/{total}")

# 题型
if st.session_state.question_type_col:
    st.write(f"**题型：{row[st.session_state.question_type_col]}**")

# 题干
st.write(f"**{row[st.session_state.question_col]}**")

# --- 用户作答输入部分 ---
option_cols = st.session_state.option_cols
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

if option_cols:
    user_answer = st.radio(
        "请选择一个选项：",
        option_cols,
        format_func=lambda c: f"{c}. {row[c]}",
        key=f"radio_{idx}"
    )
else:
    user_answer = st.text_input("请输入你的答案：", key=f"input_{idx}")

# --- 提交答案按钮 ---
if st.button("提交答案 ✔"):
    st.session_state.user_answer = user_answer
    st.session_state.show_result = True

# ===============================
# 显示判断结果 + 上一题 / 下一题
# ===============================
if "show_result" in st.session_state and st.session_state.show_result:

    correct = str(row[st.session_state.answer_col]).strip().upper()
    your_ans = str(st.session_state.user_answer).strip().upper()

    # 判断
    if your_ans == correct:
        st.success("🎉 回答正确！")
    else:
        st.error(f"❌ 回答错误！正确答案是：{correct}")

    # ---- 上一题 / 下一题 ----
    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⬅ 上一题"):
            st.session_state.quiz_index = max(0, idx - 1)
            st.session_state.show_result = False
            st.rerun()

    with col_next:
        if st.button("下一题 ➡"):
            if idx + 1 < total:
                st.session_state.quiz_index = idx + 1
            else:
                st.success("🎉 已经是最后一题啦！")
            st.session_state.show_result = False
            st.rerun()

# ===============================
#     额外功能：返回 / 重置
# ===============================

st.markdown("---")
st.subheader("⚙️ 操作")

col1, col2, col3 = st.columns(3)

# 返回功能选择（不清空题库，只回到菜单）
with col1:
    if st.button("返回功能选择 🔙"):
        st.session_state.quiz_started = False
        st.session_state.mode_selected = False
        st.rerun()

# 重新上传（清空题库缓存）
with col2:
    if st.button("重新上传题库 📁"):
        if "df_cache" in st.session_state:
            del st.session_state.df_cache
        st.session_state.quiz_started = False
        st.session_state.mode_selected = False
        st.rerun()

# 退出刷题（退出登录）
with col3:
    if st.button("退出系统 🚪"):
        st.session_state.clear()
        st.rerun()
