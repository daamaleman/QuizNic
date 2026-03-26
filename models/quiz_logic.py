import random
from collections import deque
from uuid import uuid4


class Question:
    def __init__(self, q_id, category, difficulty, text, options, correct_option, feedback):
        self.id = q_id
        self.category = category
        self.difficulty = difficulty
        self.text = text
        self.options = options
        self.correct_option = correct_option
        self.feedback = feedback

    def to_dict_public(self):
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "text": self.text,
            "options": self.options,
        }


class QuizManager:
    def __init__(self):
        self.question_counter = 0
        self.used_signatures = set()
        self.signature_order = deque()
        self.active_quizzes = {}
        self.player_stats = {}
        self.max_active_quizzes = 250
        self.quiz_size = 10
        self.minimum_quiz_size = 10
        self.max_signature_memory = 200000
        self.knowledge = self._load_knowledge_base()
        self.prompt_openers = [
            "Reto rápido:",
            "Pon a prueba tu memoria:",
            "Desafío de conocimiento:",
            "Pregunta sorpresa:",
            "Misión del turno:",
        ]
        self.prompt_closers = [
            "Elige la mejor opción.",
            "Selecciona la respuesta correcta.",
            "Piensa bien antes de responder.",
            "Confirma tu mejor respuesta.",
            "Marca la opción más precisa.",
        ]

    def _load_knowledge_base(self):
        return {
            "historia": {
                "años": {
                    "Independencia de Centroamérica": 1821,
                    "Batalla de San Jacinto": 1856,
                    "Revolución Francesa": 1789,
                    "Llegada de Colón a América": 1492,
                    "Caída del Imperio Romano de Occidente": 476,
                    "Primera Guerra Mundial (inicio)": 1914,
                    "Segunda Guerra Mundial (inicio)": 1939,
                    "Firma de la Carta de la ONU": 1945,
                    "Fundación de Managua como capital": 1852,
                    "Independencia de Nicaragua (como parte de Centroamérica)": 1821,
                    "Invención de la imprenta por Gutenberg": 1450,
                    "Revolución Rusa": 1917,
                    "Caída del Muro de Berlín": 1989,
                    "Primer alunizaje": 1969,
                },
                "personajes": {
                    "Rubén Darío": "Modernismo literario hispanoamericano",
                    "Augusto C. Sandino": "resistencia contra la intervención estadounidense en Nicaragua",
                    "Simón Bolívar": "independencia de varias naciones sudamericanas",
                    "Miguel de Cervantes": "novela Don Quijote de la Mancha",
                    "Napoleón Bonaparte": "consolidación del Imperio francés",
                    "Mahatma Gandhi": "independencia de la India mediante resistencia no violenta",
                    "Cleopatra": "última gran reina del Egipto ptolemaico",
                    "Abraham Lincoln": "abolición de la esclavitud en Estados Unidos",
                    "Juana de Arco": "apoyo decisivo a Francia en la Guerra de los Cien Años",
                    "Winston Churchill": "liderazgo británico durante la Segunda Guerra Mundial",
                },
            },
            "geografía": {
                "capitales": {
                    "Nicaragua": "Managua",
                    "Honduras": "Tegucigalpa",
                    "Costa Rica": "San José",
                    "El Salvador": "San Salvador",
                    "Guatemala": "Ciudad de Guatemala",
                    "Panamá": "Ciudad de Panamá",
                    "México": "Ciudad de México",
                    "Colombia": "Bogotá",
                    "Perú": "Lima",
                    "Argentina": "Buenos Aires",
                    "Chile": "Santiago",
                    "España": "Madrid",
                    "Francia": "París",
                    "Japón": "Tokio",
                },
                "volcanes_nicaragua": {
                    "San Cristóbal": 1745,
                    "Concepción": 1610,
                    "Telica": 1061,
                    "Maderas": 1394,
                    "Momotombo": 1297,
                    "Masaya": 635,
                    "Cerro Negro": 728,
                    "Cosigüina": 872,
                    "Casita": 1405,
                    "Mombacho": 1344,
                },
                "rios": {
                    "Amazonas": "América del Sur",
                    "Nilo": "África",
                    "Yangtsé": "Asia",
                    "Danubio": "Europa",
                    "Misisipi": "América del Norte",
                    "San Juan": "Nicaragua y Costa Rica",
                    "Coco": "Nicaragua y Honduras",
                    "Ganges": "Asia",
                    "Tíber": "Europa",
                    "Ebro": "Europa",
                },
            },
            "cultura": {
                "obras": {
                    "El Güegüense": "teatro-danza satírico nicaragüense",
                    "Azul": "obra clave del modernismo de Rubén Darío",
                    "Cantos de vida y esperanza": "poemario de madurez de Rubén Darío",
                    "Popol Vuh": "texto sagrado de tradición maya k'iche'",
                    "Don Quijote": "novela cumbre de Miguel de Cervantes",
                    "Cien años de soledad": "novela icónica del realismo mágico latinoamericano",
                    "La divina comedia": "poema épico medieval de Dante",
                    "La Odisea": "epopeya griega atribuida a Homero",
                    "Hamlet": "tragedia escrita por William Shakespeare",
                    "Pedro Páramo": "novela fundamental de Juan Rulfo",
                    "El Principito": "novela corta filosófica de Antoine de Saint-Exupéry",
                    "La metamorfosis": "obra narrativa de Franz Kafka",
                },
                "festividades": {
                    "La Purísima": "celebración mariana tradicional en Nicaragua",
                    "Semana Santa": "conmemoración cristiana de la pasión y resurrección",
                    "Día de los Muertos": "tradición de memoria y homenaje a difuntos",
                    "Carnaval": "fiesta popular previa a la cuaresma",
                    "Fiestas de Santo Domingo": "festividad tradicional de Managua",
                    "Inti Raymi": "celebración andina vinculada al sol",
                    "Hanami": "tradición japonesa de contemplar los cerezos",
                    "Oktoberfest": "festival alemán asociado a la cultura bávara",
                    "Año Nuevo Lunar": "celebración de renovación en Asia oriental",
                    "San Fermín": "fiesta popular de Pamplona",
                },
                "musica": {
                    "Marimba": "instrumento tradicional de percusión melódica en Mesoamérica",
                    "Guitarra clásica": "instrumento central en música iberoamericana",
                    "Piano": "instrumento de teclas ampliamente usado en música académica",
                    "Violín": "instrumento de cuerda frotada de gran versatilidad",
                    "Saxofón": "instrumento de viento de gran presencia en jazz",
                    "Quena": "flauta andina de sonido tradicional",
                    "Bandoneón": "instrumento emblemático del tango",
                    "Cajón": "instrumento de percusión usado en música afroperuana",
                    "Arpa llanera": "instrumento típico de música de los llanos",
                    "Ocarina": "instrumento de viento de origen antiguo",
                },
            },
        }

    def _next_question_id(self):
        self.question_counter += 1
        return f"q{self.question_counter}"

    def _difficulty_label(self, difficulty):
        labels = {
            "básico": "nivel básico",
            "intermedio": "nivel intermedio",
            "avanzado": "nivel avanzado",
        }
        return labels.get(difficulty, "nivel general")

    def _pick_distractors(self, values, correct_value, amount=3):
        pool = [v for v in values if v != correct_value]
        if len(pool) < amount:
            return pool
        return random.sample(pool, amount)

    def _make_question(self, category, difficulty, text, correct, options, feedback):
        random.shuffle(options)
        return Question(
            q_id=self._next_question_id(),
            category=category,
            difficulty=difficulty,
            text=text,
            options=options,
            correct_option=correct,
            feedback=feedback,
        )

    def _signature(self, question):
        joined_options = "|".join(question.options)
        return f"{question.category}|{question.difficulty}|{question.text}|{joined_options}"

    def _remember_signature(self, signature):
        self.used_signatures.add(signature)
        self.signature_order.append(signature)
        if len(self.signature_order) > self.max_signature_memory:
            old_signature = self.signature_order.popleft()
            self.used_signatures.discard(old_signature)

    def _stylize_prompt(self, core_text):
        opener = random.choice(self.prompt_openers)
        closer = random.choice(self.prompt_closers)
        return f"{opener} {core_text} {closer}"

    def _generate_history_question(self, difficulty):
        mode = random.choice(["años", "personajes"])
        level = self._difficulty_label(difficulty)

        if mode == "años":
            event, year = random.choice(list(self.knowledge["historia"]["años"].items()))
            all_years = list(set(self.knowledge["historia"]["años"].values()))
            options = [str(year)] + [str(y) for y in self._pick_distractors(all_years, year, 3)]
            text = self._stylize_prompt(f"[{level}] ¿En qué año ocurrió: {event}?")
            feedback = f"{event} ocurrió en {year}."
            return self._make_question("historia", difficulty, text, str(year), options, feedback)

        person, contribution = random.choice(list(self.knowledge["historia"]["personajes"].items()))
        all_people = list(self.knowledge["historia"]["personajes"].keys())
        options = [person] + self._pick_distractors(all_people, person, 3)
        text = self._stylize_prompt(f"[{level}] ¿Qué personaje histórico se asocia con: {contribution}?")
        feedback = f"La respuesta correcta es {person}, reconocido por {contribution}."
        return self._make_question("historia", difficulty, text, person, options, feedback)

    def _generate_geography_question(self, difficulty):
        mode = random.choice(["capitales", "volcanes", "rios"])
        level = self._difficulty_label(difficulty)

        if mode == "capitales":
            country, capital = random.choice(list(self.knowledge["geografía"]["capitales"].items()))
            all_capitals = list(self.knowledge["geografía"]["capitales"].values())
            options = [capital] + self._pick_distractors(all_capitals, capital, 3)
            text = self._stylize_prompt(f"[{level}] ¿Cuál es la capital de {country}?")
            feedback = f"La capital de {country} es {capital}."
            return self._make_question("geografía", difficulty, text, capital, options, feedback)

        if mode == "volcanes":
            volcano, height = random.choice(list(self.knowledge["geografía"]["volcanes_nicaragua"].items()))
            all_volcanoes = list(self.knowledge["geografía"]["volcanes_nicaragua"].keys())
            options = [volcano] + self._pick_distractors(all_volcanoes, volcano, 3)
            text = self._stylize_prompt(f"[{level}] ¿Qué volcán de Nicaragua tiene aproximadamente {height} metros de altura?")
            feedback = f"{volcano} alcanza aproximadamente {height} metros de altura."
            return self._make_question("geografía", difficulty, text, volcano, options, feedback)

        river, region = random.choice(list(self.knowledge["geografía"]["rios"].items()))
        all_regions = list(set(self.knowledge["geografía"]["rios"].values()))
        options = [region] + self._pick_distractors(all_regions, region, 3)
        text = self._stylize_prompt(f"[{level}] ¿En qué región se ubica principalmente el río {river}?")
        feedback = f"El río {river} se ubica en {region}."
        return self._make_question("geografía", difficulty, text, region, options, feedback)

    def _generate_culture_question(self, difficulty):
        mode = random.choice(["obras", "festividades", "musica"])
        level = self._difficulty_label(difficulty)

        if mode == "obras":
            work, description = random.choice(list(self.knowledge["cultura"]["obras"].items()))
            all_works = list(self.knowledge["cultura"]["obras"].keys())
            options = [work] + self._pick_distractors(all_works, work, 3)
            text = self._stylize_prompt(f"[{level}] ¿Qué obra corresponde a esta descripción: {description}?")
            feedback = f"La descripción corresponde a {work}."
            return self._make_question("cultura", difficulty, text, work, options, feedback)

        if mode == "festividades":
            festivity, meaning = random.choice(list(self.knowledge["cultura"]["festividades"].items()))
            all_festivities = list(self.knowledge["cultura"]["festividades"].keys())
            options = [festivity] + self._pick_distractors(all_festivities, festivity, 3)
            text = self._stylize_prompt(f"[{level}] ¿Qué festividad se define como: {meaning}?")
            feedback = f"La definición corresponde a {festivity}."
            return self._make_question("cultura", difficulty, text, festivity, options, feedback)

        instrument, note = random.choice(list(self.knowledge["cultura"]["musica"].items()))
        all_instruments = list(self.knowledge["cultura"]["musica"].keys())
        options = [instrument] + self._pick_distractors(all_instruments, instrument, 3)
        text = self._stylize_prompt(f"[{level}] ¿Qué instrumento encaja mejor con esta descripción: {note}?")
        feedback = f"La respuesta correcta es {instrument}."
        return self._make_question("cultura", difficulty, text, instrument, options, feedback)

    def _generate_question(self, category, difficulty):
        generators = {
            "historia": self._generate_history_question,
            "geografía": self._generate_geography_question,
            "cultura": self._generate_culture_question,
        }
        generator = generators.get(category)
        if not generator:
            return None
        return generator(difficulty)

    def _prune_old_quizzes(self):
        if len(self.active_quizzes) <= self.max_active_quizzes:
            return

        surplus = len(self.active_quizzes) - self.max_active_quizzes
        keys_to_remove = list(self.active_quizzes.keys())[:surplus]
        for key in keys_to_remove:
            self.active_quizzes.pop(key, None)

    def _empty_stats(self, player_name):
        return {
            "player_name": player_name,
            "quizzes_played": 0,
            "questions_answered": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "accuracy": 0,
            "total_score": 0,
            "average_score": 0,
            "best_score": 0,
            "best_accuracy": 0,
            "current_streak": 0,
            "best_streak": 0,
            "category_performance": {},
            "difficulty_performance": {},
            "recent_scores": [],
        }

    def _upsert_bucket(self, store, key):
        if key not in store:
            store[key] = {
                "key": key,
                "quizzes": 0,
                "questions": 0,
                "correct": 0,
                "incorrect": 0,
                "accuracy": 0,
            }
        return store[key]

    def _recalc_bucket_accuracy(self, bucket):
        if bucket["questions"] == 0:
            bucket["accuracy"] = 0
            return
        bucket["accuracy"] = round((bucket["correct"] / bucket["questions"]) * 100, 2)

    def _update_player_stats(self, player_name, quiz_summary, quiz_meta):
        safe_player = player_name.strip() if player_name else "Anónimo"
        stats = self.player_stats.get(safe_player)
        if not stats:
            stats = self._empty_stats(safe_player)

        questions_answered = quiz_summary["correct_answers"] + quiz_summary["incorrect_answers"]
        quiz_accuracy = quiz_summary["percentage"]

        stats["quizzes_played"] += 1
        stats["questions_answered"] += questions_answered
        stats["correct_answers"] += quiz_summary["correct_answers"]
        stats["incorrect_answers"] += quiz_summary["incorrect_answers"]
        stats["total_score"] += quiz_summary["score"]
        stats["best_score"] = max(stats["best_score"], quiz_summary["score"])
        stats["best_accuracy"] = max(stats["best_accuracy"], round(quiz_accuracy, 2))

        if stats["questions_answered"] > 0:
            stats["accuracy"] = round((stats["correct_answers"] / stats["questions_answered"]) * 100, 2)
        stats["average_score"] = round(stats["total_score"] / stats["quizzes_played"], 2)

        if quiz_accuracy >= 60:
            stats["current_streak"] += 1
            stats["best_streak"] = max(stats["best_streak"], stats["current_streak"])
        else:
            stats["current_streak"] = 0

        category_key = quiz_meta.get("category", "desconocida")
        difficulty_key = quiz_meta.get("difficulty", "desconocida")

        category_bucket = self._upsert_bucket(stats["category_performance"], category_key)
        category_bucket["quizzes"] += 1
        category_bucket["questions"] += questions_answered
        category_bucket["correct"] += quiz_summary["correct_answers"]
        category_bucket["incorrect"] += quiz_summary["incorrect_answers"]
        self._recalc_bucket_accuracy(category_bucket)

        difficulty_bucket = self._upsert_bucket(stats["difficulty_performance"], difficulty_key)
        difficulty_bucket["quizzes"] += 1
        difficulty_bucket["questions"] += questions_answered
        difficulty_bucket["correct"] += quiz_summary["correct_answers"]
        difficulty_bucket["incorrect"] += quiz_summary["incorrect_answers"]
        self._recalc_bucket_accuracy(difficulty_bucket)

        stats["recent_scores"].insert(
            0,
            {
                "score": quiz_summary["score"],
                "accuracy": round(quiz_accuracy, 2),
                "category": category_key,
                "difficulty": difficulty_key,
            },
        )
        stats["recent_scores"] = stats["recent_scores"][:8]

        self.player_stats[safe_player] = stats

    def get_player_stats(self, player_name):
        safe_player = player_name.strip() if player_name else "Anónimo"
        stats = self.player_stats.get(safe_player)
        if not stats:
            return self._empty_stats(safe_player)
        return stats

    def create_quiz(self, category, difficulty, count=None):
        target = max(count or self.quiz_size, self.minimum_quiz_size)
        questions = []
        attempts = 0
        max_attempts = target * 500

        while len(questions) < target and attempts < max_attempts:
            attempts += 1
            question = self._generate_question(category, difficulty)
            if question is None:
                break

            signature = self._signature(question)
            if signature in self.used_signatures:
                continue

            self._remember_signature(signature)
            questions.append(question)

        if len(questions) < target:
            # Evita vacíos incluso cuando hay alta colisión de firmas.
            while len(questions) < target:
                question = self._generate_question(category, difficulty)
                if question is None:
                    break

                signature = self._signature(question)
                variant = 1
                while signature in self.used_signatures:
                    question.text = f"{question.text} [variante {variant}]"
                    signature = self._signature(question)
                    variant += 1

                self._remember_signature(signature)
                questions.append(question)

        quiz_id = uuid4().hex
        self.active_quizzes[quiz_id] = {
            "questions": {q.id: q for q in questions},
            "meta": {
                "category": category,
                "difficulty": difficulty,
            },
        }
        self._prune_old_quizzes()
        return quiz_id, questions

    def evaluate_answers(self, quiz_id, user_answers, player_name="Anónimo"):
        selected_quiz = self.active_quizzes.get(quiz_id, {})
        quiz_questions = selected_quiz.get("questions", {})
        quiz_meta = selected_quiz.get("meta", {})
        correct_count = 0
        incorrect_count = 0
        feedback_list = []

        for q_id, answer in user_answers.items():
            question = quiz_questions.get(q_id)
            if not question:
                continue

            is_correct = question.correct_option == answer
            if is_correct:
                correct_count += 1
            else:
                incorrect_count += 1

            feedback_list.append(
                {
                    "question_text": question.text,
                    "user_answer": answer,
                    "correct_answer": question.correct_option,
                    "is_correct": is_correct,
                    "feedback": question.feedback,
                }
            )

        total = correct_count + incorrect_count
        percentage = (correct_count / total * 100) if total > 0 else 0

        if percentage == 100:
            message = "Excelente trabajo. Nivel experto."
        elif percentage >= 60:
            message = "Buen rendimiento. Sigue subiendo de nivel."
        else:
            message = "Sigue practicando. Cada intento te hace mejorar."

        result = {
            "score": correct_count * 10,
            "correct_answers": correct_count,
            "incorrect_answers": incorrect_count,
            "percentage": percentage,
            "motivational_message": message,
            "details": feedback_list,
        }

        self._update_player_stats(player_name, result, quiz_meta)
        return result