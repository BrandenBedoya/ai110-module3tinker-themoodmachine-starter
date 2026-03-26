"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # Gen-Z slang (positive meanings)
    "sick",       # "that was sick" = impressive
    "fire",       # "this beat is fire" = excellent
    "slaps",      # "this song slaps" = is great
    "bussin",     # "the food is bussin" = delicious/excellent
    "goated",     # "he's goated" = greatest of all time
    "vibing",     # "just vibing" = feeling good/relaxed
    "slay",       # "she slayed" = did really well
    "based",      # "that's based" = admirable
    "proud",      # "proud of myself"
    "hopeful",    # "feeling hopeful"
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # Gen-Z slang (negative meanings)
    "mid",        # "that was mid" = mediocre/disappointing
    "cringe",     # "that's cringe" = embarrassing
    "trash",      # "this is trash" = terrible
    "npc",        # sometimes used dismissively
    "exhausted",  # "totally exhausted"
    "anxious",    # "anxious about the presentation"
    "broke",      # "feeling broke" = depleted/empty
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "ugh this code is terrible but at least i'm learning something",
    "honestly just vibing no cap",
    "I absolutely love waiting in traffic for 2 hours",
    "this assignment lowkey slaps tho 🕺",
    "nah fr fr that was mid",
    "anxious about the presentation but ready to give it my all",
    "literally dying this is so funny 😂😂😂",
    "another day another dollar i guess",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "ugh this code is terrible but at least i'm learning something"
    "positive",  # "honestly just vibing no cap"
    "negative",  # "I absolutely love waiting in traffic for 2 hours" (sarcasm)
    "positive",  # "this assignment lowkey slaps tho 🕺" (slang: "slaps" = is good)
    "negative",  # "nah fr fr that was mid" (slang: "mid" = mediocre)
    "mixed",     # "anxious about the presentation but ready to give it my all"
    "positive",  # "literally dying this is so funny 😂😂😂" (exaggeration, laughter)
    "neutral",   # "another day another dollar i guess"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
print(len(SAMPLE_POSTS) == len(TRUE_LABELS))
