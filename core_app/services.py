# core_app/services.py
from django.contrib.auth.models import User
from django.db.models import Count, Q, Case, When, IntegerField

ACTIVE_STATUSES = ['Assigned', 'En Route']

def choose_best_volunteer(max_active_tasks: int = 1) -> User | None:
    """
    Pick the best volunteer:
      1) Prefer users with Profile.role='volunteer'
      2) Fall back to any active staff user (even if Profile missing)
      3) Among candidates, choose the fewest active tasks (Assigned/En Route)
      4) Tie-break by user id
    """
    base_qs = (
        User.objects.filter(
            is_active=True,
            is_staff=True,  # your app treats staff as volunteers/NGO operators
        )
        .select_related('profile')
        .annotate(
            # put proper volunteers first (0), others later (1)
            is_volunteer_role=Case(
                When(profile__role='volunteer', then=0),
                default=1,
                output_field=IntegerField(),
            ),
            active_tasks=Count(
                'assigned_tasks',  # from ReliefRequest.assigned_to_volunteer related_name
                filter=Q(assigned_tasks__status__in=ACTIVE_STATUSES),
            ),
        )
        .order_by('is_volunteer_role', 'active_tasks', 'id')
    )

    if not base_qs.exists():
        return None

    # Prefer candidates under capacity
    available = base_qs.filter(active_tasks__lt=max_active_tasks)
    if available.exists():
        return available.first()

    # Otherwise, least busy overall
    return base_qs.first()
