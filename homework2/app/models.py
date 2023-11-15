from django.db import models


def createAnswers(amount):
    return [
        {
            'id': answer_id,
            'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.' * answer_id,
            'like_number': answer_id,
            'correct': answer_id % 2 if True else False,
        } for answer_id in range(1, amount)
    ]


QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question {question_id}',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.' * question_id,
        'like_number': question_id,
        'answers_number': question_id-1,
        'tags': [f'Tag {i}' for i in range(1, question_id+1)],
        'answers': createAnswers(question_id)
    } for question_id in range(1, 10)
]


OPTIONS = {
    'username': 'Zefir',
    'password': 'password',
    'nickname': 'Zefirka',
    'is_auth': True
}


TAGS = [
    {
        'name': f'Tag {tag_id}'
    } for tag_id in range(1, 10)
]