import os.path
from datetime import datetime, timedelta
from GooleCalendar import GoogleCalendar

dir_path = os.path.dirname(os.path.abspath(__file__))


def main():
    calendar = GoogleCalendar(
        # api_keys_path=os.path.join(dir_path, '..', 'secrets', 'GCP-api-key.json'),
        calendar_id='idigital.bs@gmail.com'
    )

    # print(calendar.get_events_list())

    tomorrow = datetime.today() + timedelta(days=1)
    start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 15, 30)
    end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 22, 00)

    calendar.create_event(
        summery='Test from python 2',
        description='Hi Jenia, this is the second time that I\'m trying to send for you\n'
        'an invitation from my POC Python code',
        start_time=start_time,
        end_time=end_time,
        invitations=[
            'roiegol9@gmail.com',
            'jenia50@gmail.com'
        ]
    )


if __name__ == '__main__':
    main()
