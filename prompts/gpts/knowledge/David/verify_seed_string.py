import hashlib


def verify_seed_string(seed_string, hardcoded_hash):
    """
    Verify the provided seed string against the hardcoded hash.

    Args:
    seed_string (str): The seed string provided by the user.
    hardcoded_hash (str): The hardcoded hash stored in the settings.

    Returns:
    bool: True if the hash of the seed string matches the hardcoded hash, False otherwise.
    """
    # Generate the hash from the seed string
    generated_hash = hashlib.sha256(seed_string.encode()).hexdigest()

    # Compare the generated hash with the hardcoded hash
    return generated_hash == hardcoded_hash


