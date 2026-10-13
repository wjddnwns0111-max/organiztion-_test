import streamlit as st
from pathlib import Path
from collections import Counter
import random

st.set_page_config(page_title="오피스 동물원 | 조직문화 취향 테스트", page_icon="🐾", layout="centered")
ASSETS = Path(__file__).parent / "assets"
TYPES = {
    "fox": {"name":"자유로운 발명가", "culture":"혁신문화", "emoji":"🦊", "color":"#FFF0E2",
            "tagline":"정해진 길보다 새로운 길을 만드는 게 좋아!",
            "intro":"새로운 아이디어가 떠오르면 직접 시도해 보고 싶어 하는 당신! 스스로 방법을 찾아가고 새로운 도전을 통해 성장하는 환경을 선호해요.",
            "good":["아이디어를 자유롭게 제안하는 회사","업무 방식에 자율성을 주는 회사","새로운 시도와 실험을 장려하는 회사"],
            "hard":["작은 결정에도 여러 단계의 승인이 필요한 환경","기존 방식만 고집하는 환경"]},
    "rabbit": {"name":"다정한 팀플레이어", "culture":"협력문화", "emoji":"🐰", "color":"#FFF0F4",
            "tagline":"혼자 빨리 가는 것보다 함께 멀리 가는 게 좋아!",
            "intro":"좋은 동료들과 함께할 때 일하는 즐거움이 커지는 당신! 서로 존중하고 도움을 주고받으며 함께 목표를 이루는 환경을 선호해요.",
            "good":["서로 존중하고 도와주는 회사","의견을 편하게 나누는 회사","팀의 성장도 중요하게 생각하는 회사"],
            "hard":["동료 간 경쟁만 지나치게 강조하는 환경","소통과 협력이 부족한 환경"]},
    "tiger": {"name":"열정적인 도전자", "culture":"성과문화", "emoji":"🐯", "color":"#FFF5DA",
            "tagline":"목표가 생기면 달성하고 싶어지는걸!",
            "intro":"명확한 목표가 있을 때 더욱 의욕이 생기는 당신! 노력한 만큼 인정받고 도전적인 목표를 달성하는 환경을 선호해요.",
            "good":["목표와 성과 기준이 명확한 회사","노력과 성과를 공정하게 인정하는 회사","도전적인 목표를 제시하는 회사"],
            "hard":["성과 피드백이 부족한 환경","목표가 불분명한 환경"]},
    "bear": {"name":"든든한 설계자", "culture":"위계문화", "emoji":"🐻", "color":"#E9F7EE",
            "tagline":"차근차근 계획대로 해내는 게 제일 좋아!",
            "intro":"체계적인 환경에서 일을 완성해 나가는 걸 좋아하는 당신! 역할과 책임이 분명하고 안정적인 시스템이 갖춰진 환경을 선호해요.",
            "good":["업무 절차와 역할이 명확한 회사","교육과 업무 시스템이 체계적인 회사","예측 가능한 환경을 제공하는 회사"],
            "hard":["업무 기준이 자주 바뀌는 환경","역할과 책임이 불분명한 환경"]},
}
# Choices are displayed in a fixed, varied order. Each maps to a culture type.
QUESTIONS = [
("두근두근 첫 출근! 가장 설레는 순간은?",[
("동료들이 먼저 다가와 반갑게 인사해 줄 때","rabbit"),("맡을 업무와 계획을 자세히 안내받을 때","bear"),("아이디어를 자유롭게 제안해도 된다는 말을 들을 때","fox"),("목표와 성과 보상에 대해 설명받을 때","tiger")]),
("입사 일주일 차, 첫 업무를 맡았다! 듣고 싶은 말은?",[
("새로운 방식으로 한번 도전해 봐요!","fox"),("업무 매뉴얼을 준비해 뒀어요.","bear"),("어려우면 팀원들과 함께 해결해 봐요.","rabbit"),("이번 업무의 목표와 평가 기준은 명확해요.","tiger")]),
("갑자기 하루 동안 팀장이 된다면?",[
("팀원들의 고민을 듣고 함께 점심 먹기","rabbit"),("새 프로젝트를 제안해 보기","fox"),("팀의 목표 달성 현황 살펴보기","tiger"),("업무 절차의 비효율 정리하기","bear")]),
("중요한 프로젝트 회의! 어떤 방식이 좋을까?",[
("안건과 순서에 따라 진행하기","bear"),("새로운 아이디어를 자유롭게 제안하기","fox"),("모두의 의견을 듣고 함께 결정하기","rabbit"),("목표 달성 전략부터 논의하기","tiger")]),
("프로젝트가 예상과 다르게 흘러간다!",[
("기존 계획과 절차를 점검한다","bear"),("새로운 방법을 빠르게 시도한다","fox"),("팀원들과 함께 해결책을 찾는다","rabbit"),("목표에 가장 효과적인 방법을 선택한다","tiger")]),
("새 복지제도 하나만 고른다면?",[
("성과에 따른 추가 인센티브","tiger"),("팀원들과 함께하는 활동 지원","rabbit"),("새 분야에 도전하는 자기계발 지원","fox"),("안정적인 생활을 돕는 복지 지원","bear")]),
("프로젝트 성공! 가장 듣고 싶은 칭찬은?",[
("새로운 시도가 인상적이었어요!","fox"),("서로 도와준 덕분에 성공했어요!","rabbit"),("목표를 120% 달성했네요!","tiger"),("일정과 절차를 정확히 관리했네요!","bear")]),
("회사에 새로운 업무 방식이 도입된다면?",[
("새로운 방식의 가능성이 기대된다","fox"),("팀원들이 잘 적응할지 살펴본다","rabbit"),("업무 성과가 얼마나 개선될지 궁금하다","tiger"),("변경된 절차와 기준부터 확인한다","bear")]),
("가장 이상적인 팀 분위기는?",[
("서로 편하게 도와주는 분위기","rabbit"),("새 시도를 자유롭게 하는 분위기","fox"),("성과를 인정하고 목표를 향하는 분위기","tiger"),("역할과 책임이 명확한 분위기","bear")]),
("회사에서 가장 중요하게 생각하는 가치는?",[
("안정성: 예측 가능한 환경","bear"),("자율성: 스스로 판단할 자유","fox"),("협력: 신뢰하며 함께 일하기","rabbit"),("성취: 목표 달성과 인정","tiger")]),
("친구에게 가장 자랑하고 싶은 회사의 모습은?",[
("동료들이 서로 잘 챙겨줘!","rabbit"),("아이디어를 마음껏 시도할 수 있어!","fox"),("노력한 만큼 인정받아!","tiger"),("업무 체계가 잘 잡혀 있어!","bear")]),
("마지막 질문! 가장 행복한 회사생활은?",[
("새로운 도전을 통해 성장하기","fox"),("좋은 동료들과 즐겁게 일하기","rabbit"),("목표를 달성하며 성취감 느끼기","tiger"),("안정적인 환경에서 계획대로 일하기","bear")]),
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');
html,body,[class*="css"],.stApp {font-family:'Nunito','Noto Sans KR',sans-serif!important;}
.stApp {background:linear-gradient(145deg,#FFF9F2,#FFF3EA 55%,#FFF9F2);color:#513E36}
.block-container {max-width:790px!important;padding:1.6rem 1.3rem 4rem!important;}
header[data-testid="stHeader"]{background:transparent}
h1,h2,h3,p,div,span{overflow-wrap:anywhere;word-break:keep-all;}
h1,h2,h3{color:#553A2D!important;letter-spacing:-.04em}
.stButton>button {width:100%;min-height:65px;height:auto!important;padding:15px 19px!important;white-space:normal!important;text-align:left!important;justify-content:flex-start!important;line-height:1.55!important;border-radius:19px!important;border:1.5px solid #F0DFD2!important;background:#FFFDFC!important;color:#533E33!important;font-size:1rem!important;font-weight:700!important;box-shadow:0 5px 13px rgba(115,73,47,.045);transition:.15s ease;}
.stButton>button p{white-space:normal!important;word-break:keep-all!important;overflow-wrap:anywhere!important;}
.stButton>button:hover{border-color:#F8AD8C!important;background:#FFF0E6!important;transform:translateY(-1px);}
.stButton>button[kind="primary"]{justify-content:center!important;text-align:center!important;background:linear-gradient(100deg,#FF986C,#FF704C)!important;color:white!important;border:0!important;}
.stButton>button[kind="primary"] p{color:white!important}
[data-testid="stImage"] img{max-width:100%;height:auto;border-radius:22px;object-fit:contain}
[data-testid="stProgress"] [role="progressbar"]>div{background:#FF9874!important}
.zoo-card{background:#FFFDF9;border:1px solid #F3E5D7;border-radius:24px;padding:21px 23px;margin:12px 0 18px;box-shadow:0 7px 20px rgba(113,73,50,.055);max-width:100%;}
.zoo-title{text-align:center;font-size:clamp(1.45rem,5vw,2.15rem);font-weight:900;color:#573B2C;margin:6px 0 8px;}
.zoo-sub{text-align:center;color:#8C7566;font-size:1rem;margin:0 0 16px;}
.zoo-kicker{color:#E67B51;font-weight:900;letter-spacing:.09em;font-size:.88rem}
.zoo-question{font-size:clamp(1.2rem,4.5vw,1.65rem);font-weight:900;line-height:1.5;color:#50392F;margin:10px 0 18px;}
.zoo-chip{display:inline-block;background:#FFE9DB;color:#BA6E4C;padding:7px 15px;border-radius:100px;font-weight:800;font-size:.84rem;}
.zoo-result{border-radius:26px;padding:18px 22px;background:#FFFDF9;border:1px solid #F0E0D2;margin-top:10px;max-width:100%;}
.zoo-result h3{margin-bottom:8px}
.zoo-result li{margin:7px 0;line-height:1.65}
.zoo-foot{text-align:center;color:#917C70;font-size:.8rem;line-height:1.7;margin-top:16px}
@media(max-width:600px){.block-container{padding:1rem .85rem 3rem!important}.zoo-card{padding:16px}.zoo-result{padding:15px}}
</style>
""",unsafe_allow_html=True)
if "page" not in st.session_state: st.session_state.page="home"
if "idx" not in st.session_state: st.session_state.idx=0
if "answers" not in st.session_state: st.session_state.answers={}
def restart():
    st.session_state.page="home";st.session_state.idx=0;st.session_state.answers={}
def select(kind):
    st.session_state.answers[st.session_state.idx]=kind
    st.session_state.idx+=1
    st.session_state.page="result" if st.session_state.idx>=len(QUESTIONS) else "quiz"
def decide():
    counts=Counter(st.session_state.answers.values())
    max_score=max(counts.values())
    tied=[k for k,v in counts.items() if v==max_score]
    winner=next(st.session_state.answers[i] for i in reversed(range(len(QUESTIONS))) if st.session_state.answers[i] in tied)
    return winner,counts,len(tied)>1

if st.session_state.page=="home":
    st.image(str(ASSETS/"hero.png"),use_container_width=True)
    st.markdown('<div class="zoo-title">🐾 나랑 찰떡인 회사는 어디일까?</div><div class="zoo-sub">12개의 질문으로 알아보는 나의 조직문화 취향!</div>',unsafe_allow_html=True)
    if st.button("🚀 테스트 시작하기",type="primary",use_container_width=True):
        st.session_state.idx=0;st.session_state.answers={};st.session_state.page="quiz";st.rerun()
    st.markdown('<div class="zoo-foot">⏱️ 약 2~3분 · 🐾 귀여운 동물 친구들과 함께해요!<br>CVF를 참고한 재미·자기탐색용 테스트이며 채용 적합성 검사가 아닙니다.</div>',unsafe_allow_html=True)
elif st.session_state.page=="quiz":
    idx=st.session_state.idx
    question,choices=QUESTIONS[idx]
    st.progress(idx/len(QUESTIONS))
    st.markdown(f'<div class="zoo-kicker">QUESTION {idx+1} / {len(QUESTIONS)}</div>',unsafe_allow_html=True)
    left, center, right = st.columns([0.35, 2.3, 0.35])
    with center:
        st.image(str(ASSETS/f"q{idx+1:02d}.jpg"), use_container_width=True)
    st.markdown(f'<div class="zoo-card"><div class="zoo-question">Q{idx+1}. {question}</div></div>',unsafe_allow_html=True)
    for letter,(label,kind) in zip('ABCD',choices):
        if st.button(f"{letter}   {label}",key=f"q{idx}_{kind}",use_container_width=True):
            select(kind);st.rerun()
    st.write("")
    if idx>0 and st.button("← 이전 질문",key="back"):
        st.session_state.idx-=1;st.session_state.answers.pop(st.session_state.idx,None);st.rerun()
else:
    winner,counts,tied=decide()
    d=TYPES[winner]
    st.markdown('<div class="zoo-title">🎉 당신의 조직문화 취향은?</div>',unsafe_allow_html=True)
    # Result illustration is displayed within the container; no fixed-width clipping.
    col_l,col_mid,col_r=st.columns([1,2,1])
    with col_mid:
        st.image(str(ASSETS/f"{winner}.png"),use_container_width=True)
    st.markdown(f'<div class="zoo-title">{d["emoji"]} {d["name"]}</div><div class="zoo-sub">{d["culture"]} · {d["tagline"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="zoo-result"><p style="font-size:1.03rem;line-height:1.85;margin:0">{d["intro"]}</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="zoo-result"><h3>💚 이런 회사가 찰떡이에요!</h3><ul>'+''.join(f'<li>{x}</li>' for x in d['good'])+'</ul></div>',unsafe_allow_html=True)
    st.markdown('<div class="zoo-result"><h3>💭 이런 환경은 조금 답답할지도?</h3><ul>'+''.join(f'<li>{x}</li>' for x in d['hard'])+'</ul></div>',unsafe_allow_html=True)
    if tied: st.caption("여러 유형의 점수가 같아, 마지막으로 선택한 동점 유형을 대표 결과로 보여줬어요.")
    st.markdown('<div class="zoo-foot">본 결과는 조직문화 선호를 탐색하는 콘텐츠입니다. 성격·능력·실제 회사 적합성을 진단하지 않아요.</div>',unsafe_allow_html=True)
    st.info("친구에게 공유하고 싶다면 브라우저 주소를 복사해 주세요. 링크를 받은 친구는 처음부터 테스트할 수 있어요.")
    if st.button("🔄 다시 테스트하기",type="primary",use_container_width=True):
        restart();st.rerun()
