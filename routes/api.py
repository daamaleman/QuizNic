from flask import Blueprint, request, jsonify
from models.quiz_logic import QuizManager

api_bp = Blueprint('api', __name__)
quiz_manager = QuizManager()

@api_bp.route('/get_quiz', methods=['GET'])
def get_quiz():
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')

    quiz_id, questions = quiz_manager.create_quiz(category, difficulty, count=10)
    return jsonify({
        'quiz_id': quiz_id,
        'questions': [q.to_dict_public() for q in questions]
    })

@api_bp.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    quiz_id = data.get('quiz_id')
    user_answers = data.get('answers', {})
    player_name = data.get('player_name', 'Anónimo')

    result = quiz_manager.evaluate_answers(quiz_id, user_answers, player_name=player_name)
    return jsonify(result)


@api_bp.route('/player_stats', methods=['GET'])
def player_stats():
    player_name = request.args.get('player_name', 'Anónimo')
    stats = quiz_manager.get_player_stats(player_name)
    return jsonify(stats)