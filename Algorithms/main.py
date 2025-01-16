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

    for time, options in activities.items():
        print(f"{time} Activiteiten:")
        for i, (activity, location) in enumerate(options, 1):
            print(f"  {i}. {activity} op locatie {location}")

        if len(options) == 1:
            choice = 0
        else:
            choice = -1
            while choice == -1:
                try:
                    choice = int(input(f"Kies activiteit voor {time} (1-{len(options)}): ")) - 1
                    if choice < 0 or choice >= len(options):
                        choice = -1
                        print("Kies een activiteit uit de lijst!")
                except ValueError:
                    print("Voer een getal in!")

        chosen_activity, destination = options[choice]

        print(f"\nKeuze: {chosen_activity} op locatie {destination}")

        route = shortest_route(demograph, current_location, destination)
        print(f"Route naar {destination}: {route}")

if __name__ == '__main__':
    main()