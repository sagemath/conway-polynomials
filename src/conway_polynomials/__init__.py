r"""
Python interface to Frank Lübeck's Conway polynomial database

First, call ``database()`` to load the database into a python
dictionary, and then look up the coefficients of your polynomial using
two keys ``p`` (your prime) and ``n`` (your degree). The following
results for ``p=2`` can be found at,

  https://www.math.rwth-aachen.de/~Frank.Luebeck/data/ConwayPol/CP2.html

::

>>> import conway_polynomials
>>> cpdb = conway_polynomials.database()

>>> p = 2; n = 5
>>> cpdb[p][n]
[1, 0, 1, 0, 0, 1]

>>> p = 2; n = 17
>>> cpdb[p][17]
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

"""


def _parse_line(l):
    r"""
    Parse a single line (not the first or the last) from Frank
    Lübeck's data file into a triplet (p, n, coeffs), where ``p`` and
    ``n`` are python integers and ``coeffs`` is a list of
    them. According to Frank's webpage, each line has the form,

      [p, n, [a0, a1, ..., 1]],

    but in reality there are no spaces in the data.
    """
    # Remove all of the brackets, the trailing comma, and the trailing
    # newline to obtain "p, n, a0, a1, ..., 1".
    l = l.replace("[","")[:-4]

    # Now we know that p and n are the first two (CSV) fields, and
    # that the coefficients are whatever's left.
    fields = l.split(",")

    # Convert everything to integers before returning.
    p = int(fields[0])
    n = int(fields[1])
    coeffs = [int(c) for c in fields[2:]]

    return (p, n, coeffs)


_conway_dict = None  # cached result of database()
def database():
    r"""
    Load (if necessary) and return a python dictionary of Conway
    polynomial coefficients.

    The returned dictionary is of the form ``{p => {n => coeffs}}``,
    where ``p`` is a prime, ``n`` is a degree, and ``coeffs`` is a
    list of coefficients. The coefficients are listed in "ascending"
    order, i.e. they are indexed by the degree of the monomial they
    sit in front of.

    The result is cached.
    """
    global _conway_dict

    if _conway_dict is not None:
        return _conway_dict

    _conway_dict = {}
    from importlib.resources import files
    dbpath = files('conway_polynomials').joinpath('CPimport.txt')
    with open(dbpath, "rt") as f:
        # The first line of the file is "allConwayPolynomials := ["
        f.readline()

        for line in f:
            if line[0] == "0":
                # This is the last line in the file; otherwise it would
                # start with a square bracket.
                break

            (p, n, coeffs) = _parse_line(line)
            if p not in _conway_dict:
                _conway_dict[p] = {}

            _conway_dict[p][n] = coeffs

    return _conway_dict


if __name__ == "__main__":
    import doctest
    doctest.testmod()
