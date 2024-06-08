# FreightHub

FreightHub is a web application designed to manage transport orders for a logistics company. The application is divided into four main modules: User, Planner, Dispatcher, and Driver. Each module serves a specific role in the workflow of managing transport orders.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
  - [User Module](#user-module)
  - [Planner Module](#planner-module)
  - [Dispatcher Module](#dispatcher-module)
  - [Driver Module](#driver-module)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Creation and management of transport orders
- Assignment of orders to drivers and vehicles
- Reporting and tracking of order progress
- Management of company and vehicle data

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/flask-freighthub.git
    cd flask-freighthub
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    flask db upgrade
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Usage

Visit `http://127.0.0.1:5000` in your web browser to use the application. The following endpoints are available:

- `/` - Home page
- `/user/register` - User registration
- `/user/login` - User login
- `/planner` - Planner dashboard
- `/dispatcher` - Dispatcher dashboard
- `/driver` - Driver dashboard

## Modules

### User Module

The User module handles user management, including registration, login, and authentication.

- `POST /user/register` - Registers a new user.
- `POST /user/login` - Logs in an existing user.
- `GET /user/logout` - Logs out the current user.

### Planner Module

The Planner module is designed for logisticians to create and manage transport orders and company data.

- `POST /planner/companies/new` - Creates a new company.
- `GET /planner/companies` - Lists all companies.
- `GET /planner/companies/<id>` - Shows details of a specific company.
- `POST /planner/companies/edit/<id>` - Edits a company.
- `POST /planner/companies/delete/<id>` - Deletes a company.
- `POST /planner/transportation_orders/new` - Creates a new transportation order.
- `GET /planner/transportation_orders` - Lists all transportation orders.
- `GET /planner/transportation_orders/<id>` - Shows details of a specific transportation order.
- `POST /planner/transportation_orders/edit/<id>` - Edits a transportation order.
- `POST /planner/transportation_orders/delete/<id>` - Deletes a transportation order.

### Dispatcher Module

The Dispatcher module is used for assigning orders to drivers and managing vehicles.

- `POST /dispatcher/tractor_heads/new` - Creates a new tractor head.
- `GET /dispatcher/tractor_heads` - Lists all tractor heads.
- `GET /dispatcher/tractor_heads/<id>` - Shows details of a specific tractor head.
- `POST /dispatcher/tractor_heads/edit/<id>` - Edits a tractor head.
- `POST /dispatcher/tractor_heads/delete/<id>` - Deletes a tractor head.
- `POST /dispatcher/trailers/new` - Creates a new trailer.
- `GET /dispatcher/trailers` - Lists all trailers.
- `GET /dispatcher/trailers/<id>` - Shows details of a specific trailer.
- `POST /dispatcher/trailers/edit/<id>` - Edits a trailer.
- `POST /dispatcher/trailers/delete/<id>` - Deletes a trailer.
- `GET /dispatcher/orders/active` - Lists all active transportation orders.
- `POST /dispatcher/orders/complete/<id>` - Completes a transportation order.

### Driver Module

The Driver module allows drivers to view and report on their assigned transport orders.

- `GET /driver/current-order` - Shows the current transportation order.
- `GET /driver/confirm-finish-order/<id>` - Confirms the completion of a transportation order.
- `POST /driver/finish/<id>` - Marks a transportation order as completed.
- `GET /driver/archived-orders` - Lists all archived transportation orders.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.


