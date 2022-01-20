- datacamp VM instance in GCP created
- connected to instance terminal through PUTTY and VSC
  - PUTTY 
    - create a .ppk key using PUTTYgen [GCP link](https://cloud.google.com/compute/docs/connect/create-ssh-keys#windows)
    - HOST name (External IP)
    - Connection/SSH/Auth - Browse key
    - Saved session - put new name
  - VSC
    - [link](https://faun.pub/connect-gcps-vm-with-vs-code-on-windows-10-b4fc7e73afea)
    - Cloud SDK Shell login > gcloud init
    - Power Shell ssh-keygen -t rsa -f [KEY_FILENAME] -C [USERNAME]
    - ssh-keygen -t rsa -f [KEY_FILENAME] -C datacamp
    - open file with notepad and copy the pwd (ssh-rsa key user) to GCP keys
    - VS Code, Remote-SSH (+) > ssh -i C:\\Users\\...\\[KEY_FILENAME] [USERNAME]@[VM's IP]

- install anaconda and change path
- install terraform
- install docker
- pgcli

- Create 3 containers

#### docker network
docker network create pg-network

#### docker with postgres
  docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /home/datacamp/data-engineering-zoomcamp/week_1_basics/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p  5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13

#pgcli -h localhost -p 5432 -u root -d ny_taxi

#### docker GUI postgres
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin \
dpage/pgadmin4


#browser: localhost:8080 -> create server
create server
-Docker postgres
Host: pg-database
port: 5432
username: root
password: root


## HOMEWORK
### Question 3. Count records
How many taxi trips were there on January 15?
This returns number of trips each day of the month
```
SELECT  COUNT(*), extract(day from tpep_pickup_datetime) as day,extract(month from tpep_pickup_datetime)  as month
from yellow_taxi_data

GROUP BY extract(day from tpep_pickup_datetime),extract(month from tpep_pickup_datetime)
Order by month,day
```
for January 15 specifically:
```
SELECT COUNT(*) from yellow_taxi_data 
 WHERE extract(day from tpep_pickup_datetime)=15
 AND extract(month from tpep_pickup_datetime)=1
```

### Question 4. Average
Find the largest tip for each day. On which day it was the largest tip in January?
```
SELECT 	extract(day from tpep_pickup_datetime) as day,
		extract(month from tpep_pickup_datetime)  as month, 
		max(tip_amount) as tip
 from yellow_taxi_data

 GROUP BY extract(day from tpep_pickup_datetime),extract(month from tpep_pickup_datetime)
 Order by month,day
```


### Question 5. Most popular destination
What was the most popular destination for passengers picked up in central park on January 14?
```
SELECT B."Zone",count(*)
from yellow_taxi_data as A
LEFT JOIN taxi_zone_lookup as B
on A."DOLocationID" = B."LocationID"
WHERE extract(day from tpep_pickup_datetime)=14
  AND extract(month from tpep_pickup_datetime)=1
  AND A."PULocationID" = 43
GROUP BY B."Zone"

ORDER BY count(*) DESC
```
"Upper East Side South"	97
"Upper East Side North"	94
"Lincoln Square East"	83

### Question 6.
```
select Z.from, Z.to, Avg(Z.total_amount) from
(
select A."from", B."Zone" as "to",A.total_amount from ( SELECT B."Zone" as "from", A."DOLocationID", A.total_amount
from yellow_taxi_data as A
LEFT JOIN taxi_zone_lookup as B
on A."PULocationID" = B."LocationID" ) as A

LEFT JOIN taxi_zone_lookup as B
 on A."DOLocationID" = B."LocationID" 
 
) as Z

GROUP BY Z.from,Z.to
ORDER BY avg DESC
```

"Alphabet City"		2292.4
"Union Sq"	"Canarsie"	262.85200000000003
"Ocean Hill"		234.51
"Long Island City/Hunters Point"	"Clinton East"	207.61
"Boerum Hill"	"Woodside"	200.3
"Baisley Park"		181.4425
