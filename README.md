# Married-research-scholars-portal
Applications for apartments for married scholars

# Following Changes are Necessary before starting the app
- After cloning this repo, run `sudo service cron start` to start the cron jobs
- Change the values of the variables `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in the `settings_config.py` file
- Change the value of the variable `recepient_list` in `send_notifs_to_ARHCU()` function in `portal/utils.py`
## Optional
The database can be changed from Sqlite3 to MySql
