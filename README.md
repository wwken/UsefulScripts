##Useful scripts
This repo contains some small useful utility scripts that are written in python or shell.  They are all becoming very handy especially for heavy duty unix/mac programmers or system administrators.

### Installation (first time)
Step 1: clone this repo to your local drive, say under directory: /home/user1/
<pre>
user1@user1-machine:~$ <b>git clone https://github.com/wwken/UsefulScripts.git</b>
</pre>

Step 2: cd into UsefulScripts directory and run the install.sh
<pre>
user1@user1-machine:~$ cd UsefulScripts
user1@user1-machine:~/UsefulScripts$ <b>./install.sh</b>
</pre>

Step 3: Source the newly updated bash_rc
<pre>
user1@user1-machine:~$ <b>source "$HOME/.bash_rc"</b>
</pre>

### Update (for those who have previously installed already)
More simple!  Just follow the step 2 (i.e. just execute the <b>./install.sh</b>) in the above Installation section. 
### Usage
Basically in the terminal window execute the corresponding script.  For example, to execute the execScriptsWithRange.py, just do "execScriptsWithRange.py /home/kwu/scripts/runStep1.sh 20140101 20141231 30" any directory from the terminal

### What is each script?
<b>countNumOfMByptesOfaDistributedFolder.sh</b>
<br/>
This script becomes handy when you need to count how many mega bytes of data in a given distributed folder (can be s3 or hdfs...etc).

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

<b>searchAndReplaceInFolders.sh</b>
<br/>
This script is to search for a given string and replace it with another string in the given folder recursively.  

<b>telnetPort-Mac.sh</b>
<br/>
This script is to determinte who is listening on a given TCP port on Mac OS X
