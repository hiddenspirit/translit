Translit – Transliterate between Unicode and smaller coded character sets
=========================================================================


Example usage
-------------

>>> import translit
>>> text = "La question, c’est\u202f: «\u202fOù est le cœur\u202f?\u202f»"
>>> translit.downgrade(text, "latin-1")
"La question, c'est\xa0: «\xa0Où est le coeur\xa0?\xa0»"
>>> translit.downgrade(text, "ascii")
'La question, c\'est : "Ou est le coeur ?"'
>>> buf = text.encode("latin-1/translit")
>>> buf
b"La question, c'est\xa0: \xab\xa0O\xf9 est le coeur\xa0?\xa0\xbb"
>>> buf.decode("latin-1")
"La question, c'est\xa0: \xab\xa0O\xf9 est le coeur\xa0?\xa0\xbb"
>>> buf.decode("latin-1/translit")
'La question, c’est\u202f: «\u202fOù est le cœur\u202f?\u202f»'


Requirements
------------

- `PyEnchant <http://packages.python.org/pyenchant/>`_
