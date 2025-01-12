# main.py

from chatbot_functions import events_by_date, lectures_by_discipline, room_for_event, lecture_dates, disciplines_in_room, events_by_day, lecturer_for_date, laboratory_sessions, events_in_time_range, laboratory_event_dates

def handle_user_input():
    # Print the list of questions once at the start
    print("Choose a question:")
    print("1. What events are scheduled for a specific date?")
    print("2. What time are the lectures for a specific discipline?")
    print("3. Which room is assigned for a specific type of event on a given date?")
    print("4. When are the lectures for a specific discipline?")
    print("5. Which disciplines are held in a specific room?")
    print("6. List all events on a specific day of the week (e.g., Sunday)")
    print("7. Who is the lecturer for the lectures on a specific date?")
    print("8. What are the laboratory sessions for a specific discipline?")
    print("9. Which events are scheduled in a specific time range?")
    print("10. List all dates for laboratory events.")
    print("Type 'stop' to exit.")
    
    while True:
        # Prompt the user to choose a question by number
        choice = input("Enter the number of your question or 'stop' to exit: ")

        if choice.lower() == 'stop':
            print("Exiting program...")
            break  # Exit the loop if the user types 'stop'
        
        if choice == "1":
            date = input("Enter the date (e.g., 19.10.2024): ")
            print(events_by_date(date))
        elif choice == "2":
            discipline = input("Enter the discipline: ")
            print(lectures_by_discipline(discipline))
        elif choice == "3":
            event_type = input("Enter the event type (e.g., лекции): ")
            date = input("Enter the date (e.g., 19.10.2024): ")
            print(room_for_event(event_type, date))
        elif choice == "4":
            discipline = input("Enter the discipline: ")
            print(lecture_dates(discipline))
        elif choice == "5":
            room = input("Enter the room: ")
            print(disciplines_in_room(room))
        elif choice == "6":
            day_of_week = input("Enter the day of the week (e.g., неделя): ")
            print(events_by_day(day_of_week))
        elif choice == "7":
            date = input("Enter the date (e.g., 19.10.2024): ")
            print(lecturer_for_date(date))
        elif choice == "8":
            discipline = input("Enter the discipline: ")
            print(laboratory_sessions(discipline))
        elif choice == "9":
            start_time = input("Enter the start time (e.g., 9:00): ")
            end_time = input("Enter the end time (e.g., 17:30): ")
            print(events_in_time_range(start_time, end_time))
        elif choice == "10":
            print(laboratory_event_dates())
        else:
            print("Invalid choice")

handle_user_input()
