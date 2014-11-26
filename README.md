Utilities
=========

This repo contains some small useful utility scripts that are written in python or shell.

<b>execScriptsWithRange.py</b>
<br/>
This script is to execute a given script with the start date and end date and numOfDaysEachRun as parameters.
The motivitaion of having this script is that due to memory constraints in some systems, it makes sense to cut the whole execution into smaller chunks (paritioned by the date range) instead.

<b>findAllJarsByClass.py</b>
<br/>
This script is to find all jars that contain the given class name inside a given location.

<b>hadoopJobIdsKillWithRange.py</b>
<br/>
This script is to kill all hadoop jobs starting with the job id and incrementing one each time until up to n.

<b>killAllPSWith.py</b>
<br/>
This script is to kill all process specified by the grep search on all input arguements.

<b>mavenBuild.py</b>
<br/>
This python script is to automate all maven project builds in one click.  Since every time we building a whole project we need to maven build each sub project and wait for It's finish.  Very waste human being times.  
The first parameter is a path to the parent project folder.
The all other parameters are the project name that we want to maven build.

<b>renameFolders.sh</b>
<br/>
This script is to rename folders recursively.  
