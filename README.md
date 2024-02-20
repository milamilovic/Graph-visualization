# Graph explorer

## Overview
The program, developed in JavaScript using Django and the D3 library, is a powerful tool for visualizing graphs. It supports plugins for both simple and block visualizations, as well as for JSON, RDF, and XML data sources, making it versatile and adaptable. With additional features like tree and bird views, multiple workspaces, and advanced filtering and searching capabilities, this tool is an essential asset for data visualization and analysis.

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

## Images
#### graph visualization
![Graph visualizer - Google Chrome 2_20_2024 7_22_44 PM](https://github.com/milamilovic/Graph-visualization/assets/104532211/e2c9a16c-8fc8-48b1-9d18-97e61effb9b0)
#### bird view example
![Graph visualizer - Google Chrome 2_20_2024 7_23_43 PM](https://github.com/milamilovic/Graph-visualization/assets/104532211/4ed54b90-0b6a-4fd5-a7d3-dfb681184bb2)
#### clicking on node
![Graph visualizer - Google Chrome 2_20_2024 7_23_07 PM](https://github.com/milamilovic/Graph-visualization/assets/104532211/243e46cc-d15c-4403-b050-c7bdfd7b94ba)
#### dragging the nodes
![Graph visualizer - Google Chrome 2_20_2024 7_24_10 PM](https://github.com/milamilovic/Graph-visualization/assets/104532211/9781f274-5157-4b94-b36b-f1808bd2a983)
#### menu
![Graph visualizer - Google Chrome 2_20_2024 7_24_20 PM](https://github.com/milamilovic/Graph-visualization/assets/104532211/dd59c724-2fd2-4554-a0ee-a5a8e236ad5d)
