# watcher
Watcher is a study project on python+django
Simple monitoring/health-checking tool

## Installation
1. Install your own password for postgres docker-compose.yml and settings.py
2. Use docker-compose.yml to run watcher
3. Add active on the web interface
4. Copy watcher_agent.* files to hosts
5. Edit watcher_agent.json (necessarily: token and api ip)
6. Execute watcher_agent.py
7. Data will be displayed on the web interface

## Status
This is a prototype of a future pet-project
Nearest To-Do:
1. Boundary values and "no data"-exceptions
2. Move "executive" code from views to separate classes
3. Authorization for web and api
4. Auto-refresh pages
5. Appearance (style, tables, add/edit/delete pages...)
6. Alerting (on the web interface, by e-mail)