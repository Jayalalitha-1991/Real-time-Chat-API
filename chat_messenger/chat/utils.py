from django.core.cache import cache

def set_user_online(user_id):
    cache.set(f"user_online_{user_id}", True, timeout=60)

def is_user_online(user_id):
    return cache.get(f"user_online_{user_id}") is not None
