"""Tokenizer turning PDDL source text into nested lists of tokens.

PDDL is an s-expression language, so we lex into parentheses-delimited nested
lists of atoms (strings). Line comments start with ``;``. Case is insensitive
in PDDL, so all tokens are lower-cased.
"""

from __future__ import annotations

from .ast import PDDLError


def _strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        idx = line.find(";")
        out.append(line if idx == -1 else line[:idx])
    return "\n".join(out)


def tokenize(text: str) -> list:
    """Parse PDDL source into a nested list of lower-cased string tokens."""
    text = _strip_comments(text)
    # Pad parens so a simple split yields clean tokens.
    text = text.replace("(", " ( ").replace(")", " ) ")
    tokens = text.split()

    stack: list[list] = [[]]
    for tok in tokens:
        if tok == "(":
            new: list = []
            stack[-1].append(new)
            stack.append(new)
        elif tok == ")":
            if len(stack) == 1:
                raise PDDLError("Unbalanced parentheses: unexpected ')'")
            stack.pop()
        else:
            stack[-1].append(tok.lower())

    if len(stack) != 1:
        raise PDDLError("Unbalanced parentheses: missing ')'")
    top = stack[0]
    if len(top) != 1 or not isinstance(top[0], list):
        raise PDDLError("Expected a single top-level s-expression")
    return top[0]
