import csv
import random
from faker import Faker

fake = Faker()

# City lists
kerala_cities = ["Kochi", "Thiruvananthapuram", "Thrissur", "Kozhikode", "Kollam", "Alappuzha", "Kannur", "Kottayam", "Malappuram", "Ernakulam", "Palakkad", "Pathanamthitta"]
indian_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune", "Jaipur", "Ahmedabad", "Lucknow", "Surat"]
intl_cities = ["Tokyo", "London", "New York", "Dubai", "Singapore", "Paris", "Sydney"]
all_cities = kerala_cities * 40 + indian_cities * 40 + intl_cities * 20

# Property details
property_types = ["Villa", "Apartment", "House", "Office", "Land"]
props = ["Sale", "Rent"]
statuses = ["Available", "Sold", "Pending"]

# Descriptions by city type
desc_kerala = ["A serene villa with a backwater view.", "A cozy apartment near the beach.", "A traditional Kerala house with a courtyard."]
desc_india = ["A luxury apartment in the city center.", "A modern house in a gated community.", "A prime office in the business district."]
desc_intl = ["A luxury villa with a skyline view.", "A sleek office in the downtown area.", "A minimalist apartment with modern amenities."]

with open("properties_1000.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "user_id", "phone", "place", "image", "propertytype", "prop", "price", "description", "status", "date", "location", "document", "bedrooms", "bathrooms", "area_sqft", "is_furnished", "parking_space", "total_rooms", "price_per_sqft"])
    
    for i in range(1, 1001):
        city = random.choice(all_cities)
        prop_type = random.choice(property_types)
        prop = random.choice(props)
        status = random.choices(statuses, weights=[50, 25, 25])[0]
        
        # Price logic
        if city in kerala_cities:
            price = random.randint(10000, 40000) if prop == "Rent" else random.randint(400000, 1200000)
            desc = random.choice(desc_kerala)
        elif city in indian_cities:
            price = random.randint(20000, 80000) if prop == "Rent" else random.randint(800000, 2500000)
            desc = random.choice(desc_india)
        else:
            price = random.randint(50000, 150000) if prop == "Rent" else random.randint(1500000, 5000000)
            desc = random.choice(desc_intl)
        
        # Area and rooms
        area = random.uniform(500, 10000) if prop_type == "Land" else random.uniform(500, 5000)
        bedrooms = 0 if prop_type in ["Office", "Land"] else random.randint(1, 5)
        bathrooms = 0 if prop_type == "Land" else random.randint(1, 4)
        total_rooms = bedrooms + random.randint(1, 4) if prop_type not in ["Office", "Land"] else random.randint(1, 5) if prop_type == "Office" else 0
        
        writer.writerow([
            i, f"Property {i}", random.randint(1, 100), fake.phone_number()[:10],
            city, f"images/property_{i}.jpg", prop_type, prop, price, desc, status,
            "2025-03-19", "", f"documents/properties/doc_{i}.jpg", bedrooms, bathrooms,
            round(area, 2), random.choice([True, False]), random.choice([True, False]),
            total_rooms, round(price / area, 2)
        ])

print("Generated 1000 entries in 'properties_1000.csv'")