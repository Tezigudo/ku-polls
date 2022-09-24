# ku-polls
## Online Polls And Surveys

An application for conducting online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

### How to Install

make sure that you have [python](https://www.python.org/downloads/) in your computer

first, clone [**this repository**](https://github.com/Tezigudo/ku-polls) by type this command in your terminal at your choosen path

```sh
git clone https://github.com/Tezigudo/ku-polls.git ku-polls
```

go to project directory

```sh
cd ku-polls
```

next, you have to create file name `.env` to configuration **note that you may get your secretkeys [here](https://djecrety.ir)**

`.env` file template looks like [sample.env](sample.env) you can modify value and copy it into `.env`


by running [`setup.sh`](setup.sh) will set everythings ready for you to running the application by typing this command

you can initialize the polls by

```sh
bash setup.sh
```


### How to run

now to run server by type this

```sh
python manage.py runserver
```

go to `http://127.0.0.1:8000/` or `localhost:8000/` for application.  

## Demo Admin

|Username|Password|
|:--:|:--:|
|God|banana123|

## Demo User

|No.|Username|Password|
|:--:|:--:|:--:|
|1|banana|iloveapple|
|2|apple|ilovebanana|


lets enjoy the polls by me :)

---


## [Project Documents](https://github.com/Tezigudo/ku-polls/wiki/Home)

* [Task board](https://github.com/Tezigudo/ku-polls/projects)
* [Vision statement](https://github.com/nabhan-au/ku-polls/wiki/Vision-Statement)
* [Requirements](https://github.com/Tezigudo/ku-polls/wiki/Requirements)
* [Iteration 1 plan](https://github.com/Tezigudo/ku-polls/wiki/Iteration-1-Plan)
* [Iteration 2 plan](https://github.com/Tezigudo/ku-polls/wiki/Iteration-2-Plan)
* [Iteration 3 plan](https://github.com/Tezigudo/ku-polls/wiki/Iteration-3-Plan)
* [Iteration 4 plan](https://github.com/Tezigudo/ku-polls/wiki/Iteration-4-Plan)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/sdx
