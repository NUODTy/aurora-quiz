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
# 全局状态初始化
# ===============================
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False


# ===============================
# 登录后 → 功能界面
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

    # =========================================
    # 刷题系统
    # =========================================
    if feature == "📝 刷题系统":
        st.subheader("📘 刷题系统")

        uploaded_file = st.file_uploader("上传 Excel 题库", type=["xlsx"])

        if uploaded_file and not st.session_state.mode_selected:

            df = pd.read_excel(uploaded_file)
            st.session_state.df_cache = df

            st.success("文件上传成功！")

            # 自动识别字段
            question_type_col = None
            question_col = None
            answer_col = None
            bank_col = None
            option_cols = []

            for col in df.columns:
                low = str(col).lower()

                if "题型" in low:
                    question_type_col = col
                elif "题库" in low or "来源" in low:
                    bank_col = col
                elif "题目" in low:
                    question_col = col
                elif "答案" in low:
                    answer_col = col
                elif low in ["a", "b", "c", "d", "e", "f"]:
                    option_cols.append(col)

            st.write("🧭 自动识别字段：")
            st.write(f"- 题型列：{question_type_col}")
            st.write(f"- 题库列：{bank_col}")
            st.write(f"- 题目列：{question_col}")
            st.write(f"- 答案列：{answer_col}")
            st.write(f"- 选项列：{option_cols}")

            if st.button("字段无误，继续 →"):
                st.session_state.question_col = question_col
                st.session_state.answer_col = answer_col
                st.session_state.question_type_col = question_type_col
                st.session_state.option_cols = option_cols
                st.session_state.bank_col = bank_col
                st.session_state.mode_selected = True
                st.rerun()

        # ====================================
        # 第二步：选择模式
        # ====================================
        if st.session_state.mode_selected and not st.session_state.quiz_started:
            st.subheader("📌 请选择刷题模式")

            mode = st.radio("选择模式：", ["顺序刷题", "随机刷题（每题都随机）"])

            if st.button("开始刷题 🚀"):

                total = len(st.session_state.df_cache)

                # 顺序刷题
                if mode == "顺序刷题":
                    st.session_state.order_mode = "顺序刷题"
                    st.session_state.quiz_index = 0

                # 随机刷题（序列随机，每题都随机）
                else:
                    st.session_state.order_mode = "随机刷题"
                    st.session_state.random_order = random.sample(range(total), total)
                    st.session_state.quiz_index = 0

                st.session_state.quiz_started = True
                st.rerun()

    if feature == "🚀 其他功能（待更新）":
        st.info("敬请期待…")

    # 退出登录
    if st.button("退出登录"):
        st.session_state.logged_in = False
        st.rerun()

    st.stop()


# ===============================
#           纯净刷题界面
# ===============================

df = st.session_state.df_cache
total = len(df)

# 取题目编号（顺序或随机）
if st.session_state.order_mode == "随机刷题":
    real_idx = st.session_state.random_order[st.session_state.quiz_index]
else:
    real_idx = st.session_state.quiz_index

row = df.iloc[real_idx]

# 展示题目进度
st.write(f"### 🎯 题目 {st.session_state.quiz_index + 1}/{total}")

# 显示题库列
if st.session_state.bank_col:
    st.write(f"📚 **题库：{row[st.session_state.bank_col]}**")

# 显示题型
if st.session_state.question_type_col:
    st.write(f"**题型：{row[st.session_state.question_type_col]}**")

# 显示题干
st.write(f"**{row[st.session_state.question_col]}**")


# =======================================
# 用户作答部分
# =======================================
option_cols = st.session_state.option_cols

if "user_answer" not in st.session_state:
    st.session_state.user_answer = []

# --- 多选题 OR 单选题 ---
correct_answer = str(row[st.session_state.answer_col]).strip().upper()

is_multi = len(correct_answer) > 1

if option_cols:

    if is_multi:
        st.info("📌 这是多选题，请选择多个选项")

        user_answer = st.multiselect(
            "请选择选项：",
            option_cols,
            default=None,
            format_func=lambda c: f"{c}. {row[c]}"
        )
    else:
        user_answer = st.radio(
            "请选择一个选项：",
            option_cols,
            index=None,   # ❗ 不默认选第一个
            format_func=lambda c: f"{c}. {row[c]}"
        )

else:
    user_answer = st.text_input("请输入你的答案：")


# --- 提交答案按钮 ---
if st.button("提交答案 ✔"):
    st.session_state.user_answer = user_answer
    st.session_state.show_result = True


# ===============================
# 判断结果
# ===============================
if "show_result" in st.session_state and st.session_state.show_result:

    your_ans = st.session_state.user_answer

    # --- 多选题判断 ---
    if is_multi:
        your_ans_str = "".join(sorted([x.upper() for x in your_ans]))
        correct_sorted = "".join(sorted(correct_answer))

        if your_ans_str == correct_sorted:
            st.success("🎉 回答正确！（多选）")
        else:
            st.error(f"❌ 回答错误！正确答案是：{correct_answer}")

    # --- 单选题判断 ---
    else:
        if str(your_ans).upper() == correct_answer:
            st.success("🎉 回答正确！")
        else:
            st.error(f"❌ 回答错误！正确答案是：{correct_answer}")

    # 上一题 / 下一题
    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⬅ 上一题"):
            st.session_state.quiz_index = max(0, st.session_state.quiz_index - 1)
            st.session_state.show_result = False
            st.rerun()

    with col_next:
        if st.button("下一题 ➡"):
            st.session_state.quiz_index += 1

            if st.session_state.quiz_index >= total:
                st.success("🎉 已刷完全部题目")
            else:
                st.session_state.show_result = False
                st.rerun()


# ===============================
# 底部操作栏
# ===============================
st.markdown("---")
st.subheader("⚙️ 操作")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("返回功能选择 🔙"):
        st.session_state.quiz_started = False
        st.session_state.mode_selected = False
        st.rerun()

with col2:
    if st.button("重新上传题库 📁"):
        if "df_cache" in st.session_state:
            del st.session_state.df_cache
        st.session_state.quiz_started = False
        st.session_state.mode_selected = False
        st.rerun()

with col3:
    if st.button("退出系统 🚪"):
        st.session_state.clear()
        st.rerun()
