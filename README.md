# Financial Data API

Financial Data API is a project that allows users to store financial data in a database based on given stock/s to retreive. It provides two main endpoints: one for accessing processed data and another for calculating a statistics based on the stored data.

## Tech Stack
- Language: Python
- Framework: 
    - Django as main web framework, 
    - Django Rest Framework: as it offers flexible toolkit for building Web APIs
- Database: PostgreSQL
- Libraries:
    - `debugpy` enabling VSCode debugging feature.
    - `alpha_vantage` a wrapper module to get stock data/cryptocurrencies from the Alpha Vantage API.
    - `numpy` used it as it is a Python library that provides a multidimensional array object, various derived objects (such as masked arrays and matrices) as the documentation said.
- Tools: 
    - Git for version control
    - Docker for containerization
    - VSCode as code editor

## Features

- Retrieve and store the financial data of a given stocks (e.g., IBM, Apple Inc.) for the most recently two weeks. Stock sourced from AlphaVantage API
- Retrieve processed data for a given stock 
- Calculate statistics based on the stored data

## Installation
---

1. Clone the repository:
    ```
    git clone https://github.com/buffer808/python_assignment.git
    ```

2. Navigate to the folder and copy/rename the file `.env-example` to `.env`
    ```
    cp .env-example .env

    #or

    mv .env-example .env
    ```
    __Note__: make necessary adjustments to the file accordingly (ports, database credentials, and [AlphaVantage API Key](https://www.alphavantage.co/documentation/)).

3. Assuming you already have docker and docker-compose installed, run the container:
    ```
    docker-compose up
    ```

4. Done, you should be able to access it at [http://localhost:<APP_PORT>](http://localhost:5000)

<br>

## Retrieving AlphaVantage Data
---

1. Open your terminal and run the command below:
    ```
    docker-compose exec api /bin/sh -c "python get_raw_data.py"
    ```
    - The above command will retrieve the data from AlphVantage and will process the raw API data response to be stored into a table named `financial_data`, a sample output after process should be like:
        ```
        {
            "symbol": "IBM",
            "date": "2023-02-14",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "62199013",
        },
        {
            "symbol": "IBM",
            "date": "2023-02-13",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "59099013"
        },
        {
            "symbol": "IBM",
            "date": "2023-02-12",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "42399013"
        },
        ...
        ``` 
    - 

## API Endpoints
---

Currently this API provides two major endpoints:

### GET /api/financial_data

- This endpoint accept following parameters: start_date, end_date and symbol, all the parameters are optional
- This endpoint support pagination with parameter: limit and page, if no parameters are given, default limit for one page is 5
- This endpoint return a result with three properties:
    - data: an array includes actual results
    - pagination: handle pagination with four properties            
        - count: count of all records without panigation
        - page: current page index
        - limit: limit of records can be retrieved for single page
        - pages: total number of pages
    - info: includes any error info if applies

    Sample Request:
    ```bash
    curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2'

    ```
    Sample Response:
    ```
    {
        "data": [
            {
                "symbol": "IBM",
                "date": "2023-01-05",
                "open_price": "153.08",
                "close_price": "154.52",
                "volume": "62199013",
            },
            {
                "symbol": "IBM",
                "date": "2023-01-06",
                "open_price": "153.08",
                "close_price": "154.52",
                "volume": "59099013"
            },
            {
                "symbol": "IBM",
                "date": "2023-01-09",
                "open_price": "153.08",
                "close_price": "154.52",
                "volume": "42399013"
            }
        ],
        "pagination": {
            "count": 20,
            "page": 2,
            "limit": 3,
            "pages": 7
        },
        "info": {'error': ''}
    }

    ```

### GET /api/statistics
The API endpoint statistics performs the following calculations on the data in given period of time:
    - Calculate the average daily open price for the period
    - Calculate the average daily closing price for the period
    - Calculate the average daily volume for the period

    - the endpoint accept following parameters: start_date, end_date, symbols, all parameters are required
    - the endpoint return an result with two properties:
        - data: calculated statistic results
        - info: includes any error info if applies

Sample request:
```bash
curl -X GET http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM

```
Sample response:
```
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "symbol": "IBM",
        "average_daily_open_price": 123.45,
        "average_daily_close_price": 234.56,
        "average_daily_volume": 1000000
    },
    "info": {'error': ''}
}

```

## VSCode Debugging 
___

To enable debugging in VSCode using `debugpy`, follow these steps:

1. Open the `.env` file and change value of the variable `APP_DEBUG` to `True`
2. Run / re-run the container `docker-compose up`
3. Open `.vscode/launch.json` file and change the port number in `connect.port` to the same port as the assigned to `APP_DEBUG_PORT` in `.env` file (you can skip this step if no changes in port settings)
4. Now, open a `views.py` file thats associated to an endpoint, set a breakpoint in the code by clicking on the left gutter of the desired line. A red dot will appear indicating the breakpoint. 
5. Start debugging by selecting the "Python: Remote Attach" configuration from the drop-down menu in the debugger sidebar, and click on the "Start Debugging" button (or press F5).
6. Access the endpoint via Postman/browser. The execution will pause at the breakpoint, and you can now use the debugging features in VSCode to step through the code, inspect variables, and analyze the program's state.