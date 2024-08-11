import streamlit as st
import time

# Set page config for dark theme compatibility
st.set_page_config(page_title="Mixer Timer and RPM Counter", layout="wide")

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'rpm' not in st.session_state:
    st.session_state.rpm = 0
if 'mixers' not in st.session_state:
    st.session_state.mixers = []
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'total_turns' not in st.session_state:
    st.session_state.total_turns = 0
if 'last_turn_update' not in st.session_state:
    st.session_state.last_turn_update = 0
if 'rpm_goal' not in st.session_state:
    st.session_state.rpm_goal = 0
if 'countdown_time' not in st.session_state:
    st.session_state.countdown_time = 0
if 'goal_reached' not in st.session_state:
    st.session_state.goal_reached = False
if 'notified' not in st.session_state:
    st.session_state.notified = False

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def calculate_turns(seconds, rpm):
    return (seconds / 60) * rpm

def play_notification_sound():
    html_string = """
    <audio autoplay style="display:none;">
      <source src="https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3" type="audio/mp3">
    </audio>
    """
    sound = st.empty()
    sound.markdown(html_string, unsafe_allow_html=True)
    time.sleep(2)  # wait for 2 seconds to finish the playing of the audio
    sound.empty()  # delete the element afterwards

def trigger_notification():
    st.balloons()
    play_notification_sound()

# Language dictionary
lang = {
    'en': {
        'title': "Mixer Timer and RPM Counter",
        'start': "Start",
        'pause': "Pause",
        'reset': "Reset",
        'enter_rpm': "Enter RPM",
        'turns': "turns",
        'save_mixer': "Save Mixer Speeds",
        'mixer_name': "Mixer Name",
        'speed': "Speed",
        'save': "Save Mixer",
        'saved_mixers': "Saved Mixers",
        'delete': "Delete",
        'language': "Language",
        'rpm_goal': "RPM Goal",
        'set_goal': "Set Goal",
        'time_to_goal': "Time to Goal",
        'goal_reached': "Goal Reached!",
        'time_over_goal': "Time Over Goal"
    },
    'fr': {
        'title': "Minuteur et Compteur de TPM du Mélangeur",
        'start': "Démarrer",
        'pause': "Pause",
        'reset': "Réinitialiser",
        'enter_rpm': "Entrer TPM",
        'turns': "tours",
        'save_mixer': "Enregistrer les Vitesses du Mélangeur",
        'mixer_name': "Nom du Mélangeur",
        'speed': "Vitesse",
        'save': "Enregistrer le Mélangeur",
        'saved_mixers': "Mélangeurs Enregistrés",
        'delete': "Supprimer",
        'language': "Langue",
        'rpm_goal': "Objectif TPM",
        'set_goal': "Définir Objectif",
        'time_to_goal': "Temps jusqu'à l'Objectif",
        'goal_reached': "Objectif Atteint !",
        'time_over_goal': "Temps Au-delà de l'Objectif"
    }
}

# App layout
st.title(lang[st.session_state.language]['title'])

# Timer display
timer_display = st.empty()
rpm_counter = st.empty()

# Timer controls
col1, col2, col3 = st.columns(3)
with col1:
    start_btn = st.button(lang[st.session_state.language]['start'])
with col2:
    pause_btn = st.button(lang[st.session_state.language]['pause'])
with col3:
    reset_btn = st.button(lang[st.session_state.language]['reset'])

# RPM input and goal setting
col1, col2 = st.columns(2)
with col1:
    new_rpm = st.number_input(lang[st.session_state.language]['enter_rpm'], min_value=0, value=st.session_state.rpm, step=1)
with col2:
    rpm_goal = st.number_input(lang[st.session_state.language]['rpm_goal'], min_value=0, value=st.session_state.rpm_goal, step=1)
    if st.button(lang[st.session_state.language]['set_goal']):
        st.session_state.rpm_goal = rpm_goal
        if st.session_state.rpm > 0:
            st.session_state.countdown_time = (rpm_goal / st.session_state.rpm) * 60
        st.session_state.goal_reached = False
        st.session_state.notified = False

# Timer logic
current_time = time.time()
if start_btn and not st.session_state.is_running:
    st.session_state.is_running = True
    if st.session_state.start_time is None:
        st.session_state.start_time = current_time
        st.session_state.last_turn_update = current_time
    st.session_state.notified = False  # Reset notification when starting
elif pause_btn and st.session_state.is_running:
    st.session_state.is_running = False
    st.session_state.elapsed_time += current_time - st.session_state.start_time
    st.session_state.start_time = None
    st.session_state.notified = False  # Reset notification when pausing
elif reset_btn:
    st.session_state.is_running = False
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.total_turns = 0
    st.session_state.last_turn_update = 0
    st.session_state.goal_reached = False
    st.session_state.notified = False

# Calculate current time and turns
if st.session_state.is_running:
    elapsed = current_time - st.session_state.start_time + st.session_state.elapsed_time
    new_turns = calculate_turns(current_time - st.session_state.last_turn_update, st.session_state.rpm)
    st.session_state.total_turns += new_turns
    st.session_state.last_turn_update = current_time
else:
    elapsed = st.session_state.elapsed_time

# Update RPM if changed
if new_rpm != st.session_state.rpm:
    st.session_state.rpm = new_rpm
    if st.session_state.is_running:
        st.session_state.last_turn_update = current_time
    if st.session_state.rpm_goal > 0:
        st.session_state.countdown_time = (st.session_state.rpm_goal / st.session_state.rpm) * 60

# Update displays
timer_display.header(format_time(elapsed))
rpm_counter.subheader(f"{int(st.session_state.total_turns)} {lang[st.session_state.language]['turns']}")

# Display countdown or time over goal
if st.session_state.rpm_goal > 0:
    time_to_goal = max(0, st.session_state.countdown_time - elapsed)
    if time_to_goal > 0:
        st.info(f"{lang[st.session_state.language]['time_to_goal']}: {format_time(time_to_goal)}")
    elif time_to_goal == 0 and not st.session_state.goal_reached:
        st.success(lang[st.session_state.language]['goal_reached'])
        if not st.session_state.notified:
            trigger_notification()
            st.session_state.notified = True
        st.session_state.goal_reached = True
    elif time_to_goal == 0:
        st.success(lang[st.session_state.language]['goal_reached'])
    else:
        st.error(f"{lang[st.session_state.language]['time_over_goal']}: {format_time(abs(time_to_goal))}")

# Save Mixer Speeds
st.header(lang[st.session_state.language]['save_mixer'])
mixer_name = st.text_input(lang[st.session_state.language]['mixer_name'])
speed1 = st.number_input(f"{lang[st.session_state.language]['speed']} 1", min_value=0, step=1)
speed2 = st.number_input(f"{lang[st.session_state.language]['speed']} 2", min_value=0, step=1)
speed3 = st.number_input(f"{lang[st.session_state.language]['speed']} 3", min_value=0, step=1)

if st.button(lang[st.session_state.language]['save']):
    speeds = [s for s in [speed1, speed2, speed3] if s > 0]
    if mixer_name and speeds:
        st.session_state.mixers.append({"name": mixer_name, "speeds": speeds})
        st.success(f"Mixer '{mixer_name}' saved successfully!")

# Display Saved Mixers
st.header(lang[st.session_state.language]['saved_mixers'])
for i, mixer in enumerate(st.session_state.mixers):
    with st.expander(f"{mixer['name']}"):
        for speed in mixer['speeds']:
            if st.button(f"{speed} RPM", key=f"speed_{i}_{speed}"):
                st.session_state.rpm = speed
                if st.session_state.is_running:
                    st.session_state.last_turn_update = time.time()
                if st.session_state.rpm_goal > 0:
                    st.session_state.countdown_time = (st.session_state.rpm_goal / speed) * 60
        if st.button(lang[st.session_state.language]['delete'], key=f"delete_{i}"):
            st.session_state.mixers.pop(i)
            st.rerun()

# Language selection
st.sidebar.selectbox(lang[st.session_state.language]['language'], ['English', 'Français'], 
                     index=0 if st.session_state.language == 'en' else 1,
                     on_change=lambda: setattr(st.session_state, 'language', 'en' if st.session_state.language == 'fr' else 'fr'))

# Ensure continuous updates
if st.session_state.is_running:
    time.sleep(0.1)
    st.rerun()

# Rerun the app if the goal is newly reached
if st.session_state.goal_reached and not st.session_state.notified:
    st.rerun()
