import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load questionnaire
@st.cache_data
def load_questions():
    df = pd.read_excel('DISC_Questionnaire_Bilingual_Reformat.xlsx')
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

    trait_combinations = {
        "DI": ("領導型影響者：你有領導與激勵他人的能力，善於推動目標與帶動氛圍。",
                "發展方向：平衡速度與細節，提升傾聽與組織力。"),
        "DS": ("堅定型領導者：你具行動力與穩定性，重視責任感，能推進任務。",
                "發展方向：學習更多人際互動技巧，建立柔性溝通能力。"),
        "DC": ("果斷型分析者：具備目標導向與邏輯思維，重視效率與結構。",
                "發展方向：強化團隊合作，尊重多元意見，避免過度批判。"),
        "ID": ("影響型推動者：樂於互動、具感染力與企圖心，能激發團隊活力。",
                "發展方向：增進紀律與專注力，避免分心與衝動。"),
        "IS": ("支持型溝通者：你善於營造良好氛圍，關注他人感受，重視和諧。",
                "發展方向：學習設定界線與展現立場，提升執行效率。"),
        "IC": ("創意型分析者：樂於表達又重視邏輯，擅長創新與規劃。",
                "發展方向：避免理想化與忽略現實需求，提升執行力。"),
        "SD": ("穩健型行動者：你具實踐力與忠誠度，重視團隊與任務平衡。",
                "發展方向：提升主動性與改變的彈性。"),
        "SI": ("溫和型影響者：善於傾聽與鼓舞他人，重視關係經營。",
                "發展方向：加強目標設定與決策效率。"),
        "SC": ("協調型分析者：你重視穩定與精準，善於支持與評估。",
                "發展方向：學習面對挑戰與適時展現自信。"),
        "CD": ("挑戰型領導者：你務實果斷，勇於突破與創新。",
                "發展方向：增進包容性與合作意識，減少衝突。"),
        "CI": ("邏輯型說服者：善於組織與表達，能影響他人看法。",
                "發展方向：強化團隊精神與情緒敏感度。"),
        "CS": ("內斂型穩定者：細心謹慎且具穩定性，支持他人達成任務。",
                "發展方向：嘗試主動發聲與表現自我，接受不確定性。")
    }

    explanations = {
        "D": "主導型：重視結果，喜歡掌控，直來直往",
        "I": "影響型：喜歡互動與表達，樂觀、有感染力",
        "S": "穩定型：重視關係，耐心傾聽，注重協調",
        "C": "謹慎型：重視品質與細節，邏輯思考，謹慎行事"
    }

    pair_key = main + sub
    if pair_key not in trait_combinations:
        pair_key = sub + main

    trait_text, growth_text = trait_combinations.get(pair_key, ("特質組合暫無定義。", "請洽顧問進一步解釋。"))

    st.markdown(f"**個人特質說明**：{explanations[main]} + {explanations[sub]}")
    st.markdown(f"**綜合特質**：{trait_text}")
    st.markdown(f"**建議方向**：{growth_text}")

