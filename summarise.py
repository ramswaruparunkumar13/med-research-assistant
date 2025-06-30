from transformers import BartForConditionalGeneration, BartTokenizer

# Load the tokenizer and model from Hugging Face's Transformers library
# BART is a sequence-to-sequence model suitable for text summarization
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def generate_summary(text, max_length=130, min_length=30):
    """Summarizes input text using BART with prompt engineering."""

    # Add a guiding prompt to steer the summary towards clinical relevance
    prompt = (
        "Summarize this medical research abstract for a clinician. "
        "Include key findings, methodology, population size, and clinical relevance.\n\n"
    )
    input_text = prompt + text

    # Tokenize the input text into model-readable format
    # Truncation ensures input fits within BART's 1024-token limit
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate the summary using beam search
    # length_penalty > 1 discourages overly long summaries
    # num_beams defines how many paths to consider during generation (tradeoff between quality and performance)
    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decode the generated token IDs back to human-readable text
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


