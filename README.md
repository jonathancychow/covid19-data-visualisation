# COVID 19 UK Cases Dashboard 

## Dashboard
![](img/dash.JPG)
The dashboard is hosted at Heroku, please see this [link](https://covid19-uk-surrey.herokuapp.com/).
## Python Library Installation 
- Run the command prompt with admin privilege and install the Python package Poetry as follow: 
```bash
pip install poetry
```
- Restart the command prompt and cd to the repo directory 
- Install the required libraries by invoking poetry 
```bash
poetry install 
``` 

## Get Going
- Install poetry following instruction from above, then invoke the poetry shell  
```bash
poetry shell 
``` 
- Start dashboard
```bash
dashboard
``` 
If you see the following, the dashboard is already running: 
```bash
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "dashboard-script" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on

```

By default, the dashboard will be running at localhost:8050, open a browser and visit http://localhost:8050. 