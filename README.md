# openf1-logger-and-interpreter
A fairly simple console program to download and (kind of) interpret data from the OpenF1 API.


## Prerequisites:
Here's the modules you'll need to get this to run, and why:
- <b>JSON:</b><br>
  So the program can make, edit, and delete JSON files for data storage.

- <b>Math:</b><br>
  Used to configure some values related to the laptimes.

- <b>URLlib:</b><br>
  So the program can talk to the API.

- <b>SSL:</b><br>
  Not <i>strictly</i> needed, but skips the SSL certificate verification process on the URL commands so that it can work on my school's WiFi- get rid of it if you want, but just remember to fix all the web search commands if you do.

- <b>Prompt_toolkit:</b><br>
  Purely for aesthetics, but the interactive functions do run off of it so you'll need to redo all of those if you don't want to use this module.

- <b>CSV:</b><br>
  This isn't being used for anything just yet, but it will be soon to reformat JSON data into CSVs for use in Excel.

- <b>OS:</b><br>
  Used for directory management.


## Usage:
It's pretty simple, all you need to do is this:

1. Select the function you want to use in the home menu (right now only the "download data" option actually works though)
2. Input the parameters that the program asks for
3. Wait for it to finish doing whatever you want it to do (this might take a while, so be patient and make sure to clear your schedule)

## Bugs/issues to look out for:
- the allpos.json file is  itself in sync with the laptime JSONs for every driver, and no it doesn't have any 'complete' tag, so if you stop the program partway through downloading info for a certain race, then the program will automatically assume that, since the allpos.json exists, that you have all the data for that race downloaded already- even if you actually only have like... 1 driver's timesheet downloaded in full. To fix this, delete the incomplete allpos.json <i>before</i> you restart the program.
- On a similar note, driver timesheets don't mark themselves as complete either. 
