# CITS5505-Group-Project

## About our website
Welcome to our Survey Website! Our platform is designed to facilitate the creation, distribution, and sharing of surveys to collect valuable data and insights. Whether you're conducting academic research, gathering customer feedback, or simply seeking opinions on various topics, our website provides a user-friendly interface to manage all your survey needs.

### Key Features
- **Create Surveys**: Easily design surveys with customizable questions and options.
- **Answer Surveys**: Participants can conveniently respond to surveys.
- **User Management**: Register, manage user profiles, change password, reset password.

### More in the future:
- More types of Survey
- Compatibale with Social Media App
- Data Sharing
- And more ...
-----

## How to install and run project

1. **Clone the source code from github with following code**
```
git clone https://github.com/CITS5505GroupProject/CITS5505-Group-Project.git
```

2. **Setup virtual environment**
- **For `macOS` user:** 

    create environment:
    ```
    python3 -m venv groupprojectenv
    ```

    enter environment:

    ```
    source groupprojectenv/bin/activate
    ```
- **For `Windows` user:**

    create environment

    ```
    python -m venv groupprojectenv
    ```

    * enter environment (**Command Prompt**):

    ```
    groupprojectenv\Scripts\activate
    ```

    * enter environment (**PowerShell**):

    ```
    .\groupprojectenv\Scripts\Activate.ps1
    ```

3. **Install Dependencies (required packages)**
```
pip install -r requirements.txt
```

4. **Set up database wit Flask-migrate**
```
flask db upgrade
```

5. **Run project**
```
flask run
```

6. So now you have the website ran in your local host!

## How to launch website
After set up environment and installed required packages. And ran command line `flask run`. Open the link provided in your terminal, its normally `http://127.0.0.1:5000`.

-----

## How to test website using test files
Run the commond line to run test files
```
python -m unittest discover -s test
```
-----

## Group members
Students 
| Student           | UWA ID        | Github ID     |
| ------------------|:-------------:|:-------------:|
| Siyuan Zhou       | 23861658      | TonyZzz       |
| Shuangefei Li     | 23428364      | DoubleAshley/DoubleAshley00  |
| Qianqian Li       | 23770748      | qianqianli626 |
| Chinmai Ravindran | 23864156      | chinmaiii     |
