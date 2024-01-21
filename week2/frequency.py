#!/usr/bin/env python3

# Global variable (constant) for the text
TEXT = """Yes and No are not the only answers. In the intricate and sometimes perplexing realm of security, the straightforward ‘yes’ and ‘no’ answers we’re accustomed to may suddenly seem elusive. It’s a humorous take on the intricacies of security, where the right answer might be 'Well, it depends,' and navigating the security landscape feels a bit like solving a riddle. Welcome to the world where black and white answers are a rare find and shades of gray are supreme.

The majority of security breaches are caused by human error. Even though you send out reminder emails and try to teach everyone the cybersecurity safety practices, because humans are evolved to trust people, someone will always trust the wrong person causing a breach. It’s like trying to teach a goldfish to play fetch. So, while you keep fighting the good fight against digital chaos, you secretly wish that human error would take a vacation.

Todays tip: MFA enabled? Make sure you have it enabled and not someone else!! In a world where cyberattacks are the uninvited party crashers, MFA is the door policy we can all get behind even if it does involve a lot of training and begging to get people to use it.

Clicking on a phishing link is like taking a stroll through a cyberjungle and stumbling upon a sign that says, “Free treasure ahead!” It’s as if your computer suddenly transformed into an adventurous pirate ship, setting sail on the high seas of the internet. But here’s the catch: instead of buried treasure, you find yourself face-to-face with malware that’s more mischievous than a band of pirate monkeys raiding your digital coconuts."""

#function that will count all consonant given 

def count_vowels_and_consonants(text):
    """Count the number of vowels and consonants in the given text."""
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    text_lower = text.lower()

    vowel_count = sum(1 for char in text_lower if char in vowels)
    consonant_count = sum(1 for char in text_lower if char in consonants)

    return vowel_count, consonant_count

def main():
    """Print the number of vowels and consonants in the TEXT variable."""
    # Count vowels and consonants
    vowel_count, consonant_count = count_vowels_and_consonants(TEXT)

    # Print the results
    print(f"Number of vowels: {vowel_count}")
    print(f"Number of consonants: {consonant_count}")

if __name__ == "__main__":
    main()
