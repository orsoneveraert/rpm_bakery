import streamlit as st
import time
from streamlit.components.v1 import html
import beepy
import threading

# ... (keep all your existing imports and initial setup)

# Add these to your session state initialization
if 'alarm_thread' not in st.session_state:
    st.session_state.alarm_thread = None
if 'alarm_active' not in st.session_state:
    st.session_state.alarm_active = False

# Function to play alarm sound
def play_alarm():
    while st.session_state.alarm_active:
        beepy.beep(sound=1)  # You can change the sound number (1-7) for different sounds
        time.sleep(1)  # Wait for 1 second before playing again

# Modify your timer logic section
current_time = time.time()
if start_btn and not st.session_state.is_running:
    st.session_state.is_running = True
    st.session_state.alarm_active = False  # Stop alarm if running
    if st.session_state.start_time is None:
        st.session_state.start_time = current_time
        st.session_state.last_turn_update = current_time
elif pause_btn and st.session_state.is_running:
    st.session_state.is_running = False
    st.session_state.alarm_active = False  # Stop alarm if running
    st.session_state.elapsed_time += current_time - st.session_state.start_time
    st.session_state.start_time = None
elif reset_btn:
    st.session_state.is_running = False
    st.session_state.alarm_active = False  # Stop alarm if running
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.total_turns = 0
    st.session_state.last_turn_update = 0

# Modify the section where you display countdown or time over goal
if st.session_state.rpm_goal > 0:
    time_to_goal = max(0, st.session_state.countdown_time - elapsed)
    if time_to_goal > 0:
        st.info(f"{lang[st.session_state.language]['time_to_goal']}: {format_time(time_to_goal)}")
    elif time_to_goal == 0:
        st.success(lang[st.session_state.language]['goal_reached'])
        if not st.session_state.alarm_active:
            st.session_state.alarm_active = True
            st.session_state.alarm_thread = threading.Thread(target=play_alarm)
            st.session_state.alarm_thread.start()
    else:
        st.error(f"{lang[st.session_state.language]['time_over_goal']}: {format_time(abs(time_to_goal))}")

# At the end of your script, add:
if st.session_state.alarm_thread and not st.session_state.alarm_thread.is_alive():
    st.session_state.alarm_thread = None
