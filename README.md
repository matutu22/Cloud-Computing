# Cluster and Cloud Computing Assignment 2 - Australian City Analytics
This repository is for subject Cluster and Cloud Computing Assignment 2, a system from twitter harvest and analysis programs to front end presentation with capability of dynamic deployment by Boto and Ansible.

------------
## Group member:
Zhenqian Hou          ID: 720261

Chi Zhang            ID: 775016

Chenhan Ma            ID: 823289

Minhan Yan           ID: 805103

-------------
# System Instructions

## File specification
* Ansible folder: Contains all the ansible scripts and the Boto script for setting up instances.
* Data folder: Contains all the data downloaded from Aurin portal.
* Javasourcecode folder: Contains source code for ASX200 program and twitter harvest program using BFS that get followers.
* Search folder: Contains twitter harvest programs that collect tweets by Search API by twitter.
* Streaming folder: Contains twitter harvest programs that collect tweets by Streaming API by twitter.
* Weather folder: Contains programs for collecting weather data.
* Cloudcomputing-cd6482d4da27.json: Crediential file for accessing Google Cloud SDK.
* Analysis.py: Analysis program.
* Analysis_fin.py: Analysis collected finance related tweets program.
* Jars: Java jars for ASX200 and get followers collecting tweets.
* Frontend folder: Contains front end presentation build by Django.
--------------
## Test instructions

* Run `python connectboto.py ` inside ansible folder. This will connect to nectar with credentials, create 4 instances on the cloud and create 4 volumes and attach to each instance. All the ip addresses will be output to “host.ini” for using ansible.
  
* Run ansible command with the format below:
  `ansible-playbook -i Path/to/host/file/hosts.ini -u ubuntu --key-file=PATH/TO/KEY/FILE/NAME.KEY  PATH/TO/YML/FILE.YML`
  
* Run the playbook named “congfigureall.yml”  which will install all the required environments and libraries of the system.
  `ansible-playbook -i ansible/hosts.ini -u ubuntu --key-file=cloudcomputing.key ansible/configureall.yml `

* User need to manully log on Nectar to configure the couchdb cluster.
* Run playbook  “uploadfiles.yml”  will upload all the files required.
* Run playbook  “runprograms.yml” will run all the required programs.
* Note that in order to run the program, the system need to run Corenlp server in advance which is configured in runprograms.yml.
* For checking disk space statistics, run “checkdisk.yml” with additional variables：`--extra-vars “hosts=xxx”` to check VM xxx. 
* For checking and manage processes, run “checkprocess.yml” with additional variables：`--extra-vars “hosts=xxx”` to check VM xxx. 
------------
[Stanford Corenlp](https://stanfordnlp.github.io/CoreNLP/index.html)

This system requires Stanford Corenlp downloaded and run as server.

## Youtube Link
* https://youtu.be/dM-csF9tm4g
