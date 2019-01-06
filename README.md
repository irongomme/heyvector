# Hey Vector

Here is a website made with to offer a catalog of Anki Vector sdk custom scripts. It provide community
contributions and give visibility to it. You can explore contributions, and add yours with your github account.

This is my first Flask project, so don't be cruel ;-)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and
testing purposes.

### Prerequisites

Be sure to have those libraries :

  - Python3
  - pip3

### Installing

A step by step series of examples that tell you how to get a development env running

First clone project and install pip dependancies :

```
$ git clone https://github.com/irongomme/heyvector
$ cd heyvector
$ pip3 install -r requirements.txt --user
```

Configure your app :

```
$ cp settings.cfg.tmpl settings.cfg
```

Then edit settings.cfg to put your own values :

  - SECRET_KEY : Flask encryption string
  - GITHUB_CLIENT_ID : ID for your github app to handle login
  - GITHUB_CLIENT_SECRET : Secret for you github app

Run the local development server :

```
$ python3 -m flask run --debugger --reload
```

Finaly visit http://127.0.0.1:5000


## Roadmap

### Version 1.0.0

- [x] Ability to share github repository
- [ ] Exploring catalog
- [ ] Expose api endpoint to export catalog

### Version 1.1.0

- [ ] Set personnal Vector settings stored into browser
- [ ] Execute scripts online


## Built With

* [Flask](https://flask-login.readthedocs.io/en/latest/) - Web Framework
* [Semantic-UI](https://semantic-ui.com/introduction/getting-started.html) - UI Framework
* [Vue.js](https://vuejs.org/v2/guide/) - Vue.js 2


## Authors

* **irongomme** - *owner* - [irongomme](https://github.com/irongomme)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
