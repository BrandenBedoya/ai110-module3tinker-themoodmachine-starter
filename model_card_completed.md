# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
I compared both the rule-based model and the machine learning model to understand their different strengths and weaknesses.

**Intended purpose:**  
Classify short text messages (social media posts, text messages) as expressing one of four moods: positive, negative, neutral, or mixed emotions.

**How it works (brief):**  
- **Rule-based version:** Scores text by counting positive/negative words, handling negation ("not happy" → negative), and boosting emoji signals. Final score maps to a mood label.
- **ML version:** Converts text to a "bag of words" (counts of each word) using CountVectorizer, then trains a LogisticRegression classifier on these word frequencies to learn mood patterns automatically.

---

## 2. Data

**Dataset description:**  
Started with 6 example posts and expanded to 14 total posts in `SAMPLE_POSTS` with matching labels in `TRUE_LABELS`. 

New posts I added (8 examples):
- "ugh this code is terrible but at least i'm learning something" → mixed
- "honestly just vibing no cap" → positive
- "I absolutely love waiting in traffic for 2 hours" → negative (sarcasm)
- "this assignment lowkey slaps tho 🕺" → positive
- "nah fr fr that was mid" → negative
- "anxious about the presentation but ready to give it my all" → mixed
- "literally dying this is so funny 😂😂😂" → positive
- "another day another dollar i guess" → neutral

**Labeling process:**  
I chose labels by asking: "What mood does a typical person reading this feel?" For mixed emotions, I labeled posts where the text clearly expressed conflicting feelings (e.g., tired but hopeful). Sarcasm was labeled by intent, not by the literal words used.

**Important characteristics of your dataset:**  
- Contains modern slang ("vibing", "no cap", "slaps", "mid", "fr fr")
- Includes emojis (😂, 🕺)
- Examples of sarcasm ("I absolutely love waiting in traffic")
- Posts expressing mixed/conflicting feelings
- Short, informal writing style (like social media)

**Possible issues with the dataset:**  
- **Very small:** 14 examples is tiny. Real ML systems need hundreds or thousands.
- **Imbalance:** 5 positive, 3 negative, 3 neutral, 3 mixed. Slightly skewed toward positive.
- **Ambiguity:** Posts like "This is fine" could be sarcastic depending on context.
- **Label subjectivity:** Different people might label sarcasm differently.
- **Limited language diversity:** All examples are in English, informal tone. No longer articles or formal writing.

---

## 3. How the Rule Based Model Works

**Your scoring rules:**  
1. **Preprocessing:** Lowercase text, remove punctuation, extract and preserve emojis as tokens
2. **Scoring logic:**
   - Start score at 0
   - For each word: +1 if in POSITIVE_WORDS, -1 if in NEGATIVE_WORDS
   - **Negation handling:** If word is preceded by "not"/"no"/"never", reverse its sign ("not happy" → -1 instead of +1)
   - **Emoji boost:** Positive emojis (😂, 🕺) worth +2, negative emojis (😢, 😡) worth -2
3. **Label mapping:**
   - score > 0 → "positive"
   - score < 0 → "negative"  
   - score == 0 → "neutral"

**Strengths of this approach:**
- ✅ **Interpretable:** Can explain exactly why it made each prediction
- ✅ **Fast:** No training needed; runs instantly
- ✅ **No data required:** Works without any labeled examples
- ✅ **Good for obvious cases:** "I love this" and "this is terrible" classified correctly
- ✅ **Handles negation:** "I am not happy" correctly reverses to negative

**Weaknesses of this approach:**
- ❌ **Can't detect sarcasm:** "I absolutely love waiting in traffic" → mistakenly positive (sees "love")
- ❌ **Unknown words:** "vibing", "slaps", "mid" not in word lists → treated as neutral
- ❌ **Loses nuance:** "tired but hopeful" saw only "tired" and returned negative (ignores hope)
- ❌ **Simple math:** Can't learn that certain words appear together in mood patterns
- ❌ **Brittleness:** Adding one sarcastic post breaks the system; need to manually add special rules

Final accuracy: **57% (8/14 correct)**

---

## 4. How the ML Model Works

**Features used:**  
Bag-of-words representation using `CountVectorizer` from scikit-learn. Each post becomes a vector where each position represents a word's frequency in that post. For example, "I love this" → [1, 1, 1, 0, 0, ...] depending on how many unique words are in the training set.

**Training data:**  
The model trained on `SAMPLE_POSTS` and `TRUE_LABELS` (all 14 labeled posts). Used `LogisticRegression` with max_iter=1000 to learn how word frequencies correlate with each mood.

**Training behavior:**  
- Accuracy jumped from 57% (rule-based) to 100% (ML model) simply by learning the patterns in the data
- The model learned that words like "vibing" and "slaps" predict positive moods
- It learned "mid" predicts negative mood
- It learned combinations: "love" + "traffic" together → sarcasm → negative

**Strengths and weaknesses:**

**Strengths:**
- ✅ **100% training accuracy:** Learned all 14 patterns perfectly
- ✅ **Automatic pattern learning:** No need to manually list words or write rules
- ✅ **Handles sarcasm indirectly:** Learned "love" near "traffic" → negative (an implicit sarcasm signal)
- ✅ **Learns slang:** Automatically recognized "vibing", "slaps", "mid" as mood indicators
- ✅ **Captures mixed emotions:** Learned to predict "mixed" when posts contain conflicting signals

**Weaknesses:**
- ❌ **Overfitting likely:** 100% on 14 training examples probably doesn't generalize to new posts
- ❌ **Tiny dataset:** With only 14 examples, the model memorizes rather than learns real patterns
- ❌ **Black box:** Can't explain *why* it made a decision (unlike rules)
- ❌ **Needs labels:** Requires you to label examples; rule-based works without any
- ❌ **Not production-ready:** Would need hundreds of labeled examples to be reliable

---

## 5. Evaluation

**How you evaluated the model:**  
Both models were evaluated on `SAMPLE_POSTS` (the same data used to build/train them). This measures "training accuracy"—how well each system recognizes examples it has already seen.

**Rule-based evaluation:** 8/14 correct = 57% accuracy
**ML evaluation:** 14/14 correct = 100% accuracy

**Examples of correct predictions:**

*Rule-based model got right:*
1. "I love this class so much" → positive ✅ (found "love")
2. "I am not happy about this" → negative ✅ (negation handled correctly)
3. "literally dying this is so funny 😂" → positive ✅ (emojis boosted score to +6)

*ML model got right (including hard ones rule-based missed):*
1. "honestly just vibing no cap" → positive ✅ (learned "vibing" predicts positive)
2. "I absolutely love waiting in traffic for 2 hours" → negative ✅ (context: "traffic" overrode "love")
3. "anxious about the presentation but ready to give it my all" → mixed ✅ (learned this pattern)

**Examples of incorrect predictions (rule-based only):**

1. **"I absolutely love waiting in traffic"** → predicted positive, true negative
   - Why it failed: Only saw "love" (+1), didn't understand sarcasm
   - ML got it right: Learned "love" near "traffic" signals sarcasm

2. **"honestly just vibing no cap"** → predicted neutral, true positive
   - Why it failed: "vibing" not in POSITIVE_WORDS; "cap" removed as punctuation
   - ML got it right: Learned "vibing" and "cap" appear in positive posts

3. **"nah fr fr that was mid"** → predicted neutral, true negative
   - Why it failed: "mid" (slang for mediocre) not recognized; "fr fr" parsed as noise
   - ML got it right: Learned "mid" is a negative word in this context

---

## 6. Limitations

1. **Tiny dataset:** 14 posts is far too small for reliable learning. ML model likely memorized rather than learned transferable patterns.

2. **Training vs. real performance:** Both models show 100% and 57% on training data, but would likely perform much worse on **new, unseen posts** from different writers.

3. **Sarcasm remains hard:** Even the ML model might fail on new sarcasm it hasn't seen. Needs explicit sarcasm examples in training.

4. **Language-specific:** All posts are informal English. Wouldn't work for emojis in other languages, formal writing, or non-English text.

5. **No context:** Without conversation history, it can't distinguish between "this is fine" as neutral vs. sarcastic.

6. **Missing data types:** Model hasn't seen longer posts, quotes, links, or metadata that might affect mood.

7. **The rule-based model is brittle:** Adding one rule affects everything. "Not good" works but "not that good" would fail (gap too wide).

---

## 7. Ethical Considerations

**Potential harms:**

1. **Mental health misuse:** Using mood detection to monitor someone without consent (e.g., flagging "sad" posts for intervention without asking) violates privacy.

2. **Misclassifying distress:** Sarcasm like "I'm doing great" might be missed, especially if someone is actually struggling.

3. **Cultural bias:** Slang, emojis, and humor vary by community. Model trained only on one style might misjudge others. Example: 😐 might mean different things in different contexts.

4. **Amplification:** If used in hiring/moderation, could systematically disadvantage groups whose speech patterns weren't in training data.

5. **Over-reliance:** Treating a 57% or even 100% classifier as truth for high-stakes decisions (content moderation, therapy recommendations) is dangerous.

**Why this matters:**  
Even simple classifiers encode assumptions. This model assumes mood is always determinable from text alone, that slang means the same thing to everyone, and that 14 examples are enough to generalize. In real applications, these could harm users.

---

## 8. Ideas for Improvement

**For the rule-based model:**
- Add more words to POSITIVE_WORDS and NEGATIVE_WORDS (especially slang: "vibing", "slaps", modern emojis)
- Improve negation: detect "not...good" even with words between them
- Add sarcasm detection rules (if post mentions something bad after "love"/"great", flip it)
- Context window: look at multi-word phrases, not just individual words
- Sentiment intensifiers: "very happy" should score higher than "happy"

**For the ML model:**
- **Get more data:** Add 50-100 more labeled posts covering different styles, languages, sarcasm types
- **Test on new data:** Create a separate test set to measure real generalization (not just training accuracy)
- **Use TF-IDF:** `TfidfVectorizer` instead of `CountVectorizer` to weight important words better
- **Longer sequences:** Use n-grams (pairs/triplets of words) to capture phrases like "love + traffic"
- **Better features:** Add emoji embeddings, or use pre-trained word embeddings (Word2Vec, GloVe)
- **Ensemble methods:** Train multiple models and combine predictions  
- **Neural networks:** Use a small transformer or LSTM that can learn word order and context

**General improvements:**
- **Balanced dataset:** Ensure equal numbers of positive/negative/neutral/mixed examples
- **Explicit sarcasm labels:** Mark which posts are sarcastic so model can learn the pattern
- **Separate test set:** Reserve 20-30% of data for evaluation (don't train on it)
- **Baseline comparison:** Start with a random classifier or majority-class baseline
- **Cross-validation:** Use k-fold cross-validation to estimate real performance
- **Domain expertise:** Collaborate with linguists or domain experts in mood/sentiment analysis
