import json
import random
from faker import Faker
from app import create_app, db
from app.models.student_request import StudentRequest
from app.models.room import Room


def load_buildings_from_json():
    with open("./data/building_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def load_names_from_json():
    with open("./data/name_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["first_names"], data["male_last_names"], data["female_last_names"]


faker = Faker()
buildings_info = load_buildings_from_json()
first_names, male_last_names, female_last_names = load_names_from_json()

genders = ["Nam", "Nữ"]
bedtime_habits = ["21h", "21h30", "22h", "22h30", "23h", "23h30", "0h", "0h30", "1h", "1h30", "2h", "2h30", "3h"]
social_stypes = ["Hướng nội", "Hướng ngoại", "Bình thường"]
religions = ["Không", "Kitô giáo", "Công giáo", "Tin lành", "Phật giáo", "Hòa Hảo", "Cao Đài", "Hồi giáo", "Khác"]
academic_years = [66, 67, 68, 69]
majors = ["CNTT & TT", "Cơ khí", "Điện - Điện tử", "Kinh tế", "Hóa & KH sự sống", "Vật liệu", "Toán-Tin", "Vật lý Kỹ thuật", "Ngoại ngữ"]
is_smokers = ["Có", "Không"]


def generate_rooms_data(seed=42):
    data = []
    total_capacity = 0
    random.seed(seed)
    for building in buildings_info:
        for floor in range(1, building["total_floors"]+1):
            for room_number in range(1, building["rooms_per_floor"]+1):
                room_name = f"{building['building_name']}-{floor}{room_number:02d}"
                room = Room(
                    building_name=building["building_name"],
                    room_name=room_name,
                    capacity=random.choice([6, 8, 10, 12]),
                )
                data.append(room)
                total_capacity += room.capacity
    
    return data, total_capacity


def generate_student_requests_data(num_of_records, seed=42):
    data = []
    faker.seed_instance(seed)
    random.seed(seed)
    
    for _ in range(num_of_records):
        academic_year = random.choices(academic_years, [0.1, 0.2, 0.3, 0.4])[0]
        if academic_year == 66:
            entry_year = 2021
        elif academic_year == 67:
            entry_year = 2022
        elif academic_year == 68:
            entry_year = 2023
        else:
            entry_year = 2024
            
        random_number = faker.unique.random_number(digits=4)
        student_id = f"{entry_year}{random_number:04d}"

        gender = random.choices(genders, [0.6, 0.4])[0]
        first_name = random.choice(first_names)
        if gender == "Nam":
            last_name = random.choice(male_last_names)
        else:
            last_name = random.choice(female_last_names)
            
        full_name = f"{first_name} {last_name}"
        
        student_request = StudentRequest(
            student_id=student_id,  
            name=full_name,
            gender=gender,
            bedtime_habit=random.choices(bedtime_habits, [0.01, 0.01, 0.05, 0.05, 0.1, 0.15, 0.2, 0.15, 0.1, 0.05, 0.05, 0.04, 0.04])[0],
            social_style=random.choices(social_stypes, [0.2, 0.5, 0.3])[0],
            religion=random.choices(religions, [0.9, 0.01, 0.03, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])[0],
            academic_year=academic_year,
            major=random.choices(majors, [0.2, 0.14, 0.19, 0.15, 0.14, 0.13, 0.05, 0.05, 0.05])[0],
            sports_passion_score=random.randint(1, 10),
            music_passion_score=random.randint(1, 10),
            gaming_passion_score=random.randint(1, 10),
            average_monthly_spending=random.randint(2000, 5000)*1000,
            is_smoker=random.choices(is_smokers, [0.25, 0.75])[0]
        )
        data.append(student_request)
        
    return data


def insert_data_into_database(num_of_students=2000):
    app = create_app()
    with app.app_context():
        if Room.query.first() is None:
            rooms_data, total_capacity = generate_rooms_data()
            db.session.bulk_save_objects(rooms_data)
            db.session.commit()
            print(f"{len(rooms_data)} records of rooms data inserted into the database with a total capacity of {total_capacity} beds.")
        else:
            print("261 records of rooms data already exist in the database with a total capacity of 2280 beds.")
            
        if StudentRequest.query.first() is None:
            student_requests_data = generate_student_requests_data(num_of_students)
            db.session.bulk_save_objects(student_requests_data)
            db.session.commit()
            print(f"{num_of_students} records of student requests data inserted into the database.")
        else:
            print(f"{num_of_students} records of student requests data already exist in the database.")
