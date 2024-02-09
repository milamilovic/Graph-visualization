# Graph explorer

## Team
- Mila Milović SV22/2021
- Sonja Baljicki SV59/2021
- Isidora Aleksić SV36/2021
- Dunja Matejić SV21/2021
- Valentina Jevtić SV11/2021


## Getting Started 


### Python 3.9 or higher

You can check your Python version by running the following command: 

`python --version`



### Activating the Virtual Environment

To be able to use pip command you can install it following these instructions

[https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)




To activate the virtual environment using the provided scripts, follow these instructions based on your operating system:

`source venv_name/bin/activate`  for Linux

`venv_name\Scripts\activate`  for Windows



### Installation 

 To install all the packages, run following commands inside venv: 
 
`.\install.bat` 

To check if packages are installed, run following command: 

`pip list`



### Running

Navigate to Django project graph_expolrer and run command:
`python manage.py runserver`



### Usage

On the page you first have to add a new workspace and apply it. Then you can choose simple or block visualizer, enter file path and choose one of loaders. When the graph is generated you can search or filter it by entering queries. The query for filtering should look like this:
`<attribute_name> <comaparator> <attribute_value>` .
Comparator can be `==,>,>=,<,<=,!=` .
The graph is shown in the main view, tree view and bird view.
You can also zoom the graph, drag and drop and click the nodes.
