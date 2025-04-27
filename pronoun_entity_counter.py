def preprocess_input_file(file_path):
    """
    Pre-process the input conversation file to extract participant names and associate them with turns.
    Returns a list mapping turn numbers to participants and their sentences.
    """
    turn_data = []  # List to store (participant, sentence) for each turn

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Match lines with the format: "name (timestamp): message"
            match = re.match(r"^(?P<name>\w+)\s\(\d{1,2}:\d{2}:\d{2}\s?(AM|PM)?\):\s+(?P<text>.+)", line)
            if match:
                # Extract participant name and message text
                participant = match.group("name").lower()  # Convert name to lowercase for consistency
                message = match.group("text")

                # Append to turn data
                turn_data.append((participant, message))

    return turn_data


def analyze_conversation(turn_data, processed_output_file):
    """
    Analyzes the preprocessed conversation for pronoun usage.
    Computes total and average pronoun usage for each participant.
    """
    # Load the preprocessed Spacy-output file (tokens with POS info)
    with open(processed_output_file, "r", encoding="utf-8") as f:
        processed_lines = f.readlines()

    pronoun_counts = defaultdict(int)  # Cumulative pronoun counts for each participant
    sentence_counts = defaultdict(int)  # Sentence counts for each participant
    current_turn = 0

    for line in processed_lines:
        line = line.strip()

        # Detect a new turn
        if line.startswith("turn"):
            current_turn = int(line.split()[1]) - 1  # Extract the turn number, convert to 0-based index

        # Check for pronouns in tokens
        if "pos tag: PRON" in line:
            # Get the participant for the current turn
            if current_turn < len(turn_data):
                participant = turn_data[current_turn][0]  # Get participant's name
                pronoun_counts[participant] += 1

        # Count sentences for this participant
        if line.startswith("sentence:"):
            if current_turn < len(turn_data):
                participant = turn_data[current_turn][0]
                sentence_counts[participant] += 1

    # Calculate average pronouns per sentence
    results = {}
    for participant, total_pronouns in pronoun_counts.items():
        total_sentences = sentence_counts.get(participant, 1)  # Avoid division by zero
        avg_pronouns = total_pronouns / total_sentences
        results[participant] = {
            "total_pronouns": total_pronouns,
            "average_pronouns": avg_pronouns
        }

    return results

import re
from collections import defaultdict


def preprocess_input_file(file_path):
    """
    Pre-process the input conversation file to extract participant names and associate them with turns.
    Returns a list mapping turn numbers to participants and their sentences.
    """
    turn_data = []  # List to store (participant, sentence) for each turn

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Match lines with the format: "name (timestamp): message"
            match = re.match(r"^(?P<name>\w+)\s\(\d{1,2}:\d{2}:\d{2}\s?(AM|PM)?\):\s+(?P<text>.+)", line)
            if match:
                # Extract participant name and message text
                participant = match.group("name").lower()  # Convert name to lowercase for consistency
                message = match.group("text")

                # Append to turn data
                turn_data.append((participant, message))

    return turn_data


def analyze_conversation(turn_data, processed_output_file):
    """
    Analyzes the preprocessed conversation for pronoun usage.
    Computes total and average pronoun usage for each participant.
    """
    # Load the preprocessed SpaCy-output file (tokens with POS info)
    with open(processed_output_file, "r", encoding="utf-8") as f:
        processed_lines = f.readlines()

    pronoun_counts = defaultdict(int)  # Cumulative pronoun counts for each participant
    sentence_counts = defaultdict(int)  # Sentence counts for each participant
    current_turn = 0

    for line in processed_lines:
        line = line.strip()

        # Detect a new turn
        if line.startswith("turn"):
            current_turn = int(line.split()[1]) - 1  # Extract the turn number, convert to 0-based index

        # Check for pronouns in tokens
        if "pos tag: PRON" in line:
            # Get the participant for the current turn
            if current_turn < len(turn_data):
                participant = turn_data[current_turn][0]  # Get participant's name
                pronoun_counts[participant] += 1

        # Count sentences for this participant
        if line.startswith("sentence:"):
            if current_turn < len(turn_data):
                participant = turn_data[current_turn][0]
                sentence_counts[participant] += 1

    # Calculate average pronouns per sentence
    results = {}
    for participant, total_pronouns in pronoun_counts.items():
        total_sentences = sentence_counts.get(participant, 1)  # Avoid division by zero
        avg_pronouns = total_pronouns / total_sentences
        results[participant] = {
            "total_pronouns": total_pronouns,
            "average_pronouns": avg_pronouns
        }

    return results


def compare_gender_pronouns(pronoun_stats):
    """
    Takes pronoun statistics and two lists (male, female) of names and calculates:
    - Average pronoun usage for males
    - Average pronoun usage for females
    """
    male_names = ["luke", "ted", "david", "matthew", "jake", "rick", "josh", "tony", "aaron", "michael", "nick",
                  "george", "john", "vincent"]
    female_names = ["judith", "tia", "meg", "vicky", "eva", "julie", "rita", "leah", "caroline", "cintihia", "ariel",
                    "macy", "lynn", "rebecca", "cinthia", "shelly", "mara", "lisa", "amy", "michelle"]
    male_total_pronouns = 0
    male_sentence_count = 0
    female_total_pronouns = 0
    female_sentence_count = 0

    # Calculate total pronouns and sentence counts for each gender
    for name, stats in pronoun_stats.items():
        if name in male_names:
            male_total_pronouns += stats["total_pronouns"]
            male_sentence_count += stats["total_pronouns"] / stats["average_pronouns"]  # Derive total sentences
        elif name in female_names:
            female_total_pronouns += stats["total_pronouns"]
            female_sentence_count += stats["total_pronouns"] / stats["average_pronouns"]  # Derive total sentences

    # Calculate averages
    male_avg_pronouns = male_total_pronouns / male_sentence_count if male_sentence_count > 0 else 0
    female_avg_pronouns = female_total_pronouns / female_sentence_count if female_sentence_count > 0 else 0

    return round(male_avg_pronouns, 2), round(female_avg_pronouns, 2)


def main():
    # Input conversation file containing raw text with participants, timestamps, and sentences
    input_file = "2009_03_27.txt"  # Replace with your input file name

    # Pre-processed output from SpaCy that contains tokenized data
    processed_output_file = "2009_03_27.txt_output.txt"  # Replace with the tokenized output file

    # Step 1: Preprocess the conversation file to extract participants and their turns
    turn_data = preprocess_input_file(input_file)

    # Step 2: Analyze the conversation for pronoun usage
    pronoun_results = analyze_conversation(turn_data, processed_output_file)

    # Step 3: Display the results
    print("Pronoun Usage Analysis:")
    for participant, stats in pronoun_results.items():
        print(f"{participant.capitalize()}: Total Pronouns = {stats['total_pronouns']}, "
              f"Average Pronouns per Sentence = {stats['average_pronouns']:.2f}")

    # Step 5: Compare male and female pronoun usage
    male_avg, female_avg = compare_gender_pronouns(pronoun_results)

    # Step 6: Display the results
    print("\nPronoun Usage Analysis by Gender:")
    print(f"Male Average Pronouns per Sentence: {male_avg}")
    print(f"Female Average Pronouns per Sentence: {female_avg}")

if __name__ == "__main__":
    main()
