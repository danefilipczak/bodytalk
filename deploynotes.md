
available on port 2200 at http://18.221.56.77 

# configurations 

Update all currently installed packages

-sudo apt-get update
-sudo apt-get upgrade

Change the SSH port from 22 to 2200
- Use `sudo nano /etc/ssh/sshd_config` and then change Port 22 to Port 2200 , save & quit.
- Reload SSH using `sudo service ssh restart`

Configure the UFW (Uncomplicated FireWall), very carefully. 
https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-16-04


# installed via apt-get

Apache, Postgresql, mod_wsgi, git

# installed via pip  

I found that the -H flag was required in order to make pip installations accesible to the Apache user. 

pip sqlalchemy
pip passlib
pip psycopg2
pip flask
pip flask-httpauth
pip oauth2client
pip requests






To adapt the ORM (sqlalchemy) from sqlite to postgreSQL, the basic procedure is to:
-create a new postgreSQL user, being sure to give it a password
-create a new database
-change the SQLAlchemy engine configuration string as documented here: http://docs.sqlalchemy.org/en/latest/core/engines.html


The apache error log is your friend
/var/log/apache2/error.log


# notes

The apache error log is your friend
/var/log/apache2/error.log

Apache is executed under its own user. Depending on how things are configured, this can lead to permissions errors. 

File names used in python scripts (e.g., client_secrets.json) must be prepended with full directory strings (relative paths do not work). 


# resources 

http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/

http://killtheyak.com/use-postgresql-with-django-flask/

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04