class Constants:
    PRIVATE = "PR"
    PUBLIC = "PU"
    VISIBILITY_TYPE = [(PRIVATE, "private"), (PUBLIC, "public")]

    METERS = "M"
    KILOMETERS = "KM"
    MILES = "ML"
    SIZE_TYPE = [(METERS, "metres"), (KILOMETERS, "kilometres"), (MILES, "miles")]

    FREE = "FR"
    LEASE = "LE"
    FOR_TYPE = [(FREE, "for free"), (LEASE, "for leasing")]

    LEASE_RATE_PERIODICITY = (
        ("h", "hourly"),
        ("d", "daily"),
        ("w", "weekly"),
        ("m", "monthly"),
        ("y", "yearly"),
    )

    XAF = "XAF"

    CURRENCIES = ((XAF, "XAF"),)
