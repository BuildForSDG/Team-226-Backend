from django.db import models
from django.db.models import Q


class LandQuerySet(models.QuerySet):
    def get_all_lands(self, user_id):
        return self.filter(owner__id=user_id) if user_id is not None else self.all()

    def get_land(self, land_id):
        return self.get(id=land_id)


class CategoryQuerySet(models.QuerySet):
    def get_all_categories(self, user_id):
        return (
            self.filter(created_by__id=user_id) if user_id is not None else self.all()
        )


class UserCategoryQuerySet(models.QuerySet):
    def get_user_category(self, user_id, category_id):
        return self.filter(Q(user__id=user_id) & Q(category__id=category_id))


class PostQuerySet(models.QuerySet):
    def get_all_posts(self, user_id):
        return (
            self.filter(created_by__id=user_id) if user_id is not None else self.all()
        )

    def get_post(self, post_id):
        return self.get(id=post_id)

    def get_user_post(self, user_id, post_id):
        return self.filter(Q(created_by_id=user_id) & Q(id=post_id))


class ListQuerySet(models.QuerySet):
    def get_all_lists(self, user_id):
        return (
            self.filter(created_by__id=user_id) if user_id is not None else self.all()
        )

    def get_list(self, list_id):
        return self.get(id=list_id)

    def get_user_list(self, user_id, list_id):
        return self.filter(Q(created_by_id=user_id) & Q(id=list_id))

    def get_all_post_in_list(self, list_id):
        qs = self.filter(id=list_id)
        if qs.exists():
            return qs[0].listing.all()
        return None


class ListPostQuerySet(models.QuerySet):
    def get_list_post(self, user_id, list_id, post_id):
        return self.filter(Q(list=list_id) & Q(post=post_id) & Q(user=user_id))


class CommentQuerySet(models.QuerySet):
    def get_comments_for_post(self, post_id):
        return self.filter(post=post_id)


# class CommentImageQuerySet(models.Query)
