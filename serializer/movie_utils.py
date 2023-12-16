# movie_utils.py

import re

def extract_name(input_string):
    """
    Extracts the name from an input string.

    Args:
        input_string (str): Input string.

    Returns:
        str: Extracted name.
    """
    name = re.search(r'\b(.+?)\s+\(\d{4}\)', input_string)

    if name:
        extracted_text = name.group(1)
        return extracted_text

    return None


def extract_year(input_string):
    """
    Extracts the year from an input string.

    Args:
        input_string (str): Input string.

    Returns:
        str: Extracted year.
    """
    year = re.search(r'\((\d{4})\)', input_string)

    if year:
        extracted_year = year.group(1)
        return extracted_year

    return None

def extract_quality(input_string):
    """
    Extracts the quality from an input string.

    Args:
        input_string (str): Input string.

    Returns:
        str: Extracted quality.
    """
    match = re.search(r'(\d{3,4}p)', input_string)

    if match:
        extracted_quality = match.group(1)
        return extracted_quality

    return None


def extract_file_size(input_string):
    """
    Extracts the file size from an input string.

    Args:
        input_string (str): Input string.

    Returns:
        str: Extracted file size.
    """
    match = re.search(r'\d+(\.\d+)?(?:GB|MB|gb|mb)', input_string)

    if match:
        extracted_file_size = match.group(0)
        return extracted_file_size

    return None


def extract_mini_languages(input_string):
    """
    Extracts the languages from an input string.

    Args:
        input_string (str): Input string.

    Returns:
        list: List of extracted languages.
    """
    match = re.search(r'\[\s*([A-Za-z]+(?:\s*\+\s*[A-Za-z]+)*)\s*\]', input_string)
    languages_list = []

    if match:
        languages = match.group(1).split('+')
        languages_list.extend([lang.strip() for lang in languages])

    return languages_list


def extract_languages(movie_string):
    """
    Extracts the supported languages from a movie string.

    Args:
        movie_string (str): Movie string.

    Returns:
        list: List of supported languages.
    """
    indian_languages = {
        'Tamil': 'Tamil',
        'Hindi': 'Hindi',
        'Telugu': 'Telugu',
        'Marathi': 'Marathi',
        'Bengali': 'Bengali',
        'Malayalam': 'Malayalam',
        'Kannada': 'Kannada',
        'Punjabi': 'Punjabi',
        'Gujarati': 'Gujarati',
        'Odia': 'Odia'
    }

    matches = re.findall(r'\b(?:' + '|'.join(re.escape(lang) for lang in indian_languages.keys()) + r')\b', movie_string, flags=re.IGNORECASE)
    matched_languages = list(set(matches))

    return matched_languages

def determine_resolution(file_size):
    """
    Determines the resolution of a movie based on its file size.

    Args:
        file_size (str): File size as a string, e.g., '1.5GB'.

    Returns:
        str: Resolution of the movie ('480p', '720p', or '1080p').
    """
    match = re.search(r'(\d+(?:\.\d+)?)(GB|MB)', file_size, re.I)
    if match:
        size, unit = match.groups()
        size = float(size)

        # Convert size to GB if it's in MB
        if unit.lower() == 'mb':
            size /= 1024

        # Determine resolution based on size
        if size < 1:
            return '480p'
        elif size <= 2:
            return '720p'
        else:
            return '1080p'
    else:
        return 'Unknown'
