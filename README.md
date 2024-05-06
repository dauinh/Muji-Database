# Muji Database Project

Welcome to the Muji Database Project! This project is part of a database class and focuses on building a database for Muji, a Japanese brand known for its high-quality products. The project involves setting up a database with MySQL, connecting it with Python, and working with various Python packages to manage and display data.

## Project Overview

Muji, originally founded in Japan in 1980, offers a wide variety of high-quality products, including household goods, apparel, and food. The name "Muji" is derived from the Japanese term "Mujirushi Ryohin," which translates to "no-brand quality goods." The brand is anchored on three core principles:

1. Selection of materials
2. Streamlining of processes
3. Simplification of packaging

The objective of this project is to create a database that stores information about Muji's products, customers, and sales, allowing efficient data management and insightful analysis.

## Installation

To set up the project, you need to have Python installed along with the following packages:

1. **mysql-connector-python**: A package used to connect Python with MySQL databases.
   ```bash
   pip install mysql-connector-python
   ```
2. **python-dotenv**: A package to load environment variables from a `.env` file.
   ```bash
   pip install python-dotenv
   ```
3. **pprint**: A built-in Python package for "pretty-printing" complex data structures.
   ```bash
   pip install pprintpp
   ```

## Getting Started

### Clone the repository

To get started, clone the repository:

```bash
git clone https://github.com/utran0612/Muji-Database.git
cd Muji-Database
```

### Set Up the Environment

1. Create a `.env` file in the project directory and add your MySQL credentials:

```bash
USERNAME = your_mysql_username
PASSWORD = your_mysql_password
```
2. Run **main.py** to start interacting with the database!
