# bookstore-django

This is a simple bookstore website, with Python Django and Bootstrap.

**Dependencies**. Run

```
pip3 install -r requirements.txt
```

**Run**. First, migrate the database:

```
python manage.py migrate
```

Run django server:

```
python manage.py runserver 8000
```

After that, run the chat server:

```
python manage.py run_chat_server
```

Chat server will be running at port 5002. You can skip this, but the chat room will not be avaliable.

Then visit `localhost:8000`。











