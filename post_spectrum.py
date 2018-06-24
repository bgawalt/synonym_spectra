"""Query the database and post a spectrum to the account.

$ python post_spectrum.py spectra.config spectra.db
"""

# Select a random low-post-count spectrum.
SPECTRUM_QUERY = """
    select Id, Chain from SPECTRA where Id in
    (select Id from SPECTRA where length(Chain) < 270
     order by PostCount + random() limit 1)
"""

# Increment a chain's post count.  Needs a chain's ID number.
POST_COUNT_UPDATE_QUERY = """
    update SPECTRA set PostCount = PostCount + 1 where Id = ?
"""

import sqlite3
import sys

def FetchSpectrum(db_cursor):
    """Returns a pair: (chain id, chain text)."""
    db_cursor.execute(SPECTRUM_QUERY)
    return db_cursor.fetchone()

if __name__ == "__main__":
    config_file = sys.argv[1]
    db_file = sys.argv[2]

    # TODO: Try out `with` context:
    db = sqlite3.connect(db_file)
    db_cur = db.cursor()
    print FetchSpectrum(db_cur)

    db.close()
