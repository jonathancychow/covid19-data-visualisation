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
- Start the dashboard
```bash
python src\dashboard.py
``` 
By default, the dashboard will be running at localhost:8050, open a browser and visit http://localhost:8050. 