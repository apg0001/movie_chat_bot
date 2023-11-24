from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector
import random

class ActionStoreUserInfo(Action):
    def name(self) -> Text:
        return "action_store_user_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # 사용자 입력 가져오기
        director = tracker.get_slot("director")
        genre = tracker.get_slot("genre")

        # 정보를 슬롯에 저장
        return [SlotSet("director", director),SlotSet("genre", genre) ]

class ActionRecommendMovie(Action):
    def name(self) -> Text:
        return "action_recommend_movie"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 슬롯에서 사용자 정보 가져오기
        user_director = tracker.get_slot("director")
        user_genre = tracker.get_slot("genre")

        # 사용자 입력이 없는 경우 무작위로 추천
        if not any([user_director, user_genre]):
            recommended_movie = self.get_random_movie()
        else:
            # 사용자 입력을 기반으로 SQL 쿼리 작성
            sql_query = "SELECT * FROM movies"
            if user_director:
                sql_query += f" WHERE director LIKE '{user_director}'"
                if user_genre:
                    sql_query += f" AND genre LIKE '{user_genre}'"
            else:
                if user_genre:
                    sql_query += f" WHERE genre LIKE '{user_genre}'"

            # MySQL 커넥터를 사용하여 SQL 쿼리 실행
            try:
                db_host = "127.0.0.1"
                db_user = "root"
                db_password = "qkrrlcks11!@#"
                db_database = "movie_database"
                conn = mysql.connector.connect(
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    database=db_database,
                )

                cursor = conn.cursor(dictionary=True)
                cursor.execute(sql_query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()

                # Check if there are no matching movies
                if not results:
                    dispatcher.utter_message("There are no movies that match the information you entered. I will recommend a movie instead.")
                    recommended_movie = self.get_random_movie()
                else:
                    recommended_movie = random.choice(results)

            except Exception as e:
                print(f"Error connecting to the database: {e}")
                dispatcher.utter_message("An error occurred while fetching movie recommendations.")
                return []

        # 추천된 영화 표시
        message = (
            f"I recommend the movie '{recommended_movie['movie_title']}' directed by "
            f"{recommended_movie['director']} in the genre '{recommended_movie['genre']}'."
        )
        dispatcher.utter_message(message)

        return []

    def get_random_movie(self):
        # 데이터베이스에서 모든 영화 가져오기
        try:
            db_host = "127.0.0.1"
            db_user = "root"
            db_password = "qkrrlcks11!@#"
            db_database = "movie_database"
            conn = mysql.connector.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                database=db_database,
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM movies")
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            # 무작위로 추천된 영화 선택
            return random.choice(results) if results else None

        except Exception as e:
            print(f"데이터베이스에 연결 중 오류 발생: {e}")
            return None

class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 인사 메시지 표시
        dispatcher.utter_message("Hello! How can I assist you today?")
        return []