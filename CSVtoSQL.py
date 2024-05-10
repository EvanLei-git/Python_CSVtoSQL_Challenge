#https://stackoverflow.com/a/29361173

import csv
import random
import requests
from geopy.geocoders import Photon
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut
from requests.exceptions import ReadTimeout
import string
import time
import re
import os

def create_insert_country(row, country_set):
	# Check if the NOC already exists
	if row['NOC'] in {item[0] for item in country_set}:
		return None  # Skip this INSERT statement
	else:
		# Add the NOC and country name tuple to the set
		country_set.add((row['NOC'], row['Team']))
		clean_team_name = row['Team'].replace("'", "")  # Remove apostrophes from the noc

		return f"INSERT INTO Country (NOC, Name) VALUES ('{row['NOC']}', '{clean_team_name}');"



def remove_gender_from_category(event_category):
	if "(Men)'s" in event_category:
		return event_category.replace("(Men)'s", "").strip()
	elif "(Women)'s" in event_category:
		return event_category.replace("(Women)'s", "").strip()
	else:
		return event_category.strip()

def determine_event_type(event_name ):
	if 'Mixed' in event_name:
		return "Mixed", event_name.split('Mixed')[1].strip()
	elif "Men" in event_name:
		return "Men", event_name.split("Men's")[1].strip()
	elif "Women" in event_name:
		return "Women", event_name.split("Women's")[1].strip()
	else:
		return 'Error'

def create_insert_event(row):
	event_sex, event_category = determine_event_type(row['Event'])
	event_category = remove_gender_from_category(event_category)
	event_name = remove_gender_from_category(row['Event'])
	return f"INSERT INTO Event (Ename, Sport, Gender, Category) VALUES ('{event_name}', '{row['Sport']}', '{event_sex}', '{event_category}');"


def calculate_birth_date(year, age):
	if age == "NA":
		age = random.randint(18, 60)
	birth_year = int(year) - int(age)
	birth_month = random.randint(1, 12)
	birth_day = random.randint(1, 28)  # Limit day to avoid invalid dates
	return f"{birth_day:02d}-{birth_month:02d}-{birth_year}"

def create_insert_athlete(row):
	name = row['ID']
	# Check if the name has already been encountered
	if name in unique_names:
		return None  # Skip this INSERT statement
	else:
		unique_names.add(name)  # Add the name to the set of unique names
		birth_date = calculate_birth_date(row['Year'], row['Age'])
		clean_name = row['Name'].replace("'", "")  # Remove apostrophes from the name
		return f"INSERT INTO Athlete (AthleteID, Name, DateOfBirth, Sex, HasTeam) VALUES ({row['ID']}, '{clean_name}', '{birth_date}', '{row['Sex']}', '{row['NOC']}');"


def create_insert_participation(row):
	event_name = remove_gender_from_category(row['Event'])
	return f"INSERT INTO Participation (AthleteID, Year, Period, Event, Medal) VALUES ({row['ID']}, {row['Year']}, '{row['Season']}', '{event_name}', '{row['Medal']}');"



def create_insert_games(row, country_set, city_set, games_set):
	city = row['City']
	period = row['Season']
	year = row['Year']
	hosted_in_country = None
	
	# Check if the city, year, and period combination has already been processed
	if (city, year, period) in games_set:
		return None  # Skip this INSERT statement
	else:
		# Add the city, year, and period combination to the set
		games_set.add((city, year, period))

	# Find the country for the city
	for noc, country_name in country_set:
		if country_name == city:
			hosted_in_country = noc
			break

	clean_city_name = city.replace("'", "")  # Remove apostrophes from the noc
	if hosted_in_country:

		return f"INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES ({year}, '{period}', '{clean_city_name}', '{hosted_in_country}');"
	else:
		if city== 'London':
			return f"INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES ({year}, '{period}', '{clean_city_name}', 'GBR');"
		if city== 'Athina':
			return f"INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES ({year}, '{period}', '{clean_city_name}', 'GRE');"
		time.sleep(1)
		# Initialize a Photon geolocator
		geolocator = Photon(
			user_agent="Mozilla/5.0 (Linux; arm; Android 8.1.0; SM-J730FM) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.5.140.00 Mobile SA/1 Safari/537.36",
			timeout=3  # Set the timeout value, e.g., 3 seconds
			)
		# Geocode the city name to get its coordinates
		location = geolocator.geocode(city)

		if location:
			# Reverse geocode the coordinates to get country name in English
			country_location = geolocator.reverse((location.latitude, location.longitude), language='en')

			# Extract country name from the reverse geocoded location
			country_name = country_location.raw['properties']['country']

			# Find the NOC for the country name
			for noc, name in country_set:
				if name == country_name:
					hosted_in_country = noc
					break

		if hosted_in_country:
			return f"INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES ({year}, '{period}', '{clean_city_name}', '{hosted_in_country}');"
		else:
			return f"INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES ({year}, '{period}', '{clean_city_name}', 'UNKNOWN');"


def remove_duplicates_from_file(input_file):
	with open(input_file, 'r', encoding='utf-8') as file:
		lines = file.readlines()

	# Remove duplicates while preserving the order
	unique_lines = []
	seen_lines = set()
	for line in lines:
		if line not in seen_lines:
			unique_lines.append(line)
			seen_lines.add(line)

	# Write unique lines back to the file
	with open(input_file, 'w', encoding='utf-8') as file:
		file.writelines(unique_lines)


def remove_gender_apostrophy(input_file):
	with open(input_file, 'r', encoding='utf-8') as file:
		lines = file.readlines()

	# Remove duplicates while preserving the order
	unique_lines = []
	seen_lines = set()
	for line in lines:
		# Remove possessive 's from lines containing "Men's" or "Women's"
		if "Men's" in line:
			line = line.replace("Men's", "Men")
		elif "Women's" in line:
			line = line.replace("Women's", "Women")

		# Check if the modified line is unique
		if line not in seen_lines:
			unique_lines.append(line)
			seen_lines.add(line)

	# Write unique lines back to the file
	with open(input_file, 'w', encoding='utf-8') as file:
		file.writelines(unique_lines)


def organize_lines(input_file, output_file):
	categories_order = ['Country', 'Event', 'Athlete', 'Games', 'Participation']
	categories = {category: [] for category in categories_order}

	with open(input_file, 'r') as file:
		for line in file:
			for category in categories_order:
				if line.startswith('INSERT INTO ' + category):
					categories[category].append(line.strip())
					break

	with open(output_file, 'w') as out_file:
		for category in categories_order:
			if categories[category]:
				# Skip the first line if it matches the category header exactly
				for line in categories[category]:
					if line != 'INSERT INTO ' + category:
						out_file.write(line + '\n')
				out_file.write('\n')

csv_file = 'athlete_events.csv'
output_file = 'output.sql'  # Name of the output file
unique_names = set()  # Set to store unique athlete names
country_set = set() #saved both NOC and the country
city_set=set()
games_set= set()

time.sleep(1)

with open(csv_file, newline='', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	csvfile.seek(0)  # Reset the file pointer to the beginning
	next(reader)  # Skip the first line (header)

	for row in reader:
		country_insert = create_insert_country(row, country_set)
		if country_insert:
			with open(output_file, 'a', encoding='utf-8') as output:
				output.write(country_insert + '\n')

	csvfile.seek(0)  # Reset the file pointer to the beginning
	next(reader)  # Skip the first line (header)
	
	for row in reader:
		with open(output_file, 'a', encoding='utf-8') as output:
			output.write(create_insert_event(row) + '\n')
			athlete_insert = create_insert_athlete(row)
			if athlete_insert is not None:
				output.write(athlete_insert + '\n')

	csvfile.seek(0)  # Reset the file pointer to the beginning
	next(reader)  # Skip the first line (header)

	for row in reader:
		game_insert = create_insert_games(row, country_set, city_set, games_set)
		
		if game_insert is not None:
			time.sleep(1) #slowing down the API calls, don't want to get 403ed
			with open(output_file, 'a', encoding='utf-8') as output:
				output.write(game_insert + '\n')

	csvfile.seek(0)  # Reset the file pointer to the beginning
	next(reader)  # Skip the first line (header)

	for row in reader:
		with open(output_file, 'a', encoding='utf-8') as output:
			output.write(create_insert_participation(row) + '\n')
			output.write('\n')  # Add a newline between each SQL statement



remove_duplicates_from_file(output_file)

remove_gender_apostrophy(output_file)
remove_duplicates_from_file(output_file)

done_file = 'done.sql'
organize_lines(output_file, done_file)

begin_lines = [
	f"set feedback off",
	f"set define off",
	f"ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';"
]
with open(done_file, 'r') as file:
	file_data = file.read()

with open(done_file, 'w') as file:
	for line in begin_lines:
		file.write(line + '\n')
	file.write(file_data)

os.remove(output_file)

'''
def check_event_format(input_file):
	lines_without_expected_format = []  # List to store lines without the expected format
	with open(input_file, 'r', encoding='utf-8') as file:
		for line in file:
			if line.startswith("INSERT INTO Participation"):
				try:
					# Extract the event name from the line
					parts = line.split("VALUES")[1].strip().strip("();").split(",")
					event_name = parts[3].strip().strip("'")
					# Check if the event name contains "Men's" or "Women's"
					if "Men's" not in event_name and "Women's" not in event_name and "Mixed" not in event_name:
						lines_without_expected_format.append(line)
				except (IndexError, ValueError):
					print(f"Error processing line: {line}")
	return lines_without_expected_format

# Test the function with the output.sql file
lines_without_expected_format = check_event_format('output.sql')

# Print the lines that don't have the expected format
for line in lines_without_expected_format:
	print(line.strip())




'''

