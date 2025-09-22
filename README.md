# openf1-logger-and-interpreter
A fairly simple console program to download and (kind of) interpret data from the OpenF1 API. Part of a maths project for school about the normal distribution.


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
  One of the two modules used by this program to work with CSV files.

- <b>Pandas:</b><br>
  The second of the two modules used for CSV interpretation.

- <b>OS:</b><br>
  Used for directory management.


## Usage:
It's pretty simple, all you need to do is this:

1. Select the function you want to use in the home menu
2. Input the parameters that the program asks for
3. Wait for it to finish doing whatever you want it to do (this might take a while, so be patient and make sure to clear your schedule)

## Bugs/issues to look out for:
- the allpos.json file is  itself in sync with the laptime JSONs for every driver, and no it doesn't have any 'complete' tag, so if you stop the program partway through downloading info for a certain race, then the program will automatically assume that, since the allpos.json exists, that you have all the data for that race downloaded already- even if you actually only have like... 1 driver's timesheet downloaded in full. To fix this, delete the incomplete allpos.json <i>before</i> you restart the program. I don't have plans to fix this, so you'll have to do so yourself if you're really that pressed about it.
- On a similar note, driver timesheets don't mark themselves as complete either, so again, if it exists, the code will assume it's complete. Again: delete it before you restart it- and don't expect me to fix it anytime soon; I have no plans to.
- Only the download function works currently (as previously mentioned). This will be sorted very soon- there's NO way I'm gonna port all that JSON data through to Excel manually. That said, it'll just take you back to the homepage if you do try to run an incomplete function for whatever reason (even though I have made it <i>very</i> clear what is and isn't complete in the interface itself).


There's a ton of annotations in the code, so hopefully everything makes sense. If not, let me know and I'll take a look when I have time.


## To-Do:

1. Set up the fastest laps interpreter
2. Improve the interface & generally clean things up
