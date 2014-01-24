REGIONS = (
    (1, "Northeast"),
    (2, "Midwest"),
    (3, "South"), 
    (4, "West"),
    (9, "Puerto Rico and the Island Areas"),
)

DIVISIONS = (
    (0, "Puerto Rico and the Island Areas"),
    (1, "New England"),
    (2, "Middle Atlantic"),
    (3, "East North Central"),
    (4, "West North Central"),
    (5, "South Atlantic"),
    (6, "East South Central"),
    (7, "West South Central"),
    (8, "Mountain"),
    (9, "Pacific"),
)

# Counties

COUNTY_LEGAL_DESCRIPTION = (
    (0, ""),
    (3, "City and Borough"),
    (4, "Borough"),
    (5, "Census Area"),
    (6, "County"),
    (7, "District"),
    (10, "Island"),
    (12, "Municipality"),
    (13, "Municipio"),
    (15, "Parish"),
    (25, "City"),
)
COUNTY_CLASS_CODE = (
    ('C7', "An incorporated place that is independent of any county."),
    ('H1', "An active county or equivalent feature."),
    ('H4', "An inactive county or equivalent feature."),
    ('H5', "A statistical county equivalent feature."),
    ('H6', "A county that is coextensive with an incorporated place, part of an incorporated place, or a consolidated city and the governmental functions of the county are part of the municipal govenment."),
)
COUNTY_FUNCTIONAL_STATUS = (
    ('A', "Active government providing primary general-purpose functions."),
    ('B', "Active government that is partially consolidated with another government but with separate officials providing primary general-purpose functions."),
    ('C', "Active government consolidated with another government with a single set of officials."),
    ('D', "Defunct Entity"),
    ('F', "Fictitious Entity created to fill the Census Bureau geographic hierarchy."),
    ('G', "Active government that is subordinate to another unit of government."),
    ('N', "Nonfunctioning legal entity."),
    ('S', "Statistical Entity"),
)

# Subcounties

SUBCOUNTY_LEGAL_DESCRIPTION = (
    (0, ""),
    (20, "barrio"),
    (21, "borough"),
    (22, "census county division"),
    (23, "census subarea"),
    (24, "census subdistrict"),
    (25, "city"),
    (26, "county"),
    (27, "district"),
    (28, "District"),
    (29, "precinct"),
    (30, "Precinct"),
    (31, "gore"),
    (32, "grant"),
    (36, "location"),
    (37, "municipality"),
    (39, "plantation"),
    (41, "barrio-pueblo"),
    (42, "purchase"),
    (43, "town"),
    (44, "township"),
    (45, "Township"),
    (46, "Unorganized Territory"),
    (47, "village"),
    (49, "charter township"),
    (86, "Reservation"),
)


SUBCOUNTY_CLASS_CODES = (
    ('C2', "An active incorporated place that is legally coextensive with an county subdivision but treated as independent of any county subdivision."),
    ('C5', "An active incorporated place that is independent of any county subdivision and serves as a county subdivision equivalent."),
    ('C7', "An incorporated place that is independent of any county."),
    ('S1', "A nonfunctioning county subdivision that is coextensive with a census designated place."),
    ('S2', "A statistical county subdivision that is coextensive with a census designated place."),
    ('S3', "A statistical county subdivision that is coextensive with a legal American Indian, Alaska Native, or Native Hawaiian area."),
    ('T1', "An active county subdivision that is not coextensive with an incorporated place."),
    ('T2', "An active county subdivision that is coextensive with a census designated place."),
    ('T5', "An active county subdivision that is coextensive with an incorporated place."),
    ('T9', "An inactive county subdivision."),
    ('Z1', "A nonfunctioning county subdivision."),
    ('Z2', "A county subdivision that is coextensive with an American Indian, Alaska Native, or Native Hawaiian area and legally is independent of any other county subdivision."),
    ('Z3', "A county subdivision defined as an unorganized territory."),
    ('Z5', "A statistical county subdivision."),
    ('Z7', "A county subdivision that is coextensive with a county or equivalent feature or all or part of an incorporated place that the Census Bureau recognizes separately."),
    ('Z9', "Area of a county or equivalent, generally in territorial sea, where no county subdivision exists."),
)

SUBCOUNTY_FUNCTIONAL_STATUS = (
    ('A', "Active government providing primary general-purpose functions."),
    ('B', "Active government that is partially consolidated with another government but with separate officials providing primary general-purpose functions."),
    ('C', "Active government consolidated with another government with a single set of officials."),
    ('D', "Defunct Entity."),
    ('F', "Fictitious entity created to fill the Census Bureau geographic hierarchy."),
    ('G', "Active government that is subordinate to another unit of government."),
    ('I', "Inactive governmental unit that has the power to provide primary special-purpose functions."),
    ('N', "Nonfunctioning legal entity."),
    ('S', "Statistical entity."),
)


# extra
# s - suffix, p - prefix
LEGAL_DESCRIPTION_POSITION = (
    (0, ''),
    (3, 's'),
    (4, 's'),
    (5, 's'),
    (6, 's'),
    (7, 's'),
    (10, 's'),
    (12, 's'),
    (13, 's'),
    (15, 's'),
    (20, 's'),
    (21, 's'),
    (22, 's'),
    (23, 's'),
    (24, 's'),
    (25, 's'),
    (26, 's'),
    (27, 's'),
    (28, 'p'),
    (29, 's'),
    (30, 'p'),
    (31, 's'),
    (32, 's'),
    (36, 's'),
    (37, 's'),
    (39, 's'),
    (41, 's'),
    (42, 's'),
    (43, 's'),
    (44, 's'),
    (45, 'p'),
    (46, 'p'),
    (47, 's'),
    (49, 's'),
    (86, 's')
)
