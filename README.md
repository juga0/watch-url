# watch_url

Work in progress...

## Installation in Debian/Ubuntu

### System dependencies

`sudo apt-get install python-dev`
For lxml package:
 `sudo apt-get install libxml2-dev libxslt1-dev`
For PyYAML package:
`sudo apt-get install libyaml-dev`
For cryptograpy package:
`sudo apt-get install libffi-dev`

### With virtualenv

#### Obtain virtualenv

Check https://virtualenv.pypa.io/en/latest/installation.html or if Debian equal/newer than jessie (virtualenv version equal or greater than 1.9)

    sudo apt-get install python-virtualenv

#### Create a virtualenv

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/oiienv
    source ~/.virtualenvs/oiienv/bin/activate

#### Install dependencies in virtualenv

    git clone https://meta.openintegrity.org/agents/watch-url.git
    cd watch-url
    pip install -r requirements.txt

## Configuration

To change the host/port in which this agent listen, modify `config.yml`
`WEB_SERVER_ADDRESS` or create the environment variables:

    WATCH_PAGE_HOST='127.0.0.1' # 127.0.0.1 is the default
    WATCH_PAGE_PORT='8000' # 8000 is the default

To change the host/port in which the fetch- agent listen, modify `config.py` or
create the following environment variables:

    FETCH_PAGE_HOST='127.0.0.1' # 127.0.0.1 is the default
    FETCH_PAGE_PORT='8001' # 8001 is the default

Other variable that can be changed in `config.py` or via environment variables:
 * `STORE_CONFIG_DB` name of the DB where the agents will find their
   configuration. Default is `config`
 * `STORE_CONFIG_DOC` name of the document where this agent will find its
   configuration. For this agent the default is `pages-juga`
 * `STORE_DB` name of the database for this agent. Default is `pages-juga`
 * `STORE_URL` URL of the store. Default is `
   `https://staging-store.openintegrity.org`
 * `LOG_LEVEL` level of log details in the stderr. All log levels are stored
   in log/watch_url.log.
   Possible values are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`
   Default is `ERROR` when `DEBUG` environment variable is `False` or
   `DEBUG` when `DEBUG` environment variable is `True`
 * `DEBUG` whether debug mode is `True` or `False`. Default is `False`

## Running

    watch_url/watch_pages_tos_service.py

or

    cd watch_url
    watch_pages_tos_service.py

or

    cd watch_url
    nameko run watch_url --config config.yaml
    # NOTE that if runned in this way,
    it won't use the `FETCH_*` environment variables
