**How to run the project**

- run this command to start the containers `docker-compose up`

- run this command to start the dag I have created `docker-compose run app airflow backfill slack_operator_testing -s 2015-06-01 -e 2015-06-07 -x`
