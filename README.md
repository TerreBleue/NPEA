Noise Pollution Exposure Analysis in Paris
=== 

## Teck Stack
- Python 3.13.3
- Docker 28.1.1
- Docker Compose 2.35.1-desktop.1

## Installation 
On Windows, install WSL and Docker Desktop.  
Then, on WSL, install Python. 

## Start 
Install the Python requirements with `pip install -r requirements.txt`  

Afterwards, create 3 differents terminals. 
- 1st: while Docker is running, start the Docker services with `docker-compose up -d`
- 2nd: start the Kafka consumer with `python "kafkaFunctions/consumer.py"`
- 3rd: start the Kafka producer with `python "main.py"`

At this point, the data should be retrieved by Spark and pushed to the MongoDB database.  
Wait a few seconds for the 2nd terminal to finish these actions.  
Subsequently, you may stop this terminal with `CTRL + C`.

Next, on the 2nd / 3rd terminal, run a Streamlit app with `streamlit run streamlit.py`. Leave the email empty.  
On a web browser, your app now should run on http://localhost:8501. 

