import locale
import re
import warnings

try:
    from functools import lru_cache
except ImportError:
    from .backports.functools import lru_cache

try:
    from . import spell
except ImportError:
    spell = None
    warnings.warn("pyenchant is unavaiable", ImportWarning)


TRANS_RE_SUBS = {
    "en": [
        (re.compile(r"(?<!\w)'([\w\s,.'’]+?)'(?!\w)", re.U), r"‘\1’"),
        (re.compile(r"(\d)'", re.U), r"\1′"),
        (re.compile(r"'"), r"’"),
        (re.compile(r'"(\w)', re.U), r"“\1"),
        (re.compile(r'^(?<!“)([^“]+\b\d+([.,]\d+)?)"', re.U), r"\1″"),
        (re.compile(r'"'), r"”"),
        (re.compile("«[ \xa0]"), "«\u202f"),
        (re.compile("[ \xa0]»"), "\u202f»"),
        (re.compile(r"--"), r"—"),
        (re.compile(r"\.{3}"), r"…"),
        (re.compile(r"^[-–—]\s", re.U | re.M), "–\xa0"),
        (re.compile(r"([^\d\w-])-([^\d\w-])", re.U), r"\1–\2"),
        (re.compile(r"(\d|\b)EUR(\d|\b)", re.U), r"\1€\2"),
        (re.compile(r"(\d|\b)GBP(\d|\b)", re.U), r"\1£\2"),
        (re.compile(r"(\d|\b)JPY(\d|\b)", re.U), r"\1¥\2"),
    ],
    "fr": [
        (re.compile(r"(?<!\w)'([\w\s,.'’]+?)'(?!\w)", re.U), r"‘\1’"),
        (re.compile(r"(\d)'", re.U), r"\1′"),
        (re.compile(r"'"), r"’"),
        (re.compile(r'"(\w)', re.U), "«\u202f\\1"),
        (re.compile(r'^(?<!«)([^«]+\b\d+([.,]\d+)?)"', re.U), r"\1″"),
        (re.compile(r'"'), "\u202f»"),
        (re.compile("«[ \xa0]"), "«\u202f"),
        (re.compile("[ \xa0]»"), "\u202f»"),
        (re.compile(r"--"), r"—"),
        (re.compile(r"\.{3}"), r"…"),
        (re.compile(r"^[-–—]\s", re.U | re.M), "–\xa0"),
        (re.compile(r"([^\d\w-])-([^\d\w-])", re.U), r"\1–\2"),
        (re.compile("(\\d)[ \xa0](\\d{3})\\b", re.U), "\\1\u202f\\2"),
        (re.compile("[ \xa0]([!?:;])"), "\u202f\\1"),
        (re.compile(r"(\d|\b)EUR(\d|\b)", re.U), r"\1€\2"),
        (re.compile(r"(\d|\b)GBP(\d|\b)", re.U), r"\1£\2"),
        (re.compile(r"(\d|\b)JPY(\d|\b)", re.U), r"\1¥\2"),
        (re.compile(r"\b(n)[o0°]\s*(\d)", re.U | re.I), "\\1º\xa0\\2"),
        (re.compile(r"oe(u|il)"), r"œ\1"),
        (re.compile(r"O(e|E)(u|U|il|IL)"), r"Œ\2"),
    ],
}
FAILSAFE_LANGUAGE = "en"


def upgrade(text: str, language=None) -> str:
    """Try to undo a downgraded transliteration.
    """
    if language is None:
        language = locale.getdefaultlocale()[0]

    try:
        subs = TRANS_RE_SUBS[language]
    except KeyError:
        try:
            subs = TRANS_RE_SUBS[language.split("_")[0]]
        except KeyError:
            subs = TRANS_RE_SUBS[FAILSAFE_LANGUAGE]

    for pattern, repl in subs:
        text = pattern.sub(repl, text)

    return fix_spelling(text, language)


if spell:
    def fix_spelling(text: str, language=None) -> str:
        try:
            return get_dict(language).autofix(text)
        except spell.errors.DictNotFoundError:
            warnings.warn(
                "dictionary not found for language: {!r}".format(language))

    @lru_cache(5)
    def get_dict(language=None):
        return spell.Dict(language)

else:
    fix_spelling = lambda text, language=None: text


def decode_factory(encoding, language=None):
    def func(input, errors="strict"): #@ReservedAssignment
        buf = bytes(input)
        return upgrade(buf.decode(encoding, errors), language), len(buf)
    return func
