Mimeograph -- YouTube & Audio Transcription Software from Atomic
=================================================================

This program is a Python based YouTube and audio transcriber that uses the open-source OpenAI Whisper Speech Recognizer/Transcription module found on GitHub, that stemmed from the Atomic Music Bot.

When opened, the software prompts the user to paste a YouTube URL, or select an audio file as well as select the file format to transcribe to (either .TXT or .RTF). 

After, it will download a .webm file of that video to it's directory. Once downloaded, it transcribes the video, and outputs the result to the "Output" folder. 

The program then deletes the original .webm download to save space. The file is downloaded contains JUST audio, no video.

The software does NOT directly interact with the YouTube video stream. Because of this, I can not guarantee it will work on your computer, or your internet connection.

If you see an HTTP error (probably 403), it likely means that dependencies need to be updated via the UpdatePackage.sh / UpdateRequirements.exe files.

If it still occurs, I am most likely unable to fix it as it is caused by a direct "wall" put up by YouTube themselves, and varies depending on which machine the program runs on.



INSTALLATION FOR WINDOWS BASED MACHINES:
===============

0. Download the Mimeograph-win.zip file from GitHub

1. Extract the Mimeograph folder from the downloaded zip file.

2. Install program libraries by running InstallRequirements.exe

3. Run "Mimeograph.exe"

4. Periodically run "UpdatePackages.exe" to keep libraries up to date.


INSTALLATION FOR LINUX/MAC/UNIX BASED MACHINES:
==================================

0. Download the Mimeograph.zip file from GitHub

1. Extract the Mimeograph folder from the downloaded zip file.

2. Through the Terminal, CD to the Mimeograph folder.

3. Open InstallerPackage.sh through the Terminal by running the command "./InstallerPackage.sh" (without quotes) -- this will install the program's dependencies.

3.1. (OR) Run the program through Terminal directly. -- CD to the folder, and type "python3 Mimeograph.py" (without quotes)

4. Open UpdatePackage.sh through the Terminal by running the command "./UpdatePackage.sh" (without quotes) -- this will update dependencies (if there is an update)

5. Double click the "run.sh" file, and select "Run in Terminal".

6. Periodically run "UpdatePackage.sh" to keep dependencies up to date.


Closing Statement:
============

This program is Open-Source. You are free to make any and all modifications to this program as desired. If you have a fix or an improvement that you made, and would like to have it added, let me know.

This program was made by using existing libraries and modules found on GitHub. Credit for usage of these goes back to their respective owners.

As of 5/3/2025, "Atomic Incorporated" does not exist (at least under me). There are no copyright holders. I do not have a copyright on this program. The name is for visuals exclusively.

https://www.atomiccorp.org/
