from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

class NotificattionsActivities:
  def run():
    with tracer.start_as_current_span("Notificattions_Activities") as outer_span:
      with tracer.start_as_current_span("Result") as inner_span:
        now = datetime.now(timezone.utc).astimezone()
        outer_span.set_attribute("now", now.isoformat())
        results = [{
          'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
          'handle':  'Benji',
          'message': 'I\'m a dog',
          'created_at': (now - timedelta(days=2)).isoformat(),
          'expires_at': (now + timedelta(days=5)).isoformat(),
          'likes_count': 5,
          'replies_count': 1,
          'reposts_count': 0,
          'replies': [{
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
            'handle':  'Worf',
            'message': 'This post has no honor!',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          }],
        },
        {
          'uuid': '66e12864-8c26-4c3a-9658-95a10f8fea67',
          'handle':  'Worf',
          'message': 'I am out of prune juice',
          'created_at': (now - timedelta(days=7)).isoformat(),
          'expires_at': (now + timedelta(days=9)).isoformat(),
          'likes': 0,
          'replies': []
        },
        {
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Garek',
          'message': 'My dear doctor, I am just simple tailor',
          'created_at': (now - timedelta(hours=1)).isoformat(),
          'expires_at': (now + timedelta(hours=12)).isoformat(),
          'likes': 0,
          'replies': []
        }
        ]
        inner_span.set_attribute("Result_lent", len(results))
        #adding custom span
        with tracer.start_as_current_span("Result_content") as inner_inner_span:
          inner_inner_span.set_attribute("user_id", results[0]['uuid'])
          inner_inner_span.set_attribute("user_handle", results[0]['handle'])
          #Custom span for catching errors --> desactivated to aovid any fake message
          # try:
          #   print(error)
          # except Exception as ex:
          #   inner_inner_span.set_status(Status(StatusCode.ERROR))
          #   inner_inner_span.record_exception(ex) 
        return results