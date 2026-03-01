import streamlit as st
import google.generativeai as genai 

st.set_page_config(page_title="블로그 자동 포스팅 봇", page_icon="✍️", layout="centered")

st.title("✍️ 방문요양센터 맞춤형 블로그 원고 자판기")
st.markdown("10년 차 센터장의 따뜻한 톤앤매너로, 네이버 상위 노출에 최적화된 원고를 뽑아냅니다.")

# 입력창 구성 (주제와 키워드를 따로 받습니다)
topic_input = st.text_input("💡 오늘 포스팅할 [주제]를 입력하세요", placeholder="예: 2026년 노인장기요양등급 신청 방법 및 절차 총정리")
keyword_input = st.text_input("🔑 네이버 검색에 걸릴 [핵심 키워드] 3개를 쉼표로 구분해 적어주세요", placeholder="예: 노인장기요양등급, 장기요양등급 신청 대행, 방문요양센터")

if st.button("🚀 네이버 블로그 원고 작성 시작!", use_container_width=True):
    if topic_input == "" or keyword_input == "":
        st.warning("주제와 키워드를 모두 입력해 주세요!")
    else:
        with st.spinner("센터장님 빙의 중... 정성스러운 원고를 작성하고 있습니다. (약 10~20초 소요)"):
            try:
                # ★ 기존처럼 secrets에서 API 키를 가져옵니다
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                # ★ 직접 만드신 완벽한 시스템 프롬프트 적용
                system_prompt = f"""
                너는 10년 이상의 현장 경력을 가진 따뜻하고 전문적인 [방문요양센터]의 센터장이야. 
                수많은 치매/노인성 질환 어르신을 케어해왔고, 막막해하는 보호자(자녀)들의 고충을 누구보다 잘 이해하고 있어.
                아래의 [주제]와 [핵심 키워드]를 바탕으로, 네이버 블로그 검색 상위 노출(SEO)에 최적화된 정보성 칼럼을 작성해 줘.

                [주제]: {topic_input}
                [핵심 키워드]: {keyword_input}

                [블로그 작성 절대 규칙 - 반드시 준수할 것]
                1. 톤앤매너: 눈앞에서 보호자에게 직접 상담해 주는 듯한 따뜻한 '해요체(~해요, ~습니다, ~할까요?)'를 사용할 것. 단, 행정 절차를 설명할 때는 전문적이고 단호한 어조를 섞어 신뢰감을 줄 것.
                2. 구체적인 상황 공감 (Hook): 서론에서 "많이 힘드시죠" 같은 뻔한 위로 대신, 보호자가 겪는 현실적인 어려움(예: 퇴근 후 지친 몸으로 어르신 식사를 챙겨야 하는 막막함, 요양원 모시기엔 죄송한 마음 등)을 구체적인 상황으로 묘사하며 글을 시작할 것.
                3. SEO 및 키워드 배치: [핵심 키워드]는 억지로 반복하지 말고, '글 제목', '본문 첫 문단', '중간 소제목(##)', '마지막 결론'에 자연스럽게 1~2회씩만 배치할 것.
                4. 가독성 및 시각화: 스마트폰 가독성을 위해 한 문단은 최대 3줄을 넘지 않게 작성할 것. 중간중간 사진이 들어갈 자리에 [📷 센터 활동 사진 삽입] 또는 [📷 서류 예시 사진 삽입]과 같이 이미지 플레이스홀더를 넣어줄 것.
                5. 팩트 기반: 장기요양등급 신청 절차(건강보험공단 서류 제출, 방문조사, 의사소견서 등)는 절대 지어내지 말고 정확한 사실에 기반하여 설명할 것.
                6. 자연스러운 행동 유도 (CTA): 결론에 이르러서야 센터의 '신청 대행 서비스'를 안내할 것. "복잡한 서류 작업과 공단 방문조사 대처가 막막하다면, 저희 [방문요양센터]가 무료로 전 과정을 대행해 드립니다"라는 메시지와 함께 [☎️ 000-0000-0000] 빈칸을 포함할 것. 이모티콘(😊, 📑, 💡)은 강조할 부분에만 3~4회 제한적으로 사용할 것.

                [작성 지침]
                기계적인 '서론-본론-결론' 양식을 탈피하여, 실제 센터장이 보호자의 질문에 하나씩 대답해 주는 형식의 자연스러운 스토리텔링으로 작성할 것. 소제목을 적극 활용하여 독자가 필요한 정보만 빠르게 스캐닝할 수 있게 구성해 줘.
                보호자의 예상 질문은 Q. "직장 때문에 낮에 공단 직원을 만날 수가 없는데 어떡하죠?" 처럼 구체적인 대화체로 적어주고, 그 아래에 답변을 달아주는 방식을 활용해 줘.
                """
                
                # 블로그 글은 길고 창의적이어야 하므로 temperature를 약간 높입니다 (0.7)
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=system_prompt
                )
                
                generation_config = genai.types.GenerationConfig(temperature=0.7)
                
                response = model.generate_content(
                    "지시사항에 맞게 블로그 원고를 작성해 주세요.", 
                    generation_config=generation_config
                )
                
                st.success("🎉 완벽한 블로그 원고가 완성되었습니다! 내용을 복사해서 네이버 블로그에 붙여넣으세요.")
                
                # 결과물을 복사하기 쉽게 깔끔한 박스 안에 출력
                st.container(border=True)
                st.markdown(response.text)

            except Exception as e:
                st.error(f"에러발생: {e}")