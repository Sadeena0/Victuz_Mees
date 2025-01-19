from Dijkstra import *

demograph = {
    'A': [('B', 18), ('C', 12), ('D', 35), ('E', 30)],
    'B': [('A', 18), ('D', 16), ('E', 18)],
    'C': [('A', 12), ('D', 23), ('F', 11)],
    'D': [('A', 35), ('B', 16), ('C', 23), ('E', 21), ('F', 10), ('G', 12), ('H', 40)],
    'E': [('B', 18), ('D', 21), ('G', 17)],
    'F': [('C', 11), ('D', 10), ('G', 25), ('H', 55)],
    'G': [('D', 12), ('E', 17), ('F', 25), ('H', 20)],
    'H': [('D', 40), ('F', 55), ('G', 20)]
}

activities = {
    "Morning": [
        ("Lesson 1", 'B'),
        ("Lesson 2", 'D')
    ],
    "Noon": [
        ("Lunch", 'H')
    ],
    "Afternoon": [
        ("Lesson 1", 'C'),
        ("Lesson 2", 'A'),
        ("Lesson 3", 'E')
    ]
}

def main():
    current_location = 'A'

    print('In geval van nood, voer "NOOD" in!')
    print('Kies nu uw activiteiten:')

    for time, options in activities.items():
        print(f"{time} Activiteiten:")
        for i, (activity, location) in enumerate(options, 1):
            print(f"  {i}. {activity} op locatie {location}")

        choice = 0
        if len(options) > 1:
            get_choice(f"Kies activiteit voor {time}", options, current_location)

        chosen_activity, destination = options[choice]

        print(f"\nKeuze: {chosen_activity} op locatie {destination}")

        route = shortest_route(demograph, current_location, destination)
        print(f"Route naar {destination}: {route}")

def get_choice(prompt, options, current_location):
    choice = -1
    while choice == -1:
        try:
            inp = input(f"{prompt} (1-{len(options)}): ")
            if inp == "NOOD":
                route = shortest_route(demograph, current_location, 'F')
                print(f"Route naar Nooduitgang: {route}")
                exit()
            choice = int(inp) - 1
            if choice < 0 or choice >= len(options):
                choice = -1
                print("Kies een activiteit uit de lijst!")
        except ValueError:
            print("Voer een getal in!")
    return choice

if __name__ == '__main__':
    main()