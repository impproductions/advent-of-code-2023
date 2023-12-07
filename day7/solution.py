from pathlib import Path
from pprint import pprint
from typing import Callable, Counter

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

games = [l.split(" ")[0] for l in lines]
bids = [int(l.split(" ")[1]) for l in lines]

hands_scoring = {
    (5,): 6,
    (4, 1): 5,
    (3, 2): 4,
    (3, 1, 1): 3,
    (2, 2, 1): 2,
    (2, 1, 1, 1): 1,
    (1, 1, 1, 1, 1): 0,
}


def count_hand_with_jokers(hand):
    count = Counter(hand)
    j_count = count.get("J", 0)
    if j_count in {5, 0}:
        return count
    del count["J"]
    count[count.most_common(1)[0][0]] += j_count
    return count


def score_games(cards, hand_counter):
    card_values = {v: i for i, v in enumerate(cards[::-1])}
    bid_for_score = {}
    scores = []
    for i, game in enumerate(games):
        card_counts = hand_counter(game)
        hand_score = hands_scoring[(*sorted(card_counts.values(), reverse=True),)]
        scoring_base = [hand_score] + [card_values[card] for card in game]
        game_score = sum(
            [score * (13 ** (6 - i)) for i, score in enumerate(scoring_base)]
        )
        bid_for_score[game_score] = bids[i]
        scores.append(game_score)

    return sum([(i + 1) * bid_for_score[score] for i, score in enumerate(sorted(scores))])


def part1():
    return score_games("AKQJT98765432", Counter)


def part2():
    return score_games("AKQT98765432J", count_hand_with_jokers)


print(part1())
print(part2())
