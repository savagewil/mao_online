from mao_model.card import Card


def render_card(card: Card):
    return chr(card.suit.value + card.rank.value)
