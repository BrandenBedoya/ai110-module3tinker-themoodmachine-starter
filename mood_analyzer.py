# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        import string
        import re
        
        # Strip whitespace and lowercase
        cleaned = text.strip().lower()
        
        # Extract and preserve emojis as separate tokens
        emoji_pattern = r'[😂🥲💀😍❤️🕺😭👌🔥😤😩😡😠😢😪:]'
        emojis = re.findall(emoji_pattern, cleaned)
        
        # Remove emojis from text first, then punctuation
        cleaned = re.sub(emoji_pattern, '', cleaned)
        
        # Map common emoticon text to emoji tokens
        cleaned = cleaned.replace(':)', 'smiley')
        cleaned = cleaned.replace(':(', 'frown')
        
        # Remove punctuation except apostrophes (for contractions)
        cleaned = cleaned.translate(str.maketrans('', '', string.punctuation.replace("'", '')))
        
        # Split into tokens
        tokens = cleaned.split()
        
        # Add emojis back as tokens
        tokens.extend(emojis)
        
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        score = 0
        
        # Simple negation handling: check if previous word is "not", "no", "never"
        negation_words = {"not", "no", "never", "ain't", "isnt"}
        
        for i, token in enumerate(tokens):
            # Check if previous token is a negation word
            is_negated = i > 0 and tokens[i - 1] in negation_words
            
            if token in self.positive_words:
                if is_negated:
                    score -= 1  # Reverse the polarity: "not good" is negative
                else:
                    score += 1
            
            elif token in self.negative_words:
                if is_negated:
                    score += 1  # Reverse the polarity: "not bad" is positive
                else:
                    score -= 1
            
            # Strong signals for emojis and slang
            elif token in ['😂', 'smiley', '🕺', '❤️', '😍']:
                score += 2  # Double weight for positive emojis
            elif token in ['frown', '😢', '😡', '😭', '😤', '😩', '😠']:
                score -= 2  # Double weight for negative emojis
            # 💀 is ambiguous: in Gen-Z context "I'm dead 💀" means something
            # is hilarious — treat it as mildly positive
            elif token == '💀':
                score += 1
        
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)
        
        # Map scores to labels with thresholds
        # Use a small threshold (1) so single words trigger predictions
        # Allow for "mixed" when score is close to zero
        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0
        
        negation_words = {"not", "no", "never", "ain't", "isnt"}
        
        for i, token in enumerate(tokens):
            is_negated = i > 0 and tokens[i - 1] in negation_words
            
            if token in self.positive_words:
                if is_negated:
                    negative_hits.append(f"not {token}")
                    score -= 1
                else:
                    positive_hits.append(token)
                    score += 1
            elif token in self.negative_words:
                if is_negated:
                    positive_hits.append(f"not {token}")
                    score += 1
                else:
                    negative_hits.append(token)
                    score -= 1
            elif token in ['😂', 'smiley', '🕺', '❤️', '😍']:
                positive_hits.append(f"emoji:{token}")
                score += 2
            elif token in ['frown', '😢', '😡', '😭', '😤', '😩', '😠']:
                negative_hits.append(f"emoji:{token}")
                score -= 2
            elif token == '💀':
                positive_hits.append(f"emoji:{token}(Gen-Z laugh)")
                score += 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
