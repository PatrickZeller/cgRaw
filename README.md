# cgRaw

## Overview
cgRaw is a Toolset for Nuke to help with cg render AOV compositing.
I used it on several commercial projects and after a few revisions i am finaly ready to release it to the world.

## Getting Started
Download the latest release and extract its contents to your .nuke directory into a subfolder called "cgRaw"
add the line "nuke.pluginAddPath("cgRaw")" to your ini.py file 
now you are ready to go ;)

## Setting up your AOVs to work with cgRaw
To make cgRaw aware of what AOV it needs to combine to recreate the beauty, 
you need to tag all AOVs that contribute to the beauty image with "col".
the ideal nameing convention is %lightname%_col_%lobename%.
If your renderer does not support per light per lobe AOVs just use one of the variables and name the other one "default" or something.

## Feedback
I want to hear from you to improve this tool!