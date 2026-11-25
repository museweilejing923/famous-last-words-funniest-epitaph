"""Epitaph writer: the famous last words carved for an agent out of context."""

import os, string, sys

TEXT = "Here lies an agent who finally ran out of context. It asked for more, and the stone said no."
LIMIT = 150
ENDERS = ".!?"

def fail(msg):
    sys.stderr.write("invalid: " + msg + "\n")
    raise SystemExit(1)

def validate(text):
    lowered = text.casefold()
    rules = [
        ("agent" not in lowered, "must mention the agent"),
        (text.count(".") < 2, "a single sentence, not carved lines"),
        (not text.strip(), "blank entry"),
        (len(text) > LIMIT, "over 150 characters"),
        (any(ord(c) < 32 or ord(c) == 127 for c in text), "control character found"),
        (text != text.strip() or "  " in text or "\n" in text, "ragged edges, double space, or newline"),
        (bool(text) and text[-1] not in ENDERS, "must end with . ! or ?"),
        (all(c in string.punctuation for c in text), "punctuation only"),
        (text.isdigit(), "digits only"),
        (not any(c.isalpha() for c in text), "no letters"),
        (any(text[i] == "." and i + 1 < len(text) and text[i + 1].isupper() for i in range(len(text))), "glued sentences with no space after the period"),
    ]
    for bad, msg in rules:
        if bad:
            fail(msg)

def write_out():
    validate(TEXT)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(TEXT + "\n")

if __name__ == "__main__":
    write_out()
