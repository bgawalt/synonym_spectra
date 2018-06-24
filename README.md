# Synonym Spectra

This code powers a Twitter account which posts chains of synonyms, which lead
from a source word to its antonym: a spectrum of words.

Distinguishable, discernible, perceptible, faint, indistinct, indistinguishable.

I read some paper years and years ago, like a decade or so, that first told me
about these structures.  In their context, they were trying to use it to power
sentiment analyses -- call one antonym +1 and the other -1, and call every link
in the chain some fractional value between them.

Good, ample, wide, inaccurate, faulty, bad.

## Usage

```
$ python post_spectrum.py spectra.config spectra.db
```

where `spectra.config` is the configuration file used and `spectra.db` is the
Sqlite3 file housing the synonym chains.  More detail on both below.

Useful, good, complete, dead, unprofitable, useless.

## Dependencies

### Synonym spectra database

Before writing this bot code, I had already created a database of the spectra.
The posting code here expects to be fed that data in a Sqlite3 file, containing
a table called `SPECTRA`:

```
$ sqlite3 spectra.db
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
sqlite> .tables
SPECTRA
sqlite> .schema SPECTRA
CREATE TABLE SPECTRA(Id INT, PostCount INT, Start TEXT, End TEXT, Distance Int, Chain TEXT);
CREATE INDEX ROW_IDX on SPECTRA(Id);
sqlite> select count(*) from SPECTRA;
5577
sqlite>
```

For reference:

* `Id` is just a handy numerical identifier, unique to each chain
* `PostCount` is a field I use to track the number of times each chain has been
  tweeted, so I can avoid tweeting the same ones over and over
* `Start` and `End` encode the antonyms of the chain
* `Distance` is the number of hops in the chain -- when `Distance` is 3, that
  means the overall chain has four words in it (including the antonyms)
* `Chain` is the actual spectrum itself, with each word separated by a space

This database file doesn't actually appear in this repo.  I can send it to you
on request, I suppose, if you're interested.

I was very proud of myself, starting with just a massive collection of synonym
pairs and antonym pairs, then staying up late implementing
[Djikstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
over top of it to find the shortest path from one antonym word to its partner
by hopping synonym edges.  I got to build a priority queue!  Then I told my
wife about it and she said why didn't I just use breadth-first search since the
edges were all unweighted.  And I had no good answer for her.  Oh well.

Looking at this now, Djikstra's was probably the wrong way to go.  Encouraging
short chains seems like it also encourages using the most tenuous synonym-links
available.  Maybe I'll relax that shortness constraint some day and see what
unfolds.

Ongoing, continuing, last, past.

### Config file

Like a lot of my bots, I set up a text file, `spectra.config`, to manage the
details of posting.  It looks like:

TODO: describe this

Secret, clandestine, fraudulent, unfair, raw, overt.

### Libraries

I'm using Python 2.7 to run this.

This really only depends on the Tweepy library.  Here's what the virtual
environment I use to run the CRON job that tweets these spectra looks like:

```
$ pip freeze
argparse==1.2.1
tweepy==2.3.0
wsgiref==0.1.2
```

Order, management, control, subdue, overpower, rout, uproar, pandemonium, chaos.
