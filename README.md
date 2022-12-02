# Watcher
Simple monitoring/health-checking tool

## Usage
Watcher is a client-server application:
1. Server (docker, django) receives metrics from clients, visualises them and sends alerts by email
2. Client (python script, json config) collects data from resources (actives) and sends them to the server

How to start monitoring:
1. Specify password for database on docker-compose.yml
2. Install the server
3. Add clients on the server
4. Set up clients on hosts
5. Run client's scripts
After these actions you will start to recieve metrics

How to start alerting:
1. Specify mail server's settings on docker-compose.yml
2. Add email addresses on the server interface
3. Specify limits for CPU, RAM and SWAP on active settings
After these actions you will start to recieve alerts by email when limits will be reached

How to manage users:
1. Administrative console: http://watcher_ip:8090/admin | Login to application: http://watcher_ip:8090/accounts/login/
2. Log in on administrative console as "admin"
3. Add new user on Users
4. Add new user to the one group: "managers" (only browse actives and metrics) or "administrators" (additionaly can add/manage actives and emails)
5. If you need a new one superuser (as "admin"), add "staff status" and "superuser status"

## Installation
1. Clone the project
2. Specify your own password for postgresql on docker-compose.yml
3. Specify your own mail settings on docker-compose.yml
4. Run docker-compose up and wait when installation will be done
5. Log in on http://watcher_ip:8090/admin (django admin) with default credetionals admin:watcheradmin and change password for "admin"
6. Add an active on the server's interface and follow the instruction
7. Execute watcher_agent.py as root
8. On a few seconds data will be displayed on the web interface

## Additional properties
1. Do not delete CONFIG file after installation, only if you want to produce full reinstallation

## License
BSD License

## Conclusion
Watcher is a study project on python+django