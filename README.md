# Is Marked (v0.1.1)
IsMarked is an API developed for scheduling and managing appointments.

It was created to provide a back-end that front-end developers can use to easily create web apps.
The project's long-term goal is that, upon reaching version 1.0.0, it will be released for free use in developing applications for self-employed individuals (barbers, manicurists, hairdressers, psychologists, etc.), facilitating the organization and management of appointments.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Planned Features](#planned-features)
- [License](#license)

## Installation
1. Clone the repository:
```bash
 git clone https://github.com/Arielsva/IsMarked.git
```

2. Create virtual environment:
```bash
 python -m venv .venv
```

3. Enter the virtual environment:
```bash
 .venv\scripts\activate
```

4. Install dependencies:
```bash
 pip install -r requirements\common.txt
```


## Usage
To run the project, use the following command: (some API features will be unavailable)
```bash
 python manage.py runserver
```
To run the project with all features, use docker-compose:
```bash
 docker compose up
```

With the project running, access http://127.0.0.1:8000/doc/ in your browser to see the API documentation


## Planned Features
Future features to be added to the API:
- [ ] Management of business days and hours
- [ ] Registration of service options and prices
- [ ] Cancellation with deadline policy
- [ ] Audit logs of appointment changes
- [ ] Time zone support
- [ ] Export reports to PDF
- [ ] Integration with Google account
- [ ] Email confirmation
- [ ] Post-service evaluation
- [ ] Integration with Google Calendar
- [ ] Integrated online payments (Pix)
- [ ] Configurable cancellation fees


## License
This project is licensed under the [MIT License](LICENSE).