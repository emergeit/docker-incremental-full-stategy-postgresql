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
1. Apache Airflow: http://localhost:8081/	# airflow - superTest #
2. Adminer: http://localhost:33380/			# postgres - superTest #

### Python app
You should access the container with docker exec -ti python3-app bash in linux or simply click on access container in Docker for Windows.

To run the feed process, run: python3 /app/code/feedDb.py