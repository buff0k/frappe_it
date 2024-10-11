## Frappe IT

A Frappe App that leverages ERPNext and HRMS to manage cellphone billing and other IT needs.


### Requirements:

1. [Frappe Framework](https://github.com/frappe/frappe) Installed and Running a Bench serving a site;
2. [ERPNext](https://github.com/frappe/erpnext) Installed on your Bench Instance;
3. [HRMS](https://github.com/frappe/hrms) Installed on your Bench Instance;
4. Having set up at least one Company in ERPNext; and
6. Having set up at least one Employee in HRMS.


### How to Install

Log into your server as your frappe-bench user and cd to your frappe-bench folder

````
bench get-app https://github.com/buff0k/frappe_it
````

````
bench --site your.site install-app frappe_it
````


### What is Working

So far I haven't gotten to everything yet, but you can import Vodacom Corporate Bills which will check against Sim Card Allocations and Employee Records, then you can generate an overage report based on contracts exceeding normal contractual values.


#### License

mit
