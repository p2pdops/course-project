from db import get_db


def get_topics(subject_id, user_id):
    db = get_db()
    topics = db.execute(
        f"""
        SELECT 
            t.id as	id, t.name as name,
            t.content as content,
            t.subject_id as subject_id,
            s.id as score_id, s.score as last_score
        FROM topics t
        LEFT JOIN user_scores s ON s.topic_id = t.id AND s.user_id = {user_id}
        where subject_id = {subject_id}
        """
    ).fetchall()
    return topics
