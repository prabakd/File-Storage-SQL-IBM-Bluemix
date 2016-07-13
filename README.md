# File-Storage-SQL-IBM-Bluemix
PreRequisites: 
1) Install flask and psycopg2 using pip command.
2) Create a postgre SQL DB and link it with your app in IBM Bluemix
3) Create the DB tables and insert the user details for login(See the createqueries.sql file for more info).
4) In the server.py script replace the "XXXXX" with your postgre SQL DB credentials

Simple Flask app to sore and download the files from SQL DB
------------------------------------------------------------------
This is a simple python program with flask web framework to do upload a file into postgre SQL DB. It has simple login screen and upload or download the file option. The files are loaded into database by reading the contents and after encoding it, it stores directly. For the download option the files are downloaded to the current directory after decoding it. 

To push the application into IBM Bluemix
1) Edit the Manifest file as per your application and host name

Note:
----------
Static directory and its contents are not used in this program. 
