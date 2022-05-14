from db import get_db


def get_topics(subject_id, user_id):
    db = get_db()
    topics = db.execute(
        f"""
        SELECT 
            t.id as	id, t.name as name,
            t.content as content,
            t.subject_id as subject_id,
            s.score as last_score
        FROM topics t
        LEFT JOIN user_scores s ON s.topic_id = t.id AND s.user_id = {user_id}
        where subject_id = {subject_id}
        """
    ).fetchall()
    topics = [dict(row) for row in topics]
    for i, topic in enumerate(topics):
        topic['last_score'] = topic['last_score'] or 0
        if i == 0 or topics[i-1]['last_score'] > 0:
            topic['allowed'] = True
        else:
            topic['allowed'] = False
    print("topics", topics)
    return topics


def insert_score(score, topic_id, user_id):
    db = get_db()
    db.execute(
        f"""
        INSERT OR REPLACE INTO user_scores (topic_id,user_id, score)
        VALUES (?,?,?)
        """, (topic_id, user_id, score)
    )
    db.commit()
    return True


def get_user_score(topic_id, user_id):
    db = get_db()
    score = db.execute(
        f"""
        SELECT score FROM user_scores WHERE topic_id = {topic_id} AND user_id = {user_id}
        """
    ).fetchone()
    return dict(score)
