import time
import datetime #import datetime, timedelta

def calculate_corrected_gestational_age(birth_date, gestational_age_weeks, gestational_age_days, days_after_birth):
    # Convert the gestational age at birth into days
    gestational_age_days_total = (gestational_age_weeks * 7) + gestational_age_days
    
    # Calculate the corrected gestational age
    corrected_gestational_age_days = gestational_age_days_total + days_after_birth
    corrected_gestational_age_weeks = corrected_gestational_age_days // 7
    corrected_gestational_age_days = corrected_gestational_age_days % 7
    
    # Calculate the date X days after birth
    birth_datetime = datetime.strptime(birth_date, '%Y-%m-%d')
    days_after_birth_timedelta = timedelta(days=days_after_birth)
    x_days_after_birth_datetime = birth_datetime + days_after_birth_timedelta
    
    # Print the results
    print(f"On {x_days_after_birth_datetime.strftime('%Y-%m-%d')}, the corrected gestational age is {corrected_gestational_age_weeks} weeks and {corrected_gestational_age_days} days.")

# Example usage
# example = calculate_corrected_gestational_age('2023-03-31', 32, 5, 14)  # birth_date = '2023-03-31', gestational_age_weeks = 32, gestational_age_days = 5, days_after_birth = 4

def magic_convert_date(date_input):
    try:
        date_input = int(date_input)
        return time.strftime('%Y-%m-%d', time.localtime(date_input))
    except ValueError:
        return int(time.mktime(time.strptime(date_input, '%Y-%m-%d')))

def gestational_seperator(gestational_age_str):
    # Split the gestational age string into weeks and days
    weeks_str, days_str = gestational_age_str.split()
    # Convert the weeks and days to integers
    weeks = int(weeks_str)
    days = min(int(days_str), 6)  # Limit the number of days to 6
    # Return the separated values
    return weeks, days

# gestational_age_str = '32 week 5 day'
# birth_date_str = '2023-03-30'
# birth_weight = 1234
# gestational_age_weeks,gestational_age_day = gestational_seperator()

def create_reminder(birth_date, days_offset):
    return (birth_date + datetime.timedelta(days=days_offset)).strftime('%Y-%m-%d')

def premature_reminders(birth_date_str, gestational_age_weeks):
    birth_date = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d')
    reminder_keys = [
        'D vitamin begins', 'K vitamin prophylaxis', 'Eye PenG', 'Hepatitis B vaccine',
        'BCG vaccine', 'Karma vaccine', 'KPA vaccine', 'Thyroid function check',
        'Check weight gain', 'ROP exam', 'Iron prophylaxis', 'TFUS', 'EKO',
        'Osteopenia evaluation', 'Anemia evaluation', 'Blood tests (Ca, P, ALP, CBC)',
        'TFUS 1', 'TFUS 2'
    ]
    reminders = {key: None for key in reminder_keys}

    reminders.update({
        'D vitamin begins': create_reminder(birth_date, 7),
        'K vitamin prophylaxis': create_reminder(birth_date, 0),
        'Eye PenG': create_reminder(birth_date, 0),
        'Hepatitis B vaccine': create_reminder(birth_date, 30),
        'BCG vaccine': create_reminder(birth_date, 60),
        'Karma vaccine': create_reminder(birth_date, 60),
        'KPA vaccine': create_reminder(birth_date, 60)
    })

    if gestational_age_weeks < 34:
        reminders.update({
            'Thyroid function check': create_reminder(birth_date, 7),
            'Check weight gain': create_reminder(birth_date, 14),
            'ROP exam': create_reminder(birth_date, 28),
            'Iron prophylaxis': create_reminder(birth_date, 30)
        })

        if gestational_age_weeks < 32:
            reminders.update({
                'TFUS': create_reminder(birth_date, 3),
                'EKO': create_reminder(birth_date, 3),
                'Osteopenia evaluation': create_reminder(birth_date, 21),
                'Anemia evaluation': create_reminder(birth_date, 21),
                'Blood tests (Ca, P, ALP, CBC)': create_reminder(birth_date, 28)
            })

        if gestational_age_weeks < 28:
            reminders.update({
                'TFUS 1': create_reminder(birth_date, 0),
                'TFUS 2': create_reminder(birth_date, 7)
            })
    # Set all None values to 'NaN'
    for key, value in reminders.items():
        if value is None:
            reminders[key] = 'NaN'

    return reminders



# Demo for magic converter
# for i in reminder_list.keys():
#     unix = reminder_list[i]
#     datetime = magic_convert_date(unix)
#     print(5*'*')
#     print('With UNIX')
#     print(f"For {i} at {unix}")
#     print(5*'*')
#     print('With Date-time')
#     print(f"For {i} at {datetime}")
#     print(5*'*')

