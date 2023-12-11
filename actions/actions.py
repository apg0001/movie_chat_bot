from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector
import random


base_sql = None

class ActionStoreUserInfo(Action):
    def name(self) -> Text:
        return "action_store_user_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # 사용자 입력 가져오기
        genre = tracker.get_slot("genre")
        rating = tracker.get_slot("rating")
        platform = tracker.get_slot("platform")

        # 정보를 슬롯에 저장
        return [
            SlotSet("genre", genre),
            SlotSet("rating", rating),
            SlotSet("platform", platform),
        ]


class ActionRecommendMovie(Action):
    def name(self) -> Text:
        return "action_recommend_movie"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # 슬롯에서 사용자 정보 가져오기
        user_genre = tracker.get_slot("genre")
        user_rating = tracker.get_slot("rating")
        user_platform = tracker.get_slot("platform")

        # 사용자 입력을 기반으로 SQL 쿼리 작성
        sql_query = f"SELECT * FROM movies WHERE genre LIKE '{user_genre}' AND Platform LIKE '{user_platform}' AND rating >= '{user_rating}'"
        base_sql = sql_query

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
                dispatcher.utter_message(
                    "There are no movies that match the information you entered. I will recommend another movie instead."
                )
                recommended_movie = self.get_random_movie()
            else:
                recommended_movie = random.choice(results)

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            dispatcher.utter_message(
                "An error occurred while fetching movie recommendations."
            )
            return [
                SlotSet("genre", None),
                SlotSet("platform", None),
                SlotSet("rating", None),
            ]

        # 추천된 영화 표시
        message = (
            f"I recommend the movie '{recommended_movie['Title']}' directed by '{recommended_movie['Director']}'"
            f"'{recommended_movie['Director']}' in the genre '{recommended_movie['Genre']}'."
        )
        dispatcher.utter_message(message)

        return [
            SlotSet("genre", None),
            SlotSet("platform", None),
            SlotSet("rating", None),
        ]

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


class ActionSearchMovie(Action):
    def name(self) -> Text:
        return "action_search_movie"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # 슬롯에서 사용자 정보 가져오기
        user_movie_title = tracker.get_slot("movie_title")

        # 사용자 입력을 기반으로 SQL 쿼리 작성
        sql_query = f"SELECT * FROM movies WHERE title LIKE '{user_movie_title}'"

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
                dispatcher.utter_message(
                    f"There is no movie that matches title: '{user_movie_title}'. Search for another movie."
                )
                return [SlotSet("movie_title", None)]
            else:
                movie_info = random.choice(results)

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            dispatcher.utter_message(
                "An error occurred while fetching movie recommendations."
            )
            return [SlotSet("movie_title", None)]

        # 일치하는 영화 찾아 정보 보여주기
        message = f"Title: \t\t'{movie_info['Title']}'\nDirector: \t{movie_info['Director']}\nMain actor: \t{movie_info['MainActors']}\nGenre: \t\t{movie_info['Genre']}\nRating: \t{movie_info['Rating']}\nCountry: \t{movie_info['Country']}\nPlatform: \t{movie_info['Platform']}\nSynopsis: \t{movie_info['Synopsis']}"
        dispatcher.utter_message(message)

        return [SlotSet("movie_title", None)]

class ActionStoreUserInfoDetail(Action):
    def name(self) -> Text:
        return "action_store_user_info_detail"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # 사용자 입력 가져오기
        director = tracker.get_slot("director")
        country = tracker.get_slot("country")
        age = tracker.get_slot("age")

        # 정보를 슬롯에 저장
        return [
            SlotSet("director", director),
            SlotSet("country", country),
            SlotSet("age", age),
        ]
    
class ActionRecommendMovie(Action):
    def name(self) -> Text:
        return "action_recommend_movie_detail"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # 슬롯에서 사용자 정보 가져오기
        user_director = tracker.get_slot("director")
        user_country = tracker.get_slot("country")
        user_age = tracker.get_slot("age")

        # 사용자 입력을 기반으로 SQL 쿼리 작성
        sql_query = base_sql
        if user_director:
            sql_query += f" AND LIKE '{user_director}'"
        if user_country:
            sql_query += f" AND LIKE '{user_country}'"
        if user_age:
            sql_query += f" AND AgeLimit >= '{user_age}'"

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
                dispatcher.utter_message(
                    "There are no movies that match the information you entered. I will recommend another movie instead."
                )
                recommended_movie = self.get_random_movie()
            else:
                recommended_movie = random.choice(results)

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            dispatcher.utter_message(
                "An error occurred while fetching movie recommendations."
            )
            return [
                SlotSet("director", None),
                SlotSet("country", None),
                SlotSet("age", None),
            ]

        # 추천된 영화 표시
        message = (
            f"I recommend the movie '{recommended_movie['Title']}' directed by '{recommended_movie['Director']}'"
            f"'{recommended_movie['Director']}' in the genre '{recommended_movie['Genre']}'."
        )
        dispatcher.utter_message(message)

        return [
            SlotSet("director", None),
            SlotSet("country", None),
            SlotSet("age", None),
        ]

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