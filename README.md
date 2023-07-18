# ETL_BigData

This repository contains a web application for performing ETL (Extract, Transform, Load) processes on data and saving it in a database. It utilizes Flask as a web framework and Elastic Search for logs.

#### ETL Process

The ETL (Extract, Transform, Load) process is a common data integration process used in data warehousing and analytics. Here's a brief explanation of each step:

1. Extract:
   - The extract step involves retrieving data from various sources, such as databases, files, APIs, or web scraping.
   - In the context of this application, users can insert files in XLSX or CSV format to extract the data.

2. Transform:
   - The transform step involves cleaning, validating, and transforming the extracted data into a suitable format for analysis or storage.
   - This application provides functions for cleaning and managing the data, allowing users to apply transformations to the extracted data.

3. Load:
   - The load step involves storing the transformed data into a target database or data warehouse for further analysis and reporting.
   - The application saves the transformed data into a database for future retrieval and analysis.

#### Frameworks and Tools

The ETL_BigData application leverages the following frameworks and tools:

- Flask: Flask is a lightweight and extensible web framework used for developing web applications.
- Elastic Search: Elastic Search is a distributed, RESTful search and analytics engine capable of handling large amounts of data and providing powerful search capabilities.

#### Getting Started

To get started with the application, you need to install the required dependencies listed in `requirements.txt`. Run the following command to install them:

```shell
pip install -r requirements.txt


```shell
pip install -r requirements.txt
```
####  Running the ETL_App

To run the ETL_App, execute the following command:

```python
python app.py
```

