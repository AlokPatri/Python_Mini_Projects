import json
import random, csv
from functools import reduce

def load_flashcards():
    try:
        with open("flashcards.json", 'r') as file:
            content = file.read().strip()
            if not content:
                return []  # Empty file → return empty list
            return json.loads(content)
    except FileNotFoundError:
        return []
    
def save_flashcards(cards):
    with open("flashcards.json", "w") as file:
        json.dump(cards, file, indent=4)

def add_flashcard():
    question = input("Enter the question: ")
    answer = input("Enter the answer: ")

    cards = load_flashcards()
    cards.append({'q': question, 'a': answer})
    save_flashcards(cards)

    print("✅ Flashcard added!")
    
#add_flashcard()

def start_quiz():
    cards = load_flashcards()
    if not cards:
        print("No flashcards availabe!")
        return
    
    random.shuffle(cards)
    correct = 0
    wrong = 0
    wrong_cards = []

    for card in cards:
        user_ans = input(f"Q: {card['q']}\nYuor answer:")
        if user_ans.lower() == card['a'].lower():
            print("✅ Correct!")
            correct +=1
        else:
            print(f"❌ Wrong! The correct answer is: {card['a']}")
            wrong += 1
            wrong_cards.append(card)
    
    print(f"🎯 Quiz completed Correct: {correct}, wrong: {wrong} ")
    log_result(correct, wrong)

    if wrong_cards:
        retry = input("🔁 Retry wrong ones? (y/n):")
        if retry.lower() == 'y':
            start_quiz_from_wrong(wrong_cards)


def start_quiz_from_wrong(cards):
    correct = 0
    wrong = 0
    for card in cards:
        user_ans = input(f"Q: {card['q']}\nYour answer:")
        if user_ans.lower() == card['a'].lower():
            print("✅ Correct!")
            correct += 1
        else:
            print(f"❌ Wrong! The correct answer is: {card['a']}")
            wrong += 1
    print(f"🔁 Quiz completed Correct: {correct}, wrong: {wrong} "  )

def log_result(correct, wrong):
    with open("results.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([correct, wrong])

def show_stats():
    try:
        with open("results.csv", 'r') as file:
            reader = csv.reader(file)
            scores = list(reader)

        if not scores:
            print("No quiz results available.")
            return
        
        totals = [int(r[0]) + int(r[1]) for r in scores]
        avg = reduce(lambda x, y: x + y, totals) / len(totals)
        print(f"📊 Average Questions per Quiz: {avg:.2f}")
    
    except FileNotFoundError:
        print("❌ No results found yet.")

def main():
    while True:
        print("\n====MemoryPal====")
        print("1. Add Flashcard")
        print("2. Start Quiz")
        print("3. Show Stats")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            add_flashcard()
        elif choice == '2':
            start_quiz()
        elif choice == '3':
            show_stats()
        elif choice == '4':
            print("👋 Exiting MemoryPal. Bye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

    
if __name__ == "__main__":
    main()
