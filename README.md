# Incremental and Full Data Orchestration with:
#### Apache Airflow <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3EBBk3qLHKH6OVNKK7jtfe-cHnrgQFYqv0g&usqp=CAU" alt="Airflow" width="32" height="32"/>
#### Docker <img src="https://www.rorymon.com/blog/wp-content/uploads/2016/10/large_v-trans.png" alt="Docker" width="32" height="32"/>
#### PostgreSQL <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1200px-Postgresql_elephant.svg.png" alt="PostgreSQL" width="32" height="32"/>
#### Python <img src="https://aumoraes.com/blog/wp-content/uploads/2021/09/python_original_logo.png" alt="Python" width="32" height="32"/>


### This project is a poc of how to do incremental and full strategy with postgresql and apache airflow.

1. For setup it, you must have installed Docker and Docker-compose
2. Run it inside the project folder with: docker-compose up -d
3. Wait until the services going up (Maybe took around 4-5m depending of your hardware specs)

### For web access:
1. <b>Apache Airflow:</b> http://localhost:8081/	# airflow - superTest #
2. <b>Adminer:</b> http://localhost:33380/			# postgres - superTest #

### Python app
You should access the container with docker exec -ti python3-app sh in linux or simply click on access container in Docker for Windows (++ winpty docker exec -ti python3-app sh).

To run the feed process, run: python3 /app/code/feedDb.py

## The process is:
1. In every 5 minutes, the Airflow run the dag and the python3-app feed the database (PG) again.
2. Thats make a loop until the container dies (both)
3. The automatic feed amount is 10.000 dummy lines 
4. You can bring the data through Airflow, from SOURCE schema to TARGET schema. Both will be the <b>tb_radar</b> table.
5. The table creation is on the entrypoint in docker-compose.yml.
6. For every changes you can do it changing the code on <b>queries folder</b>
4. The faker is about radar traffic in Brazil (BR) and there should be some informations like:
	4.1 <b>ID</b> - The table unique ID, incremental;
	4.2 <b>UUID</b> - The UUID of the record;
	4.3 <b>RADAR_ID</b> - The ID of the TRAFFIC RADAR (suppose it to be in another table with specs [Not in this case])
	4.4 <b>LICENSE_PLATE</b> - Vehicle identification plate;
	4.5 <b>VEHICLE_MAKE</b> - Vehicle make;
	4.6 <b>VEHICLE_MODEL</b> - Vehicle model;
	4.7 <b>VEHICLE_COLOR</b> - Vehicle color;
	4.8 <b>VELOCITY</b> - Actual velocity captured by radar;
	4.9 <b>VELOCITY_LIMIT</b> - Max accepted velocity by this radar;
	4.10 <b>COUNTRY_CODE</b> - Country code (🇧🇷)
	4.11 <b>STATE_NAME</b> - State name in 🇧🇷
	4.12 <b>CREATED_AT</b> - Date of when this record entered in this table
	4.13 <b>UPDATED_AT</b> - Date of when this record got some update;
	4.14 <b>SOURCETIME</b> - Default sourcetime in UNIX timestamp.

For more information of how this process work you can find it in <b>docker-compose.yml</b>

# Enjoy.