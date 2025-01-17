import html
import math
import random
import re
import urllib
from datetime import datetime
from numbers import Number
from typing import List, Pattern


def areValidBools(l: List[bool]) -> bool:
    if not hasItems(l):
        return False

    for b in l:
        if not isValidBool(b):
            return False

    return True

def areValidStrs(l: List[str]) -> bool:
    if not hasItems(l):
        return False

    for s in l:
        if not isValidStr(s):
            return False

    return True

def cleanStr(s: str, replacement: str = ' ', htmlUnescape: bool = False) -> str:
    if replacement is None:
        raise ValueError(f'replacement argument is malformed: \"{replacement}\"')
    elif not isValidBool(htmlUnescape):
        raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

    if s is None:
        return ''

    s = s.replace('\r\n', replacement)\
            .replace('\r', replacement)\
            .replace('\n', replacement)\
            .strip()

    if htmlUnescape:
        s = html.unescape(s)

    return s

def formatTime(time) -> str:
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')

    return time.strftime("%A, %b %d, %Y %I:%M%p")

def formatTimeShort(time, includeSeconds: bool = False) -> str:
    if time is None:
        raise ValueError(f'time argument is malformed: \"{time}\"')
    elif not isValidBool(includeSeconds):
        raise ValueError(f'includeSeconds argument is malformed: \"{includeSeconds}\"')

    if includeSeconds:
        return time.strftime("%b %d %I:%M:%S%p")
    else:
        return time.strftime("%b %d %I:%M%p")

def getBoolFromDict(d: dict, key: str, fallback: bool = None) -> bool:
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif isValidBool(fallback):
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, bool):
        if isinstance(value, Number):
            value = value != 0
        elif isinstance(value, str):
            value = strToBool(value)
        else:
            raise RuntimeError(f'encountered unknown type that can\'t be converted to bool: \"{value}\"')

    return value

def getCleanedSplits(s: str) -> List[str]:
    splits: List[str] = list()

    if not isValidStr(s):
        return splits

    words = s.split()

    if splits is None or len(splits) == 0:
        return words

    for split in splits:
        split = cleanStr(split)

        if isValidStr(split):
            words.append(split)

    return words

def getDateTimeFromStr(text: str) -> datetime:
    if isValidStr(text):
        return datetime.fromisoformat(text)
    else:
        return None

def getDefaultTimeout() -> int:
    return 10 # seconds

def getFloatFromDict(d: dict, key: str, fallback: float = None) -> float:
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif isValidNum(fallback):
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, float):
        value = float(value)

    if not isValidNum(value):
        raise ValueError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getIntFromDict(d: dict, key: str, fallback: int = None) -> int:
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif isValidNum(fallback):
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, int):
        value = int(value)

    if not isValidNum(value):
        raise ValueError(f'value \"{value}\" for key \"{key}\" is malformed in d: \"{d}\"')

    return value

def getNowTimeText(includeSeconds: bool = False) -> str:
    if not isValidBool(includeSeconds):
        raise ValueError(f'includeSeconds argument is malformed: \"{includeSeconds}\"')

    return formatTimeShort(
        time = datetime.now(),
        includeSeconds = includeSeconds
    )

def getRandomSpaceEmoji() -> str:
    spaceEmoji = [ '🚀', '👾', '☄️', '🌌', '👨‍🚀', '👩‍🚀', '👽', '🌠' ]
    randomIndex = random.randint(0, len(spaceEmoji) - 1)
    return spaceEmoji[randomIndex]

def getStrFromDateTime(dt: datetime) -> str:
    if dt is None:
        return None
    else:
        return dt.isoformat()

def getStrFromDict(d: dict, key: str, fallback: str = None, clean: bool = False, htmlUnescape: bool = False) -> str:
    if d is None:
        raise ValueError(f'd argument is malformed: \"{d}\"')
    elif not isValidStr(key):
        raise ValueError(f'key argument is malformed: \"{key}\"')
    elif not isValidBool(clean):
        raise ValueError(f'clean argument is malformed: \"{clean}\"')
    elif not isValidBool(htmlUnescape):
        raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

    value = None

    if key in d and d[key] is not None:
        value = d[key]
    elif fallback is not None:
        value = fallback
    else:
        raise KeyError(f'there is no fallback and key \"{key}\" doesn\'t exist in d: \"{d}\"')

    if not isinstance(value, str):
        value = str(value)

    if clean:
        value = cleanStr(value, htmlUnescape = htmlUnescape)

    return value

def hasItems(l: List) -> bool:
    return l is not None and len(l) >= 1

def isValidBool(b: bool) -> bool:
    return b is not None and isinstance(b, bool)

def isValidNum(n: Number) -> bool:
    return n is not None and isinstance(n, Number) and math.isfinite(n)

def isValidStr(s: str) -> bool:
    return s is not None and isinstance(s, str) and len(s) >= 1 and not s.isspace()

def isValidUrl(s: str) -> bool:
    if not isValidStr(s):
        return False

    parsed = urllib.parse.urlparse(s)
    url = parsed.geturl()

    return isValidStr(url)

def removePreceedingAt(s: str) -> str:
    if not isValidStr(s):
        return s
    elif s[0] != '@':
        return s
    else:
        return s[1:len(s)]

trueRegEx: Pattern = re.compile(r"t(rue)?|y(es)?", re.IGNORECASE)
falseRegEx: Pattern = re.compile(r"f(alse)?|n(o)?", re.IGNORECASE)

def strToBool(s: str) -> bool:
    if not isValidStr(s):
        raise ValueError(f's argument is malformed: \"{s}\"')

    return falseRegEx.match(s) is None
