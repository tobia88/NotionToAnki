FIELDS = [
    {'name': 'Name'},
    {'name': 'Meaning'},
    {'name': 'Sentence 1'},
    {'name': 'Translation 1'},
    {'name': 'Sentence 2'},
    {'name': 'Translation 2'},
    {'name': 'Sentence 3'},
    {'name': 'Translation 3'},
    {'name': 'Compare Word 1'},
    {'name': 'Compare Meaning 1'},
    {'name': 'Compare Word 2'},
    {'name': 'Compare Meaning 2'},
    {'name': 'Compare Word 3'},
    {'name': 'Compare Meaning 3'},
    {'name': 'Root'},
    {'name': 'Illustration'}
]

TEMPLATES = [
    {
        'name': 'Card 1',
        'qfmt': (
            '<style>'
            '.card { font-family: Arial, sans-serif; font-size: 24px; text-align: center; color: #ddd; background-color: #222; padding: 20px; border-radius: 10px; rgba(0, 0, 0, 0.1); }'
            '.name { font-size: 28px; font-weight: bold; color: #fff; }'
            '</style>'
            '<div class="card">'
            '<div class="name">{{Name}}</div>'
            '</div>'
        ),
        'afmt': (
            '{{FrontSide}}<hr id="answer">'
            '<style>'
            '.card { font-family: Arial, sans-serif; font-size: 20px; text-align: center; color: #ddd; background-color: #222; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }'
            '.highlight { font-weight: bold; color: #e74c3c; font-size: 22px; margin-bottom: 10px; }'
            '.sentence { color: #3498db; margin-top: 10px; font-size: 18px; }'
            '.translation { color: #2ecc71; margin-top: 5px; font-size: 18px; }'
            '.compare { margin-top: 10px; font-size: 18px; }'
            '.root { margin-top: 15px; font-size: 18px; font-style: italic; color: #8e44ad; margin-bottom: 10px; }'
            '.illustration { margin-top: 10px; font-size: 18px; color: #f39c12; }'
            '</style>'
            '<div class="card">'
            '<div class="highlight">{{Meaning}}</div>'
            '<div class="root">{{Root}}</div>'
            '<div class="illustration">{{Illustration}}</div><br>'
            '<div class="sentence">{{Sentence 1}}</div>'
            '<div class="translation">{{Translation 1}}</div><br>'
            '<div class="sentence">{{Sentence 2}}</div>'
            '<div class="translation">{{Translation 2}}</div><br>'
            '<div class="sentence">{{Sentence 3}}</div>'
            '<div class="translation">{{Translation 3}}</div><br>'
            '<div class="compare">{{Compare Word 1}}: {{Compare Meaning 1}}</div>'
            '<div class="compare">{{Compare Word 2}}: {{Compare Meaning 2}}</div>'
            '<div class="compare">{{Compare Word 3}}: {{Compare Meaning 3}}</div><br>'
            '</div>'
        ),
    },
]
