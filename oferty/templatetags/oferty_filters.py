from django import template

register = template.Library()


@register.filter
def format_price(value):
    if value is None:
        return '—'
    try:
        return f'{int(value):,}'.replace(',', ' ') + ' PLN'
    except (ValueError, TypeError):
        return str(value)


@register.filter
def status_badge(status):
    badges = {
        'dostepne': 'badge-available',
        'sprzedane': 'badge-sold',
        'rezerwacja': 'badge-reserved',
        'w_budowie': 'badge-construction',
    }
    return badges.get(status, '')


@register.filter
def status_label(status):
    labels = {
        'dostepne': 'Dostępne',
        'sprzedane': 'Sprzedane',
        'rezerwacja': 'Rezerwacja',
        'w_budowie': 'W budowie',
    }
    return labels.get(status, status)
