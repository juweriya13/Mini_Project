import streamlit as st
import pandas as pd
import sqlite3
from streamlit_calendar import calendar
from logiic import extract_event_details  

# Database setup
def init_db():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, summary TEXT, description TEXT, 
                  start_date TEXT, end_date TEXT, start_time TEXT, end_time TEXT, location TEXT)''')
    conn.commit()
    conn.close()
    
    
def insert_event(summary, description, start_date, end_date, start_time, end_time, location):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute('''INSERT INTO events (summary, description, start_date, end_date, start_time, end_time, location) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (summary or "No title", description or "No description", 
               start_date or "N/A", end_date or start_date, start_time or "00:00", end_time or "23:59", 
               location or "Unknown"))
    conn.commit()
    conn.close()


def delete_event(event_id):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


def get_events():
    conn = sqlite3.connect("events.db")
    df = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    return df

init_db()

# Streamlit UI
st.title("📅 Event Calendar")


with st.sidebar:
    st.header("➕ Add New Event")
    user_input = st.text_area("Describe your event (e.g., 'Meeting on March 25 at 9 AM at Hilton')")
    
    submit = st.button("Add Event")
    
    
    if submit:
        event_details = extract_event_details(user_input) 
        insert_event(event_details["summary"], event_details["description"], 
                     str(event_details["start_date"]), str(event_details["end_date"]), 
                     str(event_details["start_time"]), str(event_details["end_time"]), 
                     event_details["location"])
        st.success("Event added successfully!")
        st.rerun() 


events_df = get_events()
if not events_df.empty:
    events = []
    for _, row in events_df.iterrows():
        start_datetime = f"{row['start_date']}T{row['start_time']}:00" if row['start_time'] else row['start_date']
        end_datetime = f"{row['end_date']}T{row['end_time']}:00" if row['end_time'] else row['end_date']

        events.append({
            "id": row["id"],
            "title": row["summary"],
            "start": start_datetime,
            "end": end_datetime,
            "description": f"{row['description']}\nLocation: {row['location']}"
        })
    
    event_clicked = calendar(events=events, options={"editable": False})

    if event_clicked and "event" in event_clicked:
        event_id = event_clicked["event"]["id"]
        st.sidebar.write("### Event Details")
        st.sidebar.write(f"**Summary:** {event_clicked['event']['title']}")
        st.sidebar.write(f"**Description:** {event_clicked['event']['description']}")

        st.sidebar.write("### Delete Event")
        if st.sidebar.button("Delete Event"):
            delete_event(event_id)
            st.success("Event deleted successfully!")
            st.rerun()

