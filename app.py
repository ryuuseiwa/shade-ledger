"""Shade Ledger — outdoor-first, local open-weight AI field missions."""
from datetime import datetime
import json
from pathlib import Path
import streamlit as st
from engine import MODEL, MissionInput, generate_mission, local_summary, shade_score

DATA = Path(__file__).parent / 'data' / 'field_notes.jsonl'
st.set_page_config(page_title='Shade Ledger | Touch Grass', page_icon='🌿', layout='wide')
st.markdown('''<style>
.stApp {background: #f4f6ee; color: #183d32;} [data-testid="stSidebar"] {background:#e2ebd9;}
.block-container {max-width: 1080px; padding-top: 2rem;} h1,h2,h3 {color:#1e4738;}
h1 {font-family: Georgia, serif; letter-spacing:-1.5px;} p {line-height: 1.7;}
[data-testid="stMetric"] {background:#fff; border:1px solid #d5e4cd; border-radius:14px; padding:14px;}
.stButton>button[kind="primary"] {background:#1f654b;border:none;color:white;}
div[data-testid="stAlert"] {border-radius:12px;}
</style>''', unsafe_allow_html=True)

st.caption('OPEN-WEIGHT AI  /  LOCAL-FIRST FIELDWORK  /  NO GPS')
st.title('🌿 Shade Ledger')
st.markdown('**Less scrolling. More noticing.** Turn a short trip outdoors into a tiny, useful neighborhood observation. Your private field notes stay on this computer.')
st.info('Safety first: check real weather and heat advisories yourself. Stay in safe public areas; avoid traffic, private property, and heat exposure. This app has no live weather data.')

with st.sidebar:
    st.header('Your field kit')
    st.markdown('**AI:** Qwen2.5 1.5B Instruct via local Ollama')
    model = st.text_input('Installed Ollama model', value=MODEL, help='Change only to an installed compatible model.')
    st.markdown('No login • No paid API • No GPS • No cloud upload by this app')
    st.caption('The model download and Python setup require internet once; subsequent model inference is local.')
    st.divider()
    st.markdown('**How to read your score**')
    st.caption('Shade share is a simple count of your chosen stops, not measured canopy cover, heat, air quality, or environmental impact.')

tab1, tab2, tab3 = st.tabs(['01  Plan & go', '02  Field receipt', '03  My local ledger'])
with tab1:
    st.subheader('Build a tiny outdoor mission')
    a,b = st.columns(2)
    with a:
        minutes = st.slider('Time outdoors (minutes)', 5, 30, 15, 5)
        environment = st.selectbox('Where can you go?', ['Neighborhood sidewalks','Public park','Campus paths','Apartment courtyard','Accessible outdoor area'])
        mobility = st.selectbox('How will you explore?', ['Walking','Wheelchair-friendly stationary or rolling route','Seated outdoor observation','Slow stroll'])
    with b:
        focus = st.selectbox('What do you want to notice?', ['Shade & urban heat','Trees & biodiversity','Rainwater & drainage','Urban nature & well-being','Litter & public-space care'])
        energy = st.selectbox('Today’s pace', ['Low-key','Curious','Active'])
        climate = st.selectbox('Climate context (not live weather)', ['Warm climate','Temperate climate','Cool climate','Unsure'])
    if st.button('✨ Generate my offline AI mission', type='primary', use_container_width=True):
        try:
            with st.spinner('Asking your locally installed open-weight model…'):
                st.session_state['mission'] = generate_mission(MissionInput(minutes, environment, mobility, focus, energy, climate), model=model)
            st.session_state['mission_spec'] = {'minutes':minutes,'focus':focus,'environment':environment}
        except Exception as e:
            st.error(f'Local model unavailable or invalid output: {e}')
            st.code('ollama pull qwen2.5:1.5b-instruct')
    if 'mission' in st.session_state:
        m=st.session_state['mission']
        st.success('Mission ready. Read it once, close your laptop, and go outside.')
        st.subheader('🍃 '+m['title'])
        st.write(m['mission'])
        for i, step in enumerate(m['steps'], 1): st.write(f'**{i}.** {step}')
        st.markdown('**Notice these:** '+ ' · '.join(m['notice']))
        st.markdown('**One question for later:** '+m['reflection'])
        card = '\n'.join([f"# {m['title']}",m['mission'],* [f'{i}. {x}' for i,x in enumerate(m['steps'],1)],'Notice: '+', '.join(m['notice']),'Reflect: '+m['reflection']])
        st.download_button('⬇ Save a mission card (.txt)', card, 'shade-ledger-mission.txt', 'text/plain')
        st.caption('Take the text card if useful; your goal is to keep the screen off during the activity.')
    else:
        st.caption('Requires Ollama running locally. No canned fake “AI response” is substituted.')

with tab2:
    st.subheader('Make a 60-second field receipt')
    st.caption('After you come back, log what YOU noticed. No photo uploads or precise coordinates needed.')
    left,right=st.columns(2)
    with left:
        total=st.number_input('Observation stops', min_value=1,max_value=30,value=4,step=1)
        shaded=st.number_input('Stops that felt shaded', min_value=0,max_value=30,value=2,step=1)
    with right:
        green=st.number_input('Planted / permeable surface spots noticed',min_value=0,max_value=100,value=2,step=1)
        water=st.number_input('Drainage / water features noticed',min_value=0,max_value=100,value=1,step=1)
    feeling=st.select_slider('How did being outside feel?',options=['Draining','Neutral','Refreshing','Energizing'],value='Refreshing')
    notes=st.text_area('Optional reflection (avoid names / addresses)',max_chars=500,placeholder='The shaded sidewalk felt noticeably more comfortable…')
    score=shade_score(shaded,total)
    if score is None: st.warning('Shaded stops cannot exceed total stops.')
    else:
        st.metric('Observed shade share',f'{score}%')
        st.caption(local_summary(shaded,total,green,water))
    if st.button('📗 Save local field receipt', type='primary',disabled=score is None):
        record={'timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'shaded':shaded,'total':total,
                'shade_share_pct':score,'green_spots':green,'drainage_spots':water,'feeling':feeling,
                'reflection':notes,'mission_title':st.session_state.get('mission',{}).get('title','Independent field visit')}
        try:
            DATA.parent.mkdir(parents=True,exist_ok=True)
            with DATA.open('a',encoding='utf-8') as f: f.write(json.dumps(record,ensure_ascii=False)+'\n')
            st.success('Saved to data/field_notes.jsonl on this computer.')
        except OSError as e: st.error(f'Could not save: {e}')

with tab3:
    st.subheader('Your private neighborhood ledger')
    rows=[]
    if DATA.exists():
        for line in DATA.read_text(encoding='utf-8').splitlines():
            try: rows.append(json.loads(line))
            except json.JSONDecodeError: continue
    if rows:
        c1,c2,c3=st.columns(3)
        c1.metric('Outdoor field visits',len(rows))
        c2.metric('Stops observed',sum(r.get('total',0) for r in rows))
        c3.metric('Total shaded stops',sum(r.get('shaded',0) for r in rows))
        st.dataframe(list(reversed(rows)),use_container_width=True,hide_index=True)
        st.download_button('⬇ Export my data as JSON',json.dumps(rows,indent=2,ensure_ascii=False),'my-shade-ledger.json','application/json')
        st.caption('Entries never leave this machine unless you choose to export/share them. Delete the data folder locally to erase records.')
    else: st.info('No observations yet. Generate a mission, go outside, and come back with your first field receipt.')

st.divider()
st.caption('Built for Hacktoberfest Touch Grass • An observational citizen-science-inspired prototype, not a validated environmental monitoring tool.')
