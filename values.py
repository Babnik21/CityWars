unit_costs = {
    "Infantryman": [35, 15, 0],
    "Sniper": [30, 25, 0],
    "Tank": [150, 200, 5],
    "Spy": [100, 10, 3],
    "General": [1000, 100, 100]
}

unit_stats = {
    "Infantryman": [50, 25, 4, 100],
    "Sniper": [10, 70, 3, 75],
    "Tank": [150, 190, 1, 200],
    "Spy": [1, 10, 7, 0],
    "General": [0, 0, 1, 0]
}

unit_training_place = {
    "Infantryman": "Training Camp",
    "Sniper": "Range",
    "Tank": "Factory",
    "Spy": "Agency",
    "General": "Military HQ"
}

units_trained_in = {
    "Training Camp": "Infantryman",
    "Range": "Sniper",
    "Factory": "Tank",
    "Agency": "Spy",
    "Military HQ": "General"
}


building_costs = {
    "Farm": [[20, 10, 0], [50, 20, 0], [300, 120, 2], [800, 600, 5], [1500, 1500, 12], [0, 0, 0]],
    "Iron Mine": [[70, 30, 0], [140, 30, 2], [300, 200, 5], [550, 850, 10], [800, 1500, 20], [0, 0, 0]],
    "Gold Mine": [[320, 210, 0], [500, 260, 3], [750, 550, 7], [1250, 1100, 15], [2000, 2800, 35], [0, 0, 0]],
    "Warehouse": [[100, 100, 0], [300, 200, 0], [500, 400, 0], [750, 750, 0], [1200, 1500, 0], [0, 0, 0]],
    "Wall": [[200, 50, 0], [400, 250, 0], [800, 800, 0], [1100, 1350, 5], [2000, 2900, 20], [0, 0, 0]],
    "Training Camp": [[100, 80, 1], [500, 400, 10], [700, 700, 15], [1000, 1200, 25], [1500, 2500, 50], [0, 0, 0]],    
    "Housing": [[500, 200, 0], [750, 350, 0], [1000, 700, 5], [1600, 1300, 20], [2300, 2500, 50], [0, 0, 0]],
    "Bunker": [[350, 200, 0], [500, 500, 5], [650, 1000, 15], [850, 1700, 25], [1400, 2600, 40], [0, 0, 0]],  
    "Range": [[500, 200, 5], [700, 400, 7], [1000, 850, 10], [1400, 1450, 15], [2300, 2500, 23], [0, 0, 0]],    
    "Bank": [[700, 750, 8], [1200, 1400, 15], [1800, 2250, 30], [2800, 3200, 50], [4200, 5000, 85], [0, 0, 0]],
    "Vault": [[1500, 1200, 30], [2500, 3000, 55], [3800, 4500, 100], [3900, 5500, 150], [4000, 8000, 250], [0, 0, 0]],
    "Bakery": [[3000, 200, 10], [4000, 350, 15], [5000, 600, 25], [6000, 1000, 35], [7000, 1850, 50], [0, 0, 0]],
    "Agency": [[2000, 300, 50], [2000, 500, 50], [2000, 850, 70], [3500, 1400, 100], [6000, 3000, 230], [0, 0, 0]],
    "Factory": [[1500, 1000, 30], [2000, 2000, 50], [2700, 3000, 90], [3800, 4200, 180], [5200, 6100, 350], [0, 0, 0]],
    "Military HQ": [[1000, 1500, 25], [3000, 2600, 100], [5000, 3400, 270], [5000, 4100, 600], [6500, 6500, 900], [0, 0, 0]],
}

points = {
    "Farm": [0, 1, 3, 6, 10, 16],
    "Iron Mine": [0, 1, 3, 7, 12, 20],
    "Gold Mine": [0, 2, 7, 16, 31, 59],
    "Warehouse": [0, 1, 3, 6, 11, 18],
    "Wall": [0, 0, 0, 0, 0, 0],
    "Training Camp": [0, 3, 7, 13, 22, 40],    
    "Housing": [0, 7, 19, 44, 81, 155],
    "Bunker": [0, 2, 3, 5, 7, 10],  
    "Range": [0, 4, 8, 15, 27, 45],    
    "Bank": [0, 25, 45, 88, 149, 233],
    "Vault": [0, 10, 12, 16, 23, 35],
    "Bakery": [0, 22, 41, 70, 121, 187],
    "Agency": [0, 28, 48, 84, 141, 209],
    "Factory": [0, 51, 80, 142, 211, 320],
    "Military HQ": [0, 400, 560, 750, 1000, 1500],
}

farm_prod = [10, 45, 130, 310, 750, 1600]
iron_prod = [10, 40, 100, 300, 740, 1500]
gold_prod = [0, 3, 7, 12, 20, 50]
bakery_prod = [0, 1000, 2500, 4000, 7500, 12000]

bank_capacity = [10, 50, 140, 330, 580, 980]
warehouse_capacity = [300, 1000, 3100, 7600, 18500, 40000]
bunker_capacity = [0, 200, 500, 1000, 2000, 5000]
housing_capacity = [75, 150, 425, 1100, 3600, 12500]
vault_capacity = [0, 20, 50, 100, 200, 500]

wall_power = [0, 100, 350, 1000, 3000, 7000]

training_spd = {
    "Training Camp": [0, 3, 3, 2, 2, 1],
    "Range": [0, 3, 3, 2, 2, 1],
    "Factory": [0, 10, 6, 4, 2, 1],
    "Agency": [0, 10, 6, 4, 2, 1],
    "Military HQ": [0, 10, 6, 4, 2, 1]
}

cities = [
    "Tokyo",
    "New York",
    "Los Angeles",
    "Chicago",
    "Dallas",
    "Phoenix",
    "San Diego",
    "Miami",
    "Barcelona",
    "Madrid",
    "Paris",
    "Marseille",
    "London",
    "Liverpool",
    "Munich",
    "Dortmund",
    "Istanbul",
    "Moscow",
    "Berlin",
    "Kyiv",
    "Rome",
    "Bucharest",
    "Minsk",
    "Vienna",
    "Warsaw",
    "Budapest",
    "Belgrade",
    "Milan",
    "Sofia",
    "Prague",
    "Kazan",
    "Cologne",
    "Stockholm",
    "Naples",
    "Amsterdam",
    "Turin",
    "Valencia",
    "Krakow",
    "Athens",
    "Helsinki",
    "Seville",
    "Copenhagen",
    "Riga",
    "Frankfurt",
    "Vilnius",
    "Riga",
    "Dublin",
    "Brussels",
    "Lisbon",
    "Porto",
    "Bratislava",
    "Houston",
    "Sao Paulo",
    "Lima",
    "Bogotá",
    "Caracas",
    "Buenos Aires",
    "Brasilia",
    "Mexico City",
    "Toronto",
    "Monterrey",
    "Montreal",
    "Vancouver",
    "Sydney",
    "Melbourne",
    "Brisbane",
    "Perth",
    "Delhi",
    "Manila",
    "Seoul",
    "Shanghai",
    "Beijing",
    "Bangkok",
    "Osaka",
    "Taipei",
    "Ankara",
    "Baghdad",
    "Lagos",
    "Cairo",
    "Nairobi",
]

colors = [(250, 50, 50),
    (100, 100, 100),
    (50, 50, 250),
    (250, 50, 250),
    (50, 250, 250),
    (200, 200, 50),
    (250, 200, 100),
    (50, 150, 250),
    (75, 150, 150)]