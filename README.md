# watch_url

Work in progress...

## Installation in Debian/Ubuntu

### System dependencies

`sudo apt-get install python-dev`

For lxml package:
 `sudo apt-get install libxml2-dev libxslt1-dev`

### With virtualenv

#### Obtain virtualenv

Check https://virtualenv.pypa.io/en/latest/installation.html or if Debian equal/newer than jessie (virtualenv version equal or greater than 1.9)

    sudo apt-get install python-virtualenv

#### Create a virtualenv

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/oiienv
    source ~/.virtualenvs/oiienv/bin/activate

#### Install dependencies in virtualenv

    git clone https://lab.openintegrity.org/agents/watch-url.git
    cd watch-url
    pip install -r requirements.txt

## Configuration

To change the host/port in which this agent listen, modify `config.yml` or
create the environment variables:

    WATCH_PAGE_HOST='watchhost'
    WATCH_PAGE_PORT='watchport'

and run `set_ip_port.py`

To change the host/port in which the watch- agent listen, modify `config.py` or
create the following environment variables:

    FETCH_PAGE_HOST='fetchhost'
    FETCH_PAGE_PORT='fetchport'

Other variable that can be changed in `config.py` or via environment variables:
 * `STORE_CONFIG_DB` name of the DB where the agents will find their
   configuration. Default is `config`
 * `STORE_CONFIG_DOC` name of the document where this agent will find its
   configuration. For this agent the default is `page-tos-juga`
 * `STORE_DB` name of the database for this agent. Default is `page-tos-juga`

## Running

    cd watch_url
    nameko run watch_url

