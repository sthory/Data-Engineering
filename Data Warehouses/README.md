### Project 3: Create a Data Warehouse with AWS Redshift
#### Summary

- Introduction
- Data Warehouse Schema Definition
- ETL process
- Project structure

The Sparkify company wants to move its data and processes to the AWS cloud. This data is in S3, under a directory of JSON logs containing the user's activity in the application and in a JSON directory with the songs of your application.

The task is to create an ETL pipeline that pulls your data from S3 and puts it in Redshift to transform into a set of dimensional tables and then you can find information about the songs your users listen to. The database and the ETL pipeline will then be tested by running the queries.

The project will use the resources of Amazon Web Services (AWS):

- AWS Redshift (Clusters)
- S3

The data that is ingested into the data warehouse is in two public S3 buckets:

- Group of songs, contained in "s3: // udacity-dend / song_data", has information about songs and artists.
- Event bucket, contained in "s3: // udacity-dend / log_data", it has information about the actions performed by the users, what song they are listening to, and as it has different directories, a JSON descriptor file is needed that will be used to extract data from the folders by path. The descriptor file "s3: //udacity-dend/log_json_path.json" is used and therefore there is no common prefix in the folders.

This data needs to be ingested into AWS Redshift using the COPY command. This command fetches JSON files from repositories and copies them to staging tables within AWS Redshift.

#### Song dataset structure:

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

#### Log Dataset structure:

artist, auth, firtName, gender, itemSession, lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, userid

#### Data Warehouse Schema Definition
Schema of the database:

Table: staging_events

    artist VARCHAR
    auth VARCHAR
    firstName VARCHAR(50)
    gender CHAR
    itemInSession INTEGER
    lastName VARCHAR(50)
    length FLOAT
    level VARCHAR
    location VARCHAR
    method VARCHAR
    page VARCHAR
    registration FLOAT
    sessionId INTEGER
    song VARCHAR
    status INTEGER
    ts BIGINT
    userAgent VARCHAR
    userId INTEGER
    

Table: staging_songs

    num_songs INTEGER
    artist_id VARCHAR
    artist_latitude FLOAT
    artist_longitude FLOAT
    artist_location VARCHAR
    artist_name VARCHAR
    song_id VARCHAR
    title VARCHAR
    duration FLOAT
    year FLOAT
    
    
Table: songplays

    songplay_id INTEGER IDENTITY (1, 1) PRIMARY KEY 
    start_time TIMESTAMP
    user_id INTEGER
    level VARCHAR
    song_id VARCHAR
    artist_id VARCHAR
    session_id INTEGER
    location VARCHAR
    user_agent VARCHAR

DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY ( start_time )


Table: users

    userId INTEGER PRIMARY KEY
    firsname VARCHAR(50)
    lastname VARCHAR(50)
    gender CHAR(1) ENCODE BYTEDICT
    level VARCHAR ENCODE BYTEDICT

SORTKEY (userId)


Table: songs

    song_id VARCHAR PRIMARY KEY
    title VARCHAR
    artist_id VARCHAR
    year INTEGER ENCODE BYTEDICT
    duration FLOAT

SORTKEY (song_id)


Table: artists

    artist_id VARCHAR PRIMARY KEY 
    name VARCHAR
    location VARCHAR
    latitude FLOAT
    longitude FLOAT

SORTKEY (artist_id)


Table: time

    start_time TIMESTAMP PRIMARY KEY 
    hour INTEGER
    day INTEGER
    week INTEGER
    month INTEGER
    year INTEGER ENCODE BYTEDICT 
    weekday VARCHAR(9) ENCODE BYTEDICT
)
DISTSTYLE KEY
DISTKEY (start_time)
SORTKEY (start_time)


#### ETL process

SQL is used for all transform logic (ETL) in Redshift.

Main steps:

- Ingest data from s3 public repositories into staging tables:
- Insert record in star schema from staging tables

Insert into staging events:

    staging_events_copy = ("""
    COPY staging_events
    FROM {}
    iam_role {}
    FORMAT AS json {};
    """).format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

Insert into staging songs:

    staging_songs_copy = ("""
    COPY staging_songs
    FROM {}
    iam_role {}
    FORMAT AS json 'auto';
    """).format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])
    
#### Insert data into star schema from staging tables

Insert into songplays table:

    INSERT INTO songplays (START_TIME, USER_ID, LEVEL, SONG_ID, ARTIST_ID, SESSION_ID, LOCATION, USER_AGENT)
    SELECT DISTINCT TIMESTAMP 'epoch' + (se.ts / 1000) * INTERVAL '1 second' as start_time,
           se.userId, se.level, ss.song_id, ss.artist_id, se.sessionId, se.location, se.userAgent
      FROM staging_songs ss
     INNER JOIN staging_events se
        ON (ss.title = se.song AND 
            se.artist = ss.artist_name)
       AND se.page = 'NextSong'
       
Insert into users table:

    INSERT INTO users
    SELECT DISTINCT userId, firstName, lastName, gender, level
      FROM staging_events
     WHERE userId IS NOT NULL
       AND page = 'NextSong'
       
Insert into songs table:

    INSERT INTO songs
    SELECT DISTINCT song_id, title, artist_id, year, duration
      FROM staging_songs
     WHERE song_id IS NOT NULL
     
Insert into artists table:

    INSERT INTO artists
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
      FROM staging_songs
      
Insert into time table:

    INSERT INTO time
    SELECT DISTINCT TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' as start_time,
           EXTRACT(HOUR FROM start_time) AS hour,
           EXTRACT(DAY FROM start_time) AS day,
           EXTRACT(WEEKS FROM start_time) AS week,
           EXTRACT(MONTH FROM start_time) AS month,
           EXTRACT(YEAR FROM start_time) AS year,
           to_char(start_time, 'Day') AS weekday
      FROM staging_events
      

#### How the project is structured

- create_tables.py: With this script you can delete the old tables (if they exist) and it will create the tables again.

- sql_queries.py: This is where the ETL is located. All transformation processes in SQL are done here.

- etl.py: This is a script that organizes ETL process.

- dhw.cfg: The credentials and information about AWS resources are stored here.

- README.md is where provide discussion on the process and decisions for this ETL pipeline.
      