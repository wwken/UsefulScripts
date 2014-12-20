# Copyright (c) 2014 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu
# Date: 2014 December

if [ ! -d "/usr/local/bin/usefulscripts/lib" ]; then
	mkdir -p /usr/local/bin/usefulscripts/lib
fi 


curl https://github.com/wwken/UsefulScripts/blob/master/execScriptsWithRange.py > /usr/local/bin/usefulscripts/execScriptsWithRange.py
curl https://github.com/wwken/UsefulScripts/blob/master/findAllJarsByClass.py > /usr/local/bin/usefulscripts/findAllJarsByClass.py
curl https://github.com/wwken/UsefulScripts/blob/master/hadoopJobIdsKillWithRange.py > /usr/local/bin/usefulscripts/hadoopJobIdsKillWithRange.py
curl https://github.com/wwken/UsefulScripts/blob/master/killAllPSWith.py > /usr/local/bin/usefulscripts/killAllPSWith.py
curl https://github.com/wwken/UsefulScripts/blob/master/mavenBuild.py > /usr/local/bin/usefulscripts/mavenBuild.py
curl https://github.com/wwken/UsefulScripts/blob/master/renameFolders.sh > /usr/local/bin/usefulscripts/renameFolders.sh

curl https://github.com/wwken/UsefulScripts/blob/master/lib/__init__.py > /usr/local/bin/usefulscripts/lib/__init__.py
curl https://github.com/wwken/UsefulScripts/blob/master/lib/commands.py > /usr/local/bin/usefulscripts/lib/commands.py
curl https://github.com/wwken/UsefulScripts/blob/master/lib/printings.py > /usr/local/bin/usefulscripts/lib/printings.py

#curl https://github.com/wwken/UsefulScripts/blob/master/ > /usr/local/bin/
#curl https://github.com/wwken/UsefulScripts/blob/master/lib > /usr/local/bin/usefulscripts/lib/

chmod 700 /usr/local/bin/usefulscripts/*.sh       #Optional, in case the *sh is not executable
chmod 700 /usr/local/bin/usefulscripts/*.py       #Optional, in case the *py is not executable

if [[ $PATH != *"/usr/local/bin/usefulscripts"* ]]
then
	#echo "${PATH}:/usr/local/bin/usefulscripts"
  	echo "export PATH=\$PATH:/usr/local/bin/usefulscripts" >> $HOME/.bash_rc
fi



