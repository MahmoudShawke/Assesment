Models : Employee   , Attendance ,Checks

 - Employee Can Make one Attendance in the Day but Can 
  Make more Checks.
 - Employee When Register take from him mac address to Prevent Other user make Attendace for him <br/>
 - Employee can't make attend , Check before Login (PYJWT Auth) <BR/>
 - Employee Has Relation with Attendance<BR/>
 - Attendance Has Relation with Check<BR/>


Configurations <BR/>
- python -m venv  <BR/>
- venv\Scripts\activate <BR/>
- PIP INSTALL -r requirements.txt <BR/>
- Create db IN Postgress Name Lavloon
- change Configurations for setting.py host , User ,Password 
- python manage.py makemigrations  <BR/>
- python manage.py migrate <BR/>
- python manage.py runserver  <BR/>
  
 <BR/>
APIS <BR/>
- api/register: Employee Register  <BR/>
- api/Login   : Employee LOGIN <BR/>
- api/logout  : Employee Logout<BR/>
- api/attend  : Show The all attendance For User is Logged <BR/>
- api/submit  : Submit Attendance IF Valid <BR/>
- api/check   : Show All Checks for USER is Logged  <BR/>
- api/checkio : Check IN or Check OUT As a Conditions

