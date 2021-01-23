<h1>Purpose</h1>

Data modeling is done for a company called "Sparkify", they work with streaming music online. To begin, data on songs and user activity on the platform was collected. This data modeling is for the purpose of giving the analysis team the data necessary to obtain information from the modeled data.

<h1>Datasets</h1>

Song Dataset - Details and metadata about the songs
Log Dataset - User activity log

<h1>Database schema</h1>

The type of modeling that was used is "Star Schema", it was divided into a table of facts and dimensions so that it is structured.

<h2>Fact table</h2>

The fact table contains "song sets" that is made up of data about each user's activity.

<h2>Dimension tables</h2>

The "songs", "users", "artists" and "time" tables are the dimension tables and contain the data that make up the "facts" table.

<h1>ETL (Pipleline)</h1>

An ETL "pipeline" was made that takes the data from the "json" log files and then inserts it into the corresponding tables. First it was done in etl.ipynb and then it was generalized in "etl.py" which is the complete "pipeline".

<h2>File explanation</h2>

<h3>data:</h3> It is the folder containing the data sets of records and songs (data and logs).

<h3>sql_queries.py:</h3> It is a Python script and contains the necessary code (sql) for creation, drop and insertion for the database and its tables.

<h3>etl.ipynb:</h3> It is the prototype of what will be the complete "pipeline" (in jupyter notebook format).

<h3>etl.py:</h3> It is a Python script that has the complete ETL pipeline final code for the project, it is based on the work done in "etl.ipynb"

<h3>test.ipynb:</h3> It is a jupyter notebook type file and it is used to verify that the code of the scripts written to create tables and insert data work well.

<h3>create_tables.py:</h3> this program contains sql code to create and drop databases and tables (calls queries made in "sql_queries.py").

<h3>Readme.md:</h3> It is a brief documentation of the project.

<h1>Example of Fact Table</h1>

songplay_id	   start_time	       user_id	   level	song_id	 artist_id	session_id	location	                         user_agent
1	       00:22:07.796000	        91	       free	    None	  None	      829	   Dallas-Fort Worth-Arlington, TX	     Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)
2	       01:08:41.796000	        73	       paid	    None	  None	      1049	   Tampa-St. Petersburg-Clearwater, FL	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
3	       01:12:48.796000	        73	       paid	    None	  None	      1049	   Tampa-St. Petersburg-Clearwater, FL	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
4	       01:17:05.796000	        73	       paid	    None	  None	      1049	   Tampa-St. Petersburg-Clearwater, FL	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
5	       01:20:56.796000	        73	       paid	    None	  None	      1049	   Tampa-St. Petersburg-Clearwater, FL	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"




<h1>Example of Dimension Table</h1>


start_time	   hour	day	week month	year	weekday

00:22:07.796000	0	30	 48	  11	2018	  4
01:08:41.796000	1	30	 48	  11	2018	  4
01:12:48.796000	1	30	 48	  11	2018	  4
01:17:05.796000	1	30	 48	  11	2018	  4
01:20:56.796000	1	30	 48	  11	2018	  4


user_id	first_name	last_name	gender	level
92	      Ryann	      Smith	      F	   free
78	      Chloe	      Roth	      F	   free
73	      Jacob	      Klein	      M	   paid
12	      Austin	  Rosales	  M	   free
86	      Aiden	      Hess	      M	   free


song_id	              title	            artist_id	      year	duration
SOMZWCG12A8C13C480	I Didn't Mean To	ARD7TVE1187B99BFB1	0	218.93179


artist_id	        name	location	     latitude	longitude
ARD7TVE1187B99BFB1	Casual	California - LA	  NaN	      NaN


<h1>How to run this Project ?</h1>

1- To run the project, all the aforementioned files must be in a single folder.

2- In this order, first run the script "create_tables.py" ("python create_tables.py") is executed in the terminal, in this way all the previous databases are eliminated and new databases are created with their tables.

3- Then the script "etl.py" is executed ("python etl.py"), in this way the etl "pipeline" will be executed and data will be extracted from the log files and inserted into the fact table and the dimension tables.









