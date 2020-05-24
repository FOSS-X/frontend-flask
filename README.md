# Frontend for UDAPI

## Installation Instructions

1. Clone the repository

```sh
git clone https://github.com/FOSS-X/udapi-ui-v2.git
cd udapi-ui-v2
```

2. Create a virtual environment

```sh
virtualenv <virtualenvname>
source <virtualenvname>/bin/activate
```

3. Install the dependencies
```sh
pip install -r requirements.txt
```

4.Run the application. By default it runs at port:5000
```sh
export FLASK_APP=run.py
flask run -h localhost -p 5000
```
