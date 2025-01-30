from Dijkstra import *
import json
import random

def load_graph(file_path):
    with open(file_path, 'r') as file:
        graph = json.load(file)
    return graph

graph = load_graph("graph.json")

activities = {
    "Morning": [
        ("Lezing 1", 'B3.209'),
        ("Hackaton 1", 'B1.209')
    ],
    "Noon": [
        ("Lunch", 'Restaurant')
    ],
    "Early Afternoon": [
        ("Lezing 2", 'B1.210'),
        ("Lezing 3", 'B2.210'),
        ("Workshop 1", 'B3.210')
    ],
    "Late Afternoon": [
        ("Workshop 2", 'B1.305'),
        ("Hackaton 2", 'B2.305'),
        ("Workshop 3", 'B3.305')
    ]

}

def main():
    transport_options = ["Auto", "Bus", "Fiets"]
    location_mapping = ["Ingang Parkeren", "Hoofdingang", "Hoofdingang"]
    for i, (option) in enumerate(transport_options, 1):
        print(f"  {i}. {option}")
    transport_choice = get_choice("Hoe bent u hier gekomen?", transport_options, 'Hoofdingang')
    current_location = location_mapping[transport_choice]

    mobility = not bool(get_choice("Heeft u mobiliteitsproblemen?\n  1. Ja \n  2. Nee\n", ["Ja", "Nee"], current_location))

    print('\nIn geval van nood, voer "NOOD" in!')

    for time, options in activities.items():
        print(f"{time} Activiteiten:")
        for i, (activity, location) in enumerate(options, 1):
            print(f"  {i}. {activity} op locatie {location}")

        choice = 0
        if len(options) > 1:
            choice = get_choice(f"Kies activiteit voor {time}", options, current_location, mobility)

        chosen_activity, destination = options[choice]

        print(f"\nKeuze: {chosen_activity} op locatie {destination}")

        route, _ = shortest_route(graph, current_location, destination, mobility)
        current_location = destination
        print(f"Route naar {destination}: {route}")

def get_choice(prompt, options, current_location, mobility=False):
    choice = -1
    while choice == -1:
        try:
            inp = input(f"{prompt} (1-{len(options)}): ")
            if inp == "NOOD":
                route = emergency_exit(current_location, mobility)
                print(f"Route naar Nooduitgang: {route}")
                exit()
            choice = int(inp) - 1
            if choice < 0 or choice >= len(options):
                choice = -1
                print("Kies een activiteit uit de lijst!")
        except ValueError:
            print("Voer een getal in!")
    return choice

def emergency_exit(current_location, mobility=False):
    emergency_nodes = [node for node in graph if node.startswith("Nood")]
    if not emergency_nodes:
        return None

    shortest_path = None
    shortest_distance = float('inf')

    for emergency_node in emergency_nodes:
        route, distance = shortest_route(graph, current_location, emergency_node, mobility, emergency=True)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = route

    return shortest_path

if __name__ == '__main__':
    main()