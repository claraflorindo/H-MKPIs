# H-MKPIs

This code is a Streamlit app that connects to an external MySQL database using SQLAlchemy, fetches data from three different tables (customers, articles, and transactions) using API calls.


Once the app is running, use the filters on the sidebar to filter the data and see the results of the four KPIs.

The KPIs displayed are:

What has each customer spent? (Bar chart)
How many purchases has each customer made? (Bar chart)
Total earnings per colour (Bar chart)
Total earnings per Club member status (Pie chart)

The app also displays three metrics:
Average amount spent by customers
Average number of purchases for each customer
Max earnings colour: (name of the colour with the highest earnings)

To deploy this application on App Engine, there are two folders required. Each folder should contain an app.yaml, requirements.txt file, and the main.py file. One folder is for the API, and the other is for the Streamlit application. These files define the configuration for the App Engine deployment, the dependencies required by the application, and the main code of the application.

The app.yaml file specifies the runtime environment and other settings for the App Engine application. The requirements.txt file lists the required Python packages and their versions. The main.py file contains the Python code for the application, which will be executed on the App Engine.


## Deployment link
https://20230330t150155-dot-streamlit-dot-careful-ensign-377008.oa.r.appspot.com/


