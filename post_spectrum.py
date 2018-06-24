"""Query the database and post a spectrum to the account.

$ python post_spectrum.py spectra.config spectra.db
"""


import random
import sqlite3
import sys


# Select a random low-post-count spectrum.
SPECTRUM_QUERY = """
    select Id, Distance, Chain from SPECTRA where Id in
    (select Id from SPECTRA where length(Chain) < 270
     order by PostCount + random() limit 1)
"""


# Increment a chain's post count.  Needs a chain's ID number.
POST_COUNT_UPDATE_QUERY = """
    update SPECTRA set PostCount = PostCount + 1 where Id = ?
"""


LINKING_TERMS = [" means ", " is the same as ", " equals ",
                 " is equivalent to ", " is essentially ", " is like ",
                 " is akin to ", ", a.k.a. ", ", i.e. ", " meaning ",
                 " as in ", " stands in for ", " replaces "]


def FetchSpectrum(db_cursor):
    """Returns a triplet: (chain id, chain distance, chain text)."""
    db_cursor.execute(SPECTRUM_QUERY)
    return db_cursor.fetchone()


def ChainStringToList(chain_str):
    sp_chain = chain.split()
    sp_chain[0] = sp_chain[0].upper()
    sp_chain[-1] = sp_chain[-1].upper()
    return sp_chain


def CommaChain(chain):
    return ", ".join(ChainStringToList(chain))


def NoOpChain(chain):
    return chain


def SpaceListChain(chain):
    return " ".join(ChainStringToList(chain))


def SemicolonChain(chain):
    return "; ".join(ChainStringToList(chain))


def ColonsChain(chain):
    return " :: ".join(ChainStringToList(chain))


def LinkTermList(chain):
    chain_list = ChainStringToList(chain)
    output_list = []
    for ii in range(len(chain_list) - 1):
        w1 = chain_list[ii].upper()
        w2 = chain_list[ii + 1].upper()
        linker = random.choice(LINKING_TERMS)
        output_list.append(linker.join((w1, w2)))
    return output_list


def LinkTermsChainSingleLine(chain):
    return "; ".join(LinkTermList(chain))


def LinkTermsChainMultiLine(chain):
    return "\n".join(LinkTermList(chain))


def LineBreakChain(chain):
    return "\n".join(ChainStringToList(chain))


def FormatTweet(chain, chain_distance):
    single_line_candidates = [
        CommaChain(chain),
        NoOpChain(chain),
        SemicolonChain(chain),
        SpaceListChain(chain),
        ColonsChain(chain),
        LinkTermsChainSingleLine(chain)
    ]
    single_line_candidates = [c for c in single_line_candidates if len(c) < 280]

    multi_line_candidates = [
        LineBreakChain(chain),
        LinkTermsChainMultiLine(chain)
    ]
    multi_line_candidates = [c for c in multi_line_candidates if len(c) < 280]

    if chain_distance < 6 and random.random() < 0.5:
        candidates = multi_line_candidates
    else:
        candidates = single_line_candidates

    if not candidates:
        return None

    return random.choice(candidates)


def IncrementPostCount(db_cursor, chain_id):
    db_cursor.execute(POST_COUNT_UPDATE_QUERY, (chain_id,))


if __name__ == "__main__":
    config_file = sys.argv[1]
    db_file = sys.argv[2]

    # TODO: Try out `with` context:
    db = sqlite3.connect(db_file)
    db_cur = db.cursor()
    chain_id, chain_distance, chain = FetchSpectrum(db_cur)
    print '\n', FormatTweet(chain, chain_distance), '\n'

    #IncrementPostCount(db_cur, chain_id)
    db.commit()
    db.close()
