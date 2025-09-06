import streamlit as st
from icalendar import Calendar


n = st.selectbox("Select number of courses", list(range(1, 11)))

st.write("Courses:", n)

courses = {}
for i in range(n):
    slot = st.text_input("Enter your slot (e.g., A, B, C)", "", key = f's{i}', max_chars=1).upper()
    course_name = st.text_input("Enter your course code", "", key=f'c{i}', max_chars=6).upper()
    courses[slot] = course_name 

    if st.button("Submit", key=f'submit{i}'):
        st.success('Course Added')


# Open the ICS file
with open('Timetable.ics', 'rb') as f:
    cal = Calendar.from_ical(f.read())

def change_event_name(component, course_name):
    component['SUMMARY'] = course_name

for component in cal.walk():
	if component.name == "VEVENT":
		if component.get("summary") in courses:
			change_event_name(component, courses[component.get("summary")])
		else:
			cal.subcomponents.remove(component)
                  
if st.button("Submit All"):
    st.success('All Courses Added')

    st.write("Your courses have been added to the calendar. Download the updated calendar and import it into your calendar application.")
    
    st.download_button('Download this semesters calendar', cal.to_ical(), file_name='NewCalendar.ics', icon=":material/download:")
