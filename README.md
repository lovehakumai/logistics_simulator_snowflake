# Logistics Simulator

## Project Executive Summary
I deployed cost simulator application in snowflake.
This project includes features below

1. Python script which can create Table from Zip file uploaded to stage manually
2. Visualize the data with streamlit
---
## Streamlit OverView
This Logistics Simulator is already implemented in your snowflake environment   
[KAGGLE_LOGISTICS.DEV_ANALYTICS] and The Available role is above SYSADMIN Role. 

Here’s the description of each feature.

### ANALYTICS PAGE
The Most efficient Transport
On the top, shows the origin country and destination country and form section to setup the cost factor parameters fuel_increase_param, risk_avoidance_paramm weight. 

![Analytics Page](asset/1.png)  

![Total Cost](asset/2.png)  

Showing the total_cost of each transport mode above.

These are The detail of each cost which is used in total_cost calculation and changed by setting up the params on the top.  
![Detail Cost](asset/3.png)

#### Past metrics
Showing the 2 metrics [BadWeather], [Desrupt] to check the actual past history.
Detail chart will be shown by clicking 🔍Show Detail . The metrics and chart is calculated by the daterange setted up above.  
※Each metrics is aggregated with the base point grain level. 

![Past Metrics](asset/4.png)  

![Past Metrics](asset/5.png)  

#### Global Route Visualization  
To Show the origin and destination port place.

![Global Route](asset/6.png)  

### MONITOR PAGE
#### Monitor
Showing the consumed credits in this Streamlit app. The data is from INFORMATION_SCHEMA and this view doesn’t have specific columns of credit so that I calculated it based WAREHOUSE TYPE and usage time.  

You can get the collect credit information from ACCOUNT_USAGE but the data synchronize needs 1hour to 1 day. ※INFORMATION_SCHEMA remains only for 7days so this view only have the consumed credit in latest 7 days.  

![Monitor](asset/7.png)

### SETUP PAGE
#### Setup
Setup country, base point, port and each vehicle attribution here. You cannot see Analytics Page without setting up here.  
![Monitor](asset/8.png)

---

## Core Engineering Highlights
### FinOps / st.form, st.session_state , 

* ```st.session_state``` :   
Streamlit app saves the first values as cache in memory.  ```st.session_state``` is used to call the data in cache and make the calculate faster and make the computepool's working in shorter time.

* ```Create DataFrame with for loop``` :   
To avoid redundant code in making dataframe instances, I implemeted this logic.
```python
transport_mode_list = ['air', 'sea', 'road', 'rail']
sample_dict = {}
for mode in transport_mode_list :
    sample_dict[mode] = st.session_state[f'{mode}_sample']

df = pd.DataFrame({
    'transport_mode': transport_mode_list,
    'sample' : [ sample_dict[mode] for mode in transport_mode_list ]
})
```

* ```st.form``` : 
Streamlit is the functional application and it will run all scripts in one click.  it runs all the scripts by changing the one parameter and This feature causes additional cost in snowflake.   
So I implemented ```st.form``` widget in each filter or parameter input section which doesn't run all scripts unless users don't push the 'submit' button.  This will affect on the amount of credits.



### Object Oriented architecture
This application is composed by several pages and components so I implemented object oriented architecture to simplify the maintenance and customization.  

For example, each page has each class like ```Analytics_state```, ```Analytics_data```.   
* ```~state``` class : manages the st.session_state.
* ```~data``` class : used to access to the database in snowflake, or create dataframe for the page