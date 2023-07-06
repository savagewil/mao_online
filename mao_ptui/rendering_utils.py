from mao_model.card import Card
from mao_model.deck import Deck
from mao_model.hand import Hand


def render_card(card: Card):
    return f"({card.rank.name} of {card.suit.name})"
    # return chr(card.suit.value + card.rank.value)


def render_hand(hand: Hand):
    return " ".join(f"{idx}:{card}" for idx, card in zip(range(len(hand.cards)), map(render_card, hand.cards)))


def render_deck(deck: Deck):
    return "empty" if len(deck.cards) == 0 else render_card(deck.peek())
