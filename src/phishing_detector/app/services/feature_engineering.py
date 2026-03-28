'''
📍 app/services/feature_engineering.py

This version:

extracts ALL URL-only features
handles edge cases (missing scheme, weird URLs)
returns a dict ready for your model
stays consistent with your trained feature columns
'''

import re
from urllib.parse import urlparse


# =========================
# HELPERS
# =========================

def get_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc


def is_ip(domain: str) -> int:
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return 1 if re.match(pattern, domain) else 0


def count_digits(url: str) -> int:
    return sum(c.isdigit() for c in url)


def count_letters(url: str) -> int:
    return sum(c.isalpha() for c in url)


def count_special_chars(url: str) -> int:
    return len(re.findall(r"[^\w]", url))


def count_subdomains(domain: str) -> int:
    return domain.count(".")


def has_obfuscation(url: str) -> int:
    # Basic detection: % encoding or hex patterns
    return 1 if "%" in url else 0


def count_obfuscated_chars(url: str) -> int:
    return url.count("%")


# =========================
# MAIN FEATURE FUNCTION
# =========================

def extract_features_from_url(url: str) -> dict:
    # Ensure URL has scheme
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    # Core counts
    url_length = len(url)
    domain_length = len(domain)

    num_digits = count_digits(url)
    num_letters = count_letters(url)
    num_special = count_special_chars(url)

    total_chars = max(url_length, 1)  # avoid division by zero

    # Ratios
    digit_ratio = num_digits / total_chars
    letter_ratio = num_letters / total_chars
    special_ratio = num_special / total_chars

    # Obfuscation
    obfuscated_count = count_obfuscated_chars(url)
    obfuscation_ratio = obfuscated_count / total_chars

    # HTTPS
    is_https = 1 if parsed.scheme == "https" else 0

    # Build feature dict (ORDER DOES NOT MATTER HERE)
    features = {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": is_ip(domain),
        "NoOfSubDomain": count_subdomains(domain),

        "NoOfLettersInURL": num_letters,
        "LetterRatioInURL": letter_ratio,

        "NoOfDegitsInURL": num_digits,
        "DegitRatioInURL": digit_ratio,

        "NoOfOtherSpecialCharsInURL": num_special,
        "SpacialCharRatioInURL": special_ratio,

        "HasObfuscation": has_obfuscation(url),
        "NoOfObfuscatedChar": obfuscated_count,
        "ObfuscationRatio": obfuscation_ratio,

        "IsHTTPS": is_https
    }

    return features