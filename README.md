# myPythonRecap1DayScript
Simple script to turn my homework's CSV file to a SQL file based on a Relational Database Schema ... Just Refreshing my Python Knowledge.

## Relational Schema:
![Assign2_schema_default copy](https://github.com/EvanLei-git/myPythonRecap1DayScript/assets/71707767/7308f3bb-ca3c-4695-993d-87d821edf7b3)
(schema provided by my professor)

csv uploaded by [@rgriff23](https://github.com/rgriff23): https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

Input file: **athlete_events.csv**

Created sql: **done.sql**

Due to the [Equestrian events](https://en.wikipedia.org/wiki/Equestrian_events_at_the_1956_Summer_Olympics) in the Summer of 1956 the database includes 2 cities
with the keys (1956, 'Summer') so deleting the following line will remove the error.
> INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES (1956, 'Summer', 'Stockholm', 'SWE');


## Overview of the Data format in done.sql
```sql
set feedback off
set define off
ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';
INSERT INTO Country (NOC, Name) VALUES ('CHN', 'China');
INSERT INTO Country (NOC, Name) VALUES ('DEN', 'Denmark');
INSERT INTO Country (NOC, Name) VALUES ('NED', 'Netherlands');
INSERT INTO Country (NOC, Name) VALUES ('USA', 'United States');
INSERT INTO Country (NOC, Name) VALUES ('FIN', 'Finland');

...................
INSERT INTO Event (Ename, Sport, Gender, Category) VALUES ('Basketball Men Basketball', 'Basketball', 'Men', 'Basketball');
INSERT INTO Event (Ename, Sport, Gender, Category) VALUES ('Judo Men Extra-Lightweight', 'Judo', 'Men', 'Extra-Lightweight');
INSERT INTO Event (Ename, Sport, Gender, Category) VALUES ('Football Men Football', 'Football', 'Men', 'Football');
INSERT INTO Event (Ename, Sport, Gender, Category) VALUES ('Tug-Of-War Men Tug-Of-War', 'Tug-Of-War', 'Men', 'Tug-Of-War');
INSERT INTO Event (Ename, Sport, Gender, Category) VALUES ('Speed Skating Women 500 metres', 'Speed Skating', 'Women', '500 metres');

...................
INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES (1992, 'Summer', 'Barcelona', 'ESP');
INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES (2012, 'Summer', 'London', 'GBR');
INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES (1920, 'Summer', 'Antwerpen', 'BEL');
INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES (1900, 'Summer', 'Paris', 'FRA');
INSERT INTO Games (Year, Period, City, HostedInCountry) VALUES (1988, 'Winter', 'Calgary', 'CAN');

...................
INSERT INTO Athlete (AthleteID, Name, DateOfBirth, Sex, HasTeam) VALUES (1, 'A Dijiang', '06-09-1968', 'M', 'CHN');
INSERT INTO Athlete (AthleteID, Name, DateOfBirth, Sex, HasTeam) VALUES (2, 'A Lamusi', '14-05-1989', 'M', 'CHN');
INSERT INTO Athlete (AthleteID, Name, DateOfBirth, Sex, HasTeam) VALUES (3, 'Gunnar Nielsen Aaby', '17-07-1896', 'M', 'DEN');
INSERT INTO Athlete (AthleteID, Name, DateOfBirth, Sex, HasTeam) VALUES (4, 'Edgar Lindenau Aabye', '25-10-1866', 'M', 'DEN');
INSERT INTO Athlete (AthleteID, Name, DateOfBirth, Sex, HasTeam) VALUES (5, 'Christine Jacoba Aaftink', '22-01-1967', 'F', 'NED');

...................
INSERT INTO Participation (AthleteID, Year, Period, Event, Medal) VALUES (1, 1992, 'Summer', 'Basketball Men Basketball', 'NA');
INSERT INTO Participation (AthleteID, Year, Period, Event, Medal) VALUES (2, 2012, 'Summer', 'Judo Men Extra-Lightweight', 'NA');
INSERT INTO Participation (AthleteID, Year, Period, Event, Medal) VALUES (3, 1920, 'Summer', 'Football Men Football', 'NA');
INSERT INTO Participation (AthleteID, Year, Period, Event, Medal) VALUES (4, 1900, 'Summer', 'Tug-Of-War Men Tug-Of-War', 'Gold');

...................
```
