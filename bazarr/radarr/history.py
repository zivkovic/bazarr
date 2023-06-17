# coding=utf-8

from datetime import datetime

from app.database import TableHistoryMovie, database, insert
from app.event_handler import event_stream


def history_log_movie(action, radarr_id, result, fake_provider=None, fake_score=None):
    description = result.message
    video_path = result.path
    language = result.language_code
    provider = fake_provider or result.provider
    score = fake_score or result.score
    subs_id = result.subs_id
    subtitles_path = result.subs_path
    matched = result.matched
    not_matched = result.not_matched

    database.execute(
        insert(TableHistoryMovie)
        .values(
            action=action,
            radarrId=radarr_id,
            timestamp=datetime.now(),
            description=description,
            video_path=video_path,
            language=language,
            provider=provider,
            score=score,
            subs_id=subs_id,
            subtitles_path=subtitles_path,
            matched=str(matched) if matched else None,
            not_matched=str(not_matched) if not_matched else None
        ))
    event_stream(type='movie-history')
