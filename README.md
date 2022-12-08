# Real-time threat detection
- [Real-time threat detection](#real-time-threat-detection)
  - [Foreword](#foreword)
  - [Quick Glance](#quick-glance)
  - [Further Improvements](#further-improvements)
  - [Setup](#setup)
  - [Contributors](#contributors)

## Foreword
This application is the second iteration of a Challenge for Data Analytics Hackathon with improved performance and code quality. This iteration provides a full in memory streaming solution to the challenge keeping features up to date using redis (Kind of like the Online Store in a Feature Store). Features are not pulled for every request but are instead kept up to date using background threads to refresh the state every n seconeds(TTL configuruation in app/config). The state of the first iteration stil remains in the Hackathon Branch of this repository.

For Data Analytics Hackathon our Challenge requirement was to detect an insider privilege missuse detection based on the dataset provided by Lindauer, Brian (2020): Insider Threat Test Dataset[[1]]. The breakdown of steps how the problem was solved might be helpful on how to design such systems. 

[1]: https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247/1

## Quick Glance
The initial idea was to leverage some form of anomoly detection to identify outliers in the dataset. That is based on the assumption that the behaviour of insiders is different from typical behaviour which should account for the most of the logged traffic in an enterprise network. Allthough there are labels available for the use with a supervised approach this is somewhat not ideal from a business point of view where labeled insiders already did the damage before being available in the dataset. There was the possibility to aggregate the logs to user sessions by using the login and logoff event of ldap log. Nevertheless we made the decision to analyze every datapoint in realtime as it was produced by a source system instead of aggregating to sessions, so a bad action is identified immideatly and not only after the session finished. The approach is depicted using the following diagram:

![](img/in_memory_threat_detection.drawio.png)

We created our proof of concept as a real-time outlier detection system with the following aspects in mind:

1. Every datapoint and the dimensions like the user, the used pc, the time and the acitivity gets evaluated on its own. Then the sum is calculated into an overall score.
2. The Data is guided over all components by utilizing a Dataflow to allow for realtime processing as well as backtesting of changes to the overall scoring system in batch.
3. A timestamp is present on every event flowing through the system. The overall distribution of all timestamps was calculated by getting the day of week and the hour of that timestamp which then get counted and descendingly sorted to get top n%. (See "Distribution of Timestamps") 
4. For activities the evaluation was divided into two parts: We counted visited websites and generated top n% webpages to rank everything that is not in p96 as outliers where p99 will get a higher score than p97. For Devices we assumed that every usb connection event is somewhat negative. Then the score gets reduced by a factor of how frequently the role the user belongs to connects usb devices. (See "Distribution of USB Connections")
5. In a similar manner the usage of the pc got evaluated. The assumption was made that the usage of a new pc (not used by that user in last 30d) is somewhat negative. This components score got reduced by a factor of how many pcs a user's role is typically using. E.g. In this dataset the role of admin tends to connect to way more systems than the role of janitor does. (See "Distribution of PC Usage")
6. The system was designed to allow the usage of static systems like bad link lists to further influence the overall score in conjunction with this anomoly based approach.
7. We keep only the events in our frontend that scored highly and keep everything else in the lifecycle of the underlying message queue to account for some sort of protection of personal data. (See "Alerts Dashboard")  
8. With this approach the learned distributions and features of the system should be updated periodically in batch or directly calculated on streaming to amount for the changing environment that is present in an enterprise network. E.g. a new site is created in a different timezone. 

The system works without the usage of state of the art machine learning and leverages only pandas and statistics to score events.
One of our first attempts included machine learning technologies like isolation forests without having much success as the used dataset was not suited. And as Chip Huyen said in Desinging Machine Learning Systems[[2]]: 
"While it’s essential to stay up to date with new technologies and beneficial to evaluate them for your business,
the most important thing to do when solving a problem is finding solutions that can solve that problem."


[2]: https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/

| Alerts Dashboard | Distribution of USB Connections | Distribution of PC Usage | Distribution of Timestamps |
|--------------------------------------|--------------------------------------|--------------------------------------|--------------------------------------|
| ![](img/alerts.png) | ![](img/device.png) | ![](img/pc.png) | ![](img/time.png) |


## Further Improvements

The anomaly score can be used in conjunction with static systems like a list of bad webpages (here shown as an external system) to further improve the overall performance. The system then might be able to account for situations where people have knowledge about the way that scoring system works e.g. influencing the distribution of abnormal webpages by visiting the pages frequently at a common date and time.

## Setup

To download the required data and create a database run the following:
```
make data
```

Run the script to laod features into redis.
```
python load_features.py
```

Wait for completion of the script and run the dataflow.
```
python dataflow.py
```

This will run the sample.csv through the scoring system. The dataflow can be adapted to e.g. listen a kafka topic and write output e.g. to postgres. 

Once finished delete the redis container using:
```
make clean
```

## Contributors

Mark S,
Gökhan T,
Manuel S,
Deniz D,
Luis V,
Pierre R
