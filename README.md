# Project

## Setting Up

- python
- project directory
- install virtualenv (to create virtual environment : so anyone can install the requirements)
- virtual environment (where everything we installed stored in this folder)
- install packages

```txt
    1. setup folder
    2. install virtualenv
        > pip install virtualenv
    3. virtualenv setup
        > python -m virtualenv .venv
        or
        > py -3 -m venv .venv
    4. activate env
        > .venv\scripts\activate
    5. install flask
       > pip install flask
    6. setup other files
    7. if finished configuring, run command:
        > python app.py
    - start creating, using a web server
```

```txt
    for front end setup
        requires to install node.js
        and use command: npx create-react-app client
        to get started, 'client' is just a folder name.
        npx create-react-app .
        use . to install in current directory

    to go in the front end
        use command: cd client
                     npm start
```

 npm start
    Starts the 'development' server.

  npm run build
    Bundles the app into static files for 'production'.

  npm test
    Starts the 'test' runner.

  npm run eject
    'Removes' this tool and 'copies' build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!

## Extention needs

- ES7 React/Redux/GraphQL/React-Native snippets
  - for easy native react coding (example, using rcf and enter)

## Activation

@important!

```txt
  cd app
  .venv\scripts\activate
  python server.py

  cd client
  npm start
```

## Installing the package that will help us get the files we want from forms

```cmd
  # if error occurs
  python -m pip install --upgrade pip
  # install flask_wtf
  pip install flask_wtf wtforms
```

> then use it in the file to get forms
  > source: <https://www.youtube.com/watch?v=GeiUTkSAJPs&ab_channel=ArpanNeupane>

```py

```

## References

<https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment>

solution for file upload

<https://www.askpython.com/python-modules/flask/flask-file-uploading>

<https://stackoverflow.com/questions/61628503/flask-uploads-importerror-cannot-import-name-secure-filename>

<https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask>

solution for permission error

<https://www.youtube.com/watch?v=bwduoqYRqjA&ab_channel=RomanDoesConsumerTips>

<https://www.youtube.com/watch?v=GeiUTkSAJPs&ab_channel=ArpanNeupane>

<https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/>
