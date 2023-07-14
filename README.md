<h1>SMarket</h1>

CS2 trading platform where users can buy, sell, and trade skins. You can create trade offers that other users
can accept. Trades are processed after the guarantor reviews them.

https://github.com/Mykhailiuk66/SMarket/assets/110096259/8ba6e2c5-f878-4351-9711-734da117bce4


<h1>Getting Started</h1>

First clone the repository from Github and switch to the new directory:

```
$ git clone git@github.com:Mykhailiuk66/SMarket.git
$ cd SMarket
```

Activate the virtualenv for your project.

Install project dependencies:

```
$ pip install -r requirements.txt
```

Then simply apply the migrations:

```
$ python manage.py migrate
```

You can now run the development server:

```
$ python manage.py runserver
```
