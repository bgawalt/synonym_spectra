"""Query the database and post a spectrum to the account.

$ python post_spectrum.py spectra.config spectra.db
"""


import random
import sqlite3
import sys
import tweepy


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
    if random.random() < 0.5:
        print 'reversed!'
        sp_chain = sp_chain[::-1]
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


def LinkTermList(chain, upper_words=True):
    chain_list = ChainStringToList(chain)
    output_list = []
    for ii in range(len(chain_list) - 1):
        w1 = chain_list[ii]
        if ii == 0 or upper_words:
            w1 = w1.upper()
        w2 = chain_list[ii + 1]
        if (ii == (len(chain_list) - 1)) or upper_words:
            w2 = w2.upper()
        linker = random.choice(LINKING_TERMS)
        output_list.append(linker.join((w1, w2)))
    return output_list


def LinkTermsChainSingleLine(chain, upper_words=True):
    tweet = "; ".join(LinkTermList(chain, upper_words=upper_words))
    if random.random() < -10.5:
        return tweet
    spchain = ChainStringToList(chain)
    tweet = tweet + "\n\n" + spchain[0].upper() + " = " + spchain[-1].upper()
    return tweet


def LinkTermsChainMultiLine(chain, upper_words=True):
    tweet = "\n".join(LinkTermList(chain, upper_words=upper_words))
    if random.random() < -10.5:
        return tweet
    spchain = ChainStringToList(chain)
    tweet = tweet + "\n\n" + spchain[0].upper() + " = " + spchain[-1].upper()
    return tweet


def LineBreakChain(chain):
    return "\n".join(ChainStringToList(chain))


def FormatTweet(chain, chain_distance):
    up_words = random.random() < 0.5
    single_line_candidates = [
        CommaChain(chain),
        NoOpChain(chain),
        SemicolonChain(chain),
        SpaceListChain(chain),
        ColonsChain(chain),
        LinkTermsChainSingleLine(chain, upper_words=up_words)
    ]
    single_line_candidates = [c for c in single_line_candidates if len(c) < 280]

    multi_line_candidates = [
        LineBreakChain(chain),
        LinkTermsChainMultiLine(chain, upper_words=up_words)
    ]
    multi_line_candidates = [c for c in multi_line_candidates if len(c) < 280]

    if chain_distance < 6 and random.random() < 0.5:
        candidates = multi_line_candidates
    else:
        candidates = single_line_candidates

    if not candidates:
        return None

    return random.choice(candidates)


def GetTweepyConfig(config_filename):
    """Returns dictionary with auth details for building a Tweepy API object."""
    with open(config_filename, "r") as infile:
        config = {}
        for line in infile:
            spline = line.split(" = ")
            config[spline[0]] = spline[1].strip()
    return config


def GetTweepyAuth(config_file):
    config = GetTweepyConfig(config_file)
    ckey = config["CONSUMER_KEY"]
    csec = config["CONSUMER_SECRET"]
    akey = config["ACCESS_KEY"]
    asec = config["ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(ckey, csec)
    auth.set_access_token(akey, asec)
    return auth


def TweetChain(chain, tweepy_config_filename):
    auth = GetTweepyAuth(tweepy_config_filename)
    api = tweepy.API(auth)
    status = api.update_status(status=chain)
    return status.id_str


def IncrementPostCount(db_cursor, chain_id):
    db_cursor.execute(POST_COUNT_UPDATE_QUERY, (chain_id,))


if __name__ == "__main__":
    config_file = sys.argv[1]
    db_file = sys.argv[2]

    # TODO: Try out `with` context:
    db = sqlite3.connect(db_file)
    db_cur = db.cursor()
    chain_id, chain_distance, chain = FetchSpectrum(db_cur)

    tweet = None
    count = 10
    while tweet is None:
        count -= 1
        if count == 0:
            raise ValueError("Couldn't make a tweeet!")
        tweet = FormatTweet(chain, chain_distance)
        print tweet
    print TweetChain(tweet, config_file)
    IncrementPostCount(db_cur, chain_id)
    db.commit()
    db.close()
