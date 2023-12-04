import pandas as pd
import re

def extract_days(days_string, day_abbreviations):
    """Extract and normalize days from a string."""
    pattern = '|'.join([re.escape(day[:3]) for day in day_abbreviations])
    found_days = re.findall(pattern, days_string, flags=re.IGNORECASE)
    # Normalize day abbreviations (capitalize first letter)
    normalized_days = [day.capitalize() for day in found_days]
    # Remove duplicates while preserving order
    unique_days = sorted(set(normalized_days), key=normalized_days.index)
    return ', '.join(unique_days)

def parse_time(time_string):
    """Parse time string to datetime.time object, return None if parsing fails."""
    try:
        return pd.to_datetime(time_string, errors='coerce', format='%H:%M').time()
    except ValueError:
        return None

def parse_schedule_optimized(data, day_abbreviations):
    """Parse and reformat broker schedule data with improved error handling."""
    try:
        # Check data format
        if data.shape[1] != 1:
            raise ValueError("Data should have a single column.")

        # Splitting the data into separate columns
        columns = ['BrokerName', 'DaysWorked', 'Begin', 'LunchBegin', 'LunchEnd', 'End']
        data_split = data.iloc[:, 0].str.split(' / ', expand=True)
        if len(data_split.columns) != len(columns):
            raise ValueError("Data splitting did not result in the expected number of columns.")

        data_split.columns = columns

        # Parsing time columns
        for col in ['Begin', 'LunchBegin', 'LunchEnd', 'End']:
            data_split[col] = data_split[col].apply(parse_time)

        # Extracting and normalizing days
        data_split['DaysWorked'] = data_split['DaysWorked'].apply(
            lambda x: extract_days(x, day_abbreviations))

        return data_split
    except Exception as e:
        print(f"Error parsing schedule: {e}")
        return None

# Standard day abbreviations
day_abbreviations = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# File path (adjust as per your environment)
file_path = '/content/BrokerData.csv'

# Loading the data without assuming a header row
broker_data = pd.read_csv(file_path, header=None)

# Parsing the data
parsed_data_optimized = parse_schedule_optimized(broker_data, day_abbreviations)

# Displaying the first row for debugging
if parsed_data_optimized is not None:
    parsed_data_optimized.head()
else:
    print("Parsing failed.")

parsed_data_optimized.head() if parsed_data_optimized is not None else "Parsing failed."
