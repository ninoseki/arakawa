from functools import partial

from pydantic import Field

TypeAliasedField = partial(Field, alias="_type")
