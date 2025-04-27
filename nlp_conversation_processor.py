import re
import spacy

# Load SpaCy's transformer-based English NLP pipeline
# This model needs to be installed: python -m spacy download en_core_web_trf
nlp = spacy.load("en_core_web_trf")


def clean_turn_text(turn):
    """
    Remove everything (e.g., speaker and timestamp) before the dialogue message in a turn.
    """
    match = re.match(r"^[^\(]*\(\d{1,2}:\d{2}:\d{2}\s?(AM|PM)?\):\s", turn)
    if match:
        return turn[match.end():].strip()  # Remove speaker/timestamp
    return turn.strip()


def process_conversation(conversation_text, output_file):
    """
    Process the line-separated conversation text and write results to the specified output file.
    """
    with open(output_file, "w", encoding="utf-8") as out_f:
        # Split conversation into lines (each line represents a message/turn)
        lines = conversation_text.strip().split("\n")

        # Process each line as a turn
        for turn_num, line in enumerate(lines, start=1):
            # Clean the line by removing metadata (speaker and timestamp)
            cleaned_turn = clean_turn_text(line)

            # Process the cleaned turn with SpaCy's transformer-based NLP pipeline
            doc = nlp(cleaned_turn)

            # Write the turn number
            out_f.write(f"turn {turn_num}\n")

            # List to store identified named entities in the current turn
            turn_named_entities = []

            # Process each sentence in the current turn
            for sent in doc.sents:
                out_f.write(f"\tsentence: {sent.text.strip()}\n")

                # Write each token in this sentence
                for token in sent:
                    # Skip invalid tokens (spaces, empty tokens)
                    if token.is_space or token.text.strip() == "":
                        continue
                    out_f.write(f"\t\ttoken: {token.text} pos tag: {token.pos_} lemma: {token.lemma_}\n")

                # Detect entities using SpaCy's Named Entity Recognizer (Transformer-based)
                for ent in doc.ents:
                    # Append each entity as a tuple (entity_text, entity_label)
                    turn_named_entities.append((ent.text, ent.label_))

            # Write all named entities at the end of the current turn
            if turn_named_entities:
                out_f.write("\t\tnamed entities: " + ", ".join(
                    f"{entity} type: {label}" for entity, label in turn_named_entities) + "\n")

            # Add a blank line to separate turns
            out_f.write("\n")


if __name__ == "__main__":
    # List of input conversation text files
    input_files = ["2009_03_27.txt", "2009_03_29.txt"]

    # Process each file and generate corresponding output
    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as in_f:
            conversation_text = in_f.read()

        # Generate the output file name
        output_file = f"{input_file}_output.txt"
        process_conversation(conversation_text, output_file)
