import os
from nlp_conversation_processor import process_conversation
from pronoun_entity_counter import preprocess_input_file, analyze_conversation, compare_gender_pronouns

def main():
    """
    Main function to execute the conversation processor and
    pronoun analyzer, creating output files in the OutputFiles directory.
    """
    # Get input file from the user
    input_file = input("Enter the input file name (e.g., conversation.txt): ").strip()

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    # Create OutputFiles directory if it doesn't already exist
    output_dir = "OutputFiles"
    os.makedirs(output_dir, exist_ok=True)

    # STEP 1: Process the file with NLP processor
    input_filename = os.path.basename(input_file)  # Extract filename from path
    tokenized_output_file = os.path.join(output_dir, f"output_tokenized_{input_filename}")

    print("\nStep 1: Running NLP Conversation Processor...")
    # Tokenize and process input file (NLP task)
    inputFile_text = open(input_file, "r", encoding="utf-8").read()
    process_conversation(inputFile_text, tokenized_output_file)  # NLP processing logic

    print(f"Intermediate tokenized file created: {tokenized_output_file}")

    # STEP 2: Count and analyze pronouns associated with entities
    pronoun_analysis_file = os.path.join(output_dir, f"pronoun_analysis_{input_filename}")

    print("\nStep 2: Running Pronoun Entity Counter...")
    preprocessedInput = preprocess_input_file(input_file)
    gender_analysis_results = analyze_conversation(preprocessedInput,tokenized_output_file)  # Analyze entities and pronouns

    maleAverage, femaleAverage = compare_gender_pronouns(gender_analysis_results)

    # Save the pronoun analysis results to a file
    with open(pronoun_analysis_file, "w", encoding="utf-8") as f:
        f.write("Pronoun Usage Analysis by Entity:\n")
        for entity, stats in gender_analysis_results.items():
            f.write(f"{entity.capitalize()}: Total Pronouns = {stats['total_pronouns']}, "
                    f"Average Pronouns per Sentence = {stats['average_pronouns']:.2f}\n")
        f.write("\nPronoun Usage Analysis by Gender:\n")
        f.write(f"Male Average Pronouns per Sentence: {maleAverage}\n")
        f.write(f"Female Average Pronouns per Sentence: {femaleAverage}\n")

    print(f"Final pronoun analysis file created: {pronoun_analysis_file}")

    print("\nProcess completed! Results saved in the OutputFiles directory.")


if __name__ == "__main__":
    main()