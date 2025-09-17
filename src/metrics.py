from prometheus_client import Counter

posts_counter = Counter("posts_total", "Total posts made")
likes_counter = Counter("likes_total", "Total likes given")
replies_counter = Counter("replies_total", "Total replies made")
retweets_counter = Counter("retweets_total", "Total retweets made")
engagements_counter = Counter(
    "engagements_total", "Total engagements (likes + replies)"
)
