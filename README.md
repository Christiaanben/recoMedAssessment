# RecoMed Assessment

#### Developed by <ins>Bennie van Eeden</ins>

Provides an API end point that will calculate the total number of business seconds between two given times. A business
second is defined as any whole second that elapses after 08:00 and before 17:00 during a weekday (Monday - Friday) that
is not a public holiday in the Republic of South Africa. The end point must support only list GET requests and must take
two parameters: start_time and end_time. Parameter values will be in ISO-8601 format. You are guaranteed that start_time
will be before end_time. The end point must respond with only a single integer value for successful requests or a
suitable error message string for failed requests.

Please commit your code to a private GitHub repository and grant me read access. Here is my GitHub profile:
https://github.com/tasleemwilliams.

The repository should show your development workflow. The repository should include all code for the end point as well
as a script which automates deployment. You should also include automated testing in the repository.

1. Include the end point's URL in your submission
2. Complete in python
3. Do not use a package to calculate business seconds
4. Add Full Name in readme

## Setup & Deploy

Tested on Linux with python3

```shell
pip3 install -r requirements.txt
sudo chmod +x ./deploy.sh
./deploy.sh
```

## Endpoints

URL: http://localhost:5000

### Server Status

Checks if server is online.

* **URL**

  /
   
* **Method:**

  `GET`

* **Success Response:**
  
  * **Code:** 200 <br/>
    **Content:** `Server online.`

***

### Business Seconds

Returns the business seconds between a start and end time.

* **URL**

  /api/business-seconds

* **Method:**

  `GET`

* **URL Params**

  `start_time=[string(ISO-8601 date)]`
  
  `end_time=[string(ISO-8601 date)]`

* **Success Response:**

    * **Code:** 200 <br/>
      **Content:** `3600`

* **Error Response:**

    * **Code:** 400 BAD REQUEST <br/>
      **Content:** `{ "error" : "Invalid params provided" }`

## Post ReadMe meme

![pseudocode vs python code](https://i.imgur.com/2YyST5M.jpg)
