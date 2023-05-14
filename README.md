# Django ChatGPT Client
This project is a django implementation of using OpenAI API key to have a custom ChatGPT client. 
_Notice_: **You need OpenAI API key so you can use this project. Get it from [here](https://platform.openai.com/account/api-keys)**

# Features
- The default settings of the project is that the admin creates users in the database and each user can have its own chat history.
- Users have to login to to have access to the chat.
- After each refresh or login user sees 10 recent messages.
- Admin can create users and give them access to use the chat. Also Admin can limit how many tokens they can use. The default for free trial is 4096 tokens. _Learn more about tokens in chatgpt [here](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)_
- The send function checks the token limit of the user and sends the best number of messages in history of user's chat, so it doesn't get token limit error.

# How to use
1. Clone the project
2. Go to the project's directory
    ```bash
    cd DjangoChatGPT
    ```
3. Create a virtual env
    ```bash
    python3 -m venv venv
    ```
4. Activate the venv
- **Linux**:
    ```bash
    source venv/bin/activate
    ```
- **Windows**:
    ```cmd
    venv\Scripts\activate.bat
    ```
5. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
6. Add your API key in "chatgptclient/settings.py"

    ```python
    API_KEY = "YOUR OPENAI API KEY"
    ```
7. Run the project:
 **_Make sure venv is activated_**
    ```bash
    cd chatgptclient
    ```
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```
- Create superuser (admin) so you can access admin page
    ```bash
    python manage.py createsuperuser
    ```
    ```bash
    python manage.py runserver
    ```
- In the browser the website runs on "http://127.0.0.1:8000" by default.
- You can go to "http://127.0.0.1:8000/admin/" to add Users.
- Also you have to add your admin user or any new user in ExtUser Table to allow access to use their own chat.
  

