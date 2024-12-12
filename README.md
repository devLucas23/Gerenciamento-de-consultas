#### Django Rest Framework (DRF)

Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Python using the Django web framework. It provides a comprehensive set of tools and features that make it easier for developers to create robust and efficient RESTful APIs.

#### System Requirements

To build web applications with DRF you will need to include the following requirements on your system:

- Python 3.10 or lattest version;
- Pip 22.0 or lattest version;
- Virtualenv 20.19 or lattest version;

### Quick Run

This command is used to execute the quick steps and start the virtual environment with the dependencies and then start the server.

~~~
    bash test.sh
~~~

If the command does not work, run the installation manually using the following step.

#### Quick Install

This guide aims to jump start the project settings and bring a fast hands-on DRF Project. However, to enable and run the project, some commands are still required.

- **Step 1** - Create a virtual python environment to install all required dependencies:
~~~
    python3 -m venv venv
~~~

- **Step 2** - Activate the virtual python environment:
~~~
    . venv/bin/activate
~~~

- **Step 3** - Install all dependencies:
~~~
    pip install -r requirements.txt
~~~

- **Step 4** - Run internal server and fun! ;)
~~~
    python manage.py runserver
~~~

Stop the server typing Ctrl+C in terminal. 

Project is based on [LISA DRF Quick Project!](<https://github.com/lisa-ufersa/django-quickproject>)

### Project constantly tested by SonarCloud
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DanielLinsAndrade_GerenciamentoDeConsultasMedicas&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DanielLinsAndrade_GerenciamentoDeConsultasMedicas)
