import requests
import sys
import utils

def get_text(text_url):
    req = requests.get(text_url)
    assert req.status_code == 200
    text = req.text.replace("/n", "")

    return text

def split_text(text, n_proc):
    factor_offset = len(text) // n_proc
    offset = len(text) % n_proc
    texts = [text[i:i+factor_offset+(1 if j < offset else 0)] \
                            for j, i in enumerate(range(0, len(text), factor_offset+1))]
    
    return texts
     

def main(DEFAULT_PROC=None):
    text_url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
    n_proc = DEFAULT_PROC

    text = get_text(text_url)
    texts = split_text(text, n_proc)
    utils.serialize(texts, "./sent_texts")
    
    # Only for debbuging reasons.
    utils.serialize(texts, "./debugging")