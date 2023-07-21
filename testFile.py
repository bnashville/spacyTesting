import spacy
import re

#use "pip install -r requirements.txt" to install spacy and dependencies

def format_transcriptions(transcriptions):
    formatted_data = []
    pattern = r'^([\d.]+)\s([\d.]+)\s+(\w+):\s(.+)$'

    for line in transcriptions:
        match = re.match(pattern, line)
        if match:
            start_time = float(match.group(1))
            end_time = float(match.group(2))
            speaker = match.group(3)
            text = match.group(4)
            
 # Clean up the text
            text = re.sub(r'[\[\]@=]+', '', text)
            text = re.sub(r'\d+\([A-Za-z]+\)\d+', '', text)
            text = re.sub(r'\d+\(Hx\)=\d+', '', text)

            # Remove leading/trailing whitespaces
            text = text.strip()

            
            turn = {
                'start_time': start_time,
                'end_time': end_time,
                'speaker': speaker,
                'text': text
            }

            formatted_data.append(turn)

    return formatted_data


# Load SpaCy model
nlp = spacy.load('en_core_web_lg')

# Read conversation transcriptions from a file
with open('G:/2023/SPAcY/SBC_SBC052.txt', 'r') as file:
    transcriptions = file.readlines()

# Format transcriptions
formatted_data = format_transcriptions(transcriptions)

# Initialize lists for different entity types
names_list = []
dates_list = []
places_list = []
numbers_list = []
orgs_list = []

# Extract entities from the transcriptions
for turn in formatted_data:
    text = turn['text']
    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            names_list.append(entity.text)
        elif entity.label_ == 'DATE':
            dates_list.append(entity.text)
        elif entity.label_ == 'GPE' or entity.label_ == 'LOC':
            places_list.append(entity.text)
        elif entity.label_ == 'CARDINAL':
            numbers_list.append(entity.text)
        elif entity.label_ == 'ORG':
            orgs_list.append(entity.text)

# Remove duplicates and empty values
names_list = list(set(names_list))
names_list = [name for name in names_list if name.strip()]

dates_list = list(set(dates_list))
dates_list = [date for date in dates_list if date.strip()]

places_list = list(set(places_list))
places_list = [place for place in places_list if place.strip()]

numbers_list = list(set(numbers_list))
numbers_list = [number for number in numbers_list if number.strip()]

orgs_list = list(set(orgs_list))
orgs_list = [org for org in orgs_list if org.strip()]

# Print the lists
print('List of names:')
print(names_list)
print('---')
print('List of dates:')
print(dates_list)
print('---')
print('List of places:')
print(places_list)
print('---')
print('List of numbers:')
print(numbers_list)
print('---')
print('List of Orgs:')
print(numbers_list)