Lunch Shuffler
--------------

ok, so we do shuffle lunch every other thursday. This has gotten a bit complicated, so here's the deal.

we've got a bunch of different notification groups:

- opt-out: people who don't even want to hear about it
- notify: people who want to hear about lunches, but don't want to automatically be signed up
- opt-in: people who want to be automatically signed up
- all: everyone in the entire group

I assume you'll keep records of all, opt-in and opt-out in the `entries` directory. Each line should just contain an email for each person in that group. The files can also contain comments and blank lines if that's useful.

Generating the mailing lists is simple, for the opt-in group run `bin/opt-in-emails`, and for the notify group run `bin/notify-emails`. 

So we need two templates notify & opt-in. These are stored in the `templates` directory.


From responses to those emails, we create a list of people who are in for the current lunch. Pipe that through the shuffler:

  bin/shuffler < current-lunch-emails.txt

It will split the folks into teams of 4-6 members. Have fun!
