import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load questionnaire
@st.cache_data
def load_questions():
    df = pd.read_excel("DISC_Questionnaire_Bilingual_Reformat.xlsx")
    questions = df.groupby("Q#").apply(
        lambda group: {
            "question_zh": group["Question_ZH"].iloc[0],
            "question_en": group["Question_EN"].iloc[0],
            "options": list(zip(group["Option_Text"], group["DISC_Type"]))
        }
    ).tolist()
    return questions

questions = load_questions()

st.title("DISC Personality Test 測驗")
st.markdown("請依據每題的描述選擇最符合你的選項，最後會給你一份雷達圖分析結果。")

responses = []

with st.form("disc_form"):
    for i, q in enumerate(questions):
        st.markdown(f"### Q{i+1}: {q['question_zh']}")
        choice = st.radio("", [opt[0] for opt in q["options"]], key=f"q{i}")
        responses.append(choice)
    submitted = st.form_submit_button("提交測驗")

if submitted:
    df = pd.read_excel("DISC_Questionnaire_Bilingual_Reformat.xlsx")
    score = {"D": 0, "I": 0, "S": 0, "C": 0}
    for r in responses:
        disc_type = df[df["Option_Text"] == r]["DISC_Type"].values[0]
        score[disc_type] += 1

    # Display radar chart
    st.subheader("你的DISC測驗結果如下：")
    labels = list(score.keys())
    values = list(score.values())
    values += values[:1]  # close the radar chart
    labels += labels[:1]

    fig, ax = plt.subplots(subplot_kw={'polar': True})
    theta = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    ax.plot(theta, values)
    ax.fill(theta, values, alpha=0.3)
    ax.set_xticks(theta[:-1])
    ax.set_xticklabels(labels[:-1])
    st.pyplot(fig)

    # Interpretation
    sorted_types = sorted(score.items(), key=lambda x: x[1], reverse=True)
    main, sub = sorted_types[0][0], sorted_types[1][0]
    st.write(f"**主風格**: {main} | **次風格**: {sub}")

    explanations = {
        "D": "主導型：重視結果，喜歡掌控，直來直往",
        "I": "影響型：喜歡互動與表達，樂觀、有感染力",
        "S": "穩定型：重視關係，耐心傾聽，注重協調",
        "C": "謹慎型：重視品質與細節，邏輯思考，謹慎行事"
    }

    suggestions = {
        "D": "建議卡：避免過度強勢，傾聽他人意見，有助於團隊合作。",
        "I": "建議卡：注意實際執行與時間管理，避免過度樂觀。",
        "S": "建議卡：勇於表達立場，適時接受變化，有助於發展潛力。",
        "C": "建議卡：避免過度完美主義，放寬對他人的標準，更易建立關係。"
    }

    st.markdown(f"**個人特質說明**：{explanations[main]}")
    st.markdown(f"**建議卡**：{suggestions[main]}")
