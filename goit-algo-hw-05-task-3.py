import timeit


def read_text(path):
    # Try plain UTF-8
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        pass

    # Try UTF-8 with BOM
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        pass

    # Try Windows-1251 (common for Cyrillic on Windows)
    try:
        with open(path, "r", encoding="cp1251") as f:
            return f.read()
    except UnicodeDecodeError:
        pass

    # Last resort: read bytes and decode best-effort
    with open(path, "rb") as f:
        data = f.read()
    for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            return data.decode(enc, errors="replace")
        except UnicodeDecodeError:
            continue
    # Fallback
    return data.decode("utf-8", errors="replace")


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return -1

    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp(text, pattern, prime=101):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return -1

    d = 256
    hpattern = 0
    htext = 0
    h = pow(d, m - 1, prime)

    for i in range(m):
        hpattern = (d * hpattern + ord(pattern[i])) % prime
        htext = (d * htext + ord(text[i])) % prime

    for i in range(n - m + 1):
        if hpattern == htext and text[i:i + m] == pattern:
            return i
        if i < n - m:
            htext = (d * (htext - ord(text[i]) * h) + ord(text[i + m])) % prime
            if htext < 0:
                htext += prime
    return -1


def boyer_moore(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return -1

    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    i = m - 1

    while i < n:
        j = m - 1
        k = i
        while j >= 0 and k >= 0 and text[k] == pattern[j]:
            k -= 1
            j -= 1
        if j == -1:
            return k + 1
        i += skip.get(text[i], m)
    return -1


def test_kmp(text, pattern):
    return kmp_search(text, pattern)


def test_rabin_karp(text, pattern):
    return rabin_karp(text, pattern)


def test_boyer_moore(text, pattern):
    return boyer_moore(text, pattern)


if __name__ == "__main__":
    text1 = read_text("text1.txt")
    text2 = read_text("text2.txt")

    # підрядки для тестування
    existing_substring = "розгорнутий список"
    non_existing_substring = "неіснуючий підрядок"

    # підрахунок часу
    for txt, name in [(text1, "стаття1"), (text2, "стаття2")]:
        print(f"\nТестування на {name}:")
        for pattern in [existing_substring, non_existing_substring]:
            print(f"\nПошук підрядка: '{pattern}'")

            kmp_time = timeit.timeit(lambda: test_kmp(txt, pattern), number=100)
            print(f"KMP час: {kmp_time:.6f} секунд")

            rabin_karp_time = timeit.timeit(lambda: test_rabin_karp(txt, pattern), number=100)
            print(f"Rabin-Karp час: {rabin_karp_time:.6f} секунд")

            boyer_moore_time = timeit.timeit(lambda: test_boyer_moore(txt, pattern), number=100)
            print(f"Boyer-Moore час: {boyer_moore_time:.6f} секунд")
