Shuffle Lunch
--------------

## Workflow
 - Use the `recurringEventId` to go out to google calendar to get the event for the current day
 - Expand `calendarGroupAlias` so that we can get the response for every user that has been invited to the event
 - Create randomized groups based on `groupSize`
 - Using mailchimp, email every group with the `subject` `fromEmail` `fromName` `template`
 - The template is a mustache html template that gets compiled for each email

## System Requirements
  - [Python](https://www.python.org/downloads/) 2.7 installed `brew install python`
  - [PIP](http://pip.readthedocs.org/en/latest/installing.html) - This comes with `brew install python`
  - [nosetests](https://nose.readthedocs.org/en/latest/) `pip install nosetests`

## Install project requirements

`make init`

## Run project

`make run`

## Run project in debug mode

`make debug`

## Test project

`make test`

## Adding new Shuffle

Added a new JSON object to shuffle/config/shuffle_data/shuffles.json
