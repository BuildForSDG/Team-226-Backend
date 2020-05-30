from resources.constants import Constants


class TestSetupData:
    USER_1 = {
        "first_name": "Big",
        "last_name": "Bob",
        "username": "bigbob",
        "email": "bigbob@test.com",
        "password": "secret",
    }

    USER_2 = {
        "first_name": "Joe",
        "last_name": "Diss",
        "username": "joediss",
        "email": "joediss@test.com",
        "password": "secret",
    }

    CATEGORY = {"name": "fertilizers", "slug": "best-fertilizers"}

    CATEGORY_CREATE = {
        "name": "fertilizers create",
        "slug": "best-fertilizers-create",
        "created_by_id": 1,
    }

    LOGIN = {"email": "bigbob@test.com", "password": "secret"}

    REGISTER = {"email": "bigbob@test.com", "password": "secret", "password2": "secret"}

    LEASE_LAND = {
        "title": "land 1",
        "cost": 500,
        "for_type": Constants.LEASE,
        "size": 100,
        "size_unit_measurement": "M",
        "location": "Akwa",
        "visibility": "PR",
        "currency": "XAF",
        "lease_rate_periodicity": "h",
    }

    LEASE_LAND_CREATE = {
        "title": "land 2",
        "cost": 500,
        "for_type": Constants.LEASE,
        "size": 100,
        "size_unit_measurement": "M",
        "location": "Akwa",
        "visibility": "PR",
        "currency": "XAF",
        "lease_rate_periodicity": "h",
        "owner_id": 1,
    }

    FREE_LAND = {
        "title": "land 1",
        "for_type": Constants.FREE,
        "size": 100,
        "size_unit_measurement": "M",
        "location": "Akwa",
        "visibility": "PR",
        "lease_rate_periodicity": "h",
    }

    LEASE_LAND_WITHOUT_COST = {
        "title": "land 1",
        "for_type": Constants.LEASE,
        "size": 100,
        "size_unit_measurement": "M",
        "location": "Akwa",
        "visibility": "PR",
        "currency": "XAF",
        "lease_rate_periodicity": "h",
    }

    LEASE_LAND_WITHOUT_PERIODICITY = {
        "title": "land 1",
        "for_type": Constants.LEASE,
        "cost": 100,
        "size": 100,
        "size_unit_measurement": "M",
        "location": "Akwa",
        "visibility": "PR",
        "currency": "XAF",
    }

    LEASE_LAND_WITHOUT_CURRENCY = {
        "title": "land 1",
        "cost": 100,
        "for_type": Constants.LEASE,
        "size": 100,
        "size_unit_measurement": "M",
        "location": "Akwa",
        "visibility": "PR",
        "lease_rate_periodicity": "h",
    }

    LIST = {
        "title": "list 1",
        "description": "more description",
        "visibility": Constants.PUBLIC,
    }

    LIST_CREATE = {
        "title": "list 2",
        "description": "more description",
        "visibility": Constants.PUBLIC,
        "created_by_id": 1,
    }

    COMMENT_CREATE = {"text": "Test comment"}

    POST = {
        "title": "post 1",
        "slug": "post-1",
        "description": "more-description",
        "video_link": "string",
        "visibility": "PR",
        "category": 1,
    }

    POST_CREATE = {
        "title": "post 2",
        "slug": "post-2",
        "description": "more-description",
        "video_link": "string",
        "visibility": "PR",
        "category_id": 1,
        "created_by_id": 1,
    }

    LIST_POST = {"list": 1, "post": 1}

    LIST_POST_BAD = {"list": 1, "post": 1}

    @staticmethod
    def temporary_image():
        """Returns a new temporary image file"""
        import tempfile
        from PIL import Image

        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file, "jpeg")
        tmp_file.seek(
            0
        )  # important because after save(), the fp is already at the end of the file
        return tmp_file
