def trim_pkcs7_padding(block):
    i = len(block) - 1
    j = i
    last_char = block[-1]
    while j >= 0 and block[j] == last_char:
        j -= 1

    return block[:-(i - j)]
