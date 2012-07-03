translit – Transliterate between Unicode and smaller coded character sets
=========================================================================


Example usage
-------------

>>> import translit
>>> text = "La question, c’est\u202f: «\u202fOù est le cœur\u202f?\u202f»"

Downgrade text to Latin-1:

>>> translit.downgrade(text, "latin-1")
"La question, c'est\xa0: «\xa0Où est le coeur\xa0?\xa0»"

Downgrade text to ASCII:

>>> translit.downgrade(text, "ascii")
'La question, c\'est : "Ou est le coeur ?"'

Downgrade and encode to Latin-1:

>>> buf = text.encode("latin-1/translit")
>>> buf
b"La question, c'est\xa0: \xab\xa0O\xf9 est le coeur\xa0?\xa0\xbb"

Decoding, the normal way:

>>> buf.decode("latin-1")
"La question, c'est\xa0: «\xa0Où est le coeur\xa0?\xa0»"

Decoding, the upgraded way:

>>> buf.decode("latin-1/translit/fr")
'La question, c’est\u202f: «\u202fOù est le cœur\u202f?\u202f»'


Installation
------------

You can use the setup script::

  $ ./setup.py install

On Windows, you can use one of the MSI binary packages provided
on the `download page
<https://bitbucket.org/spirit/translit/downloads>`_.


Requirements
------------

- `Python 3.2+ <http://www.python.org>`_
  (or 2.7, using `lib3to2 <https://bitbucket.org/amentajo/lib3to2>`_)
- `PyEnchant <http://packages.python.org/pyenchant>`_
