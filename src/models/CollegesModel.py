from .DatabaseConnection import execute_query, FetchMode
from .BaseTableModel import BaseTableModel

from src.cache import cache

class CollegesModel(BaseTableModel):

    _table_name : str = "colleges"
    _primary : str = "code"
    _columns : list[str] = ["code", "name"]

    # CREATE TABLE IF NOT EXISTS public.colleges
    # (
    #     code character varying(5) COLLATE pg_catalog."default" NOT NULL,
    #     name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #     CONSTRAINT colleges_pkey PRIMARY KEY (code),
    #     CONSTRAINT unique_college_name UNIQUE (name),
    #     CONSTRAINT college_code_format CHECK (code::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(code::text) <= 5),
    #     CONSTRAINT college_name_format CHECK (name::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(name::text) <= 100)
    # )

    @classmethod
    def delete(cls, key):
        cls.general_cache_clear()
        cache.delete_memoized(cls.college_info, key)
        super().delete(key)

    @classmethod
    def update(cls, orig_key, data):
        cls.general_cache_clear()
        cache.delete_memoized(cls.college_info, orig_key)
        super().update(orig_key, data)

    @classmethod
    @cache.memoize(timeout=300)
    def college_info(
        cls,
        code : str
    ) -> dict[int | str] :
        """
        Returns the complete details of a college record along with
        the total programs and students under it.
        """

        return execute_query(
            query = (
                "SELECT "
                "c.code, c.name, "
                "COUNT(DISTINCT p.code) as totalprgs, "
                "COUNT(s.id) as totalstds "
                "FROM colleges as c "
                "LEFT JOIN programs as p on c.code = p.collegecode "
                "LEFT JOIN students as s on p.code = s.programcode "
                "WHERE c.code = %s "
                "GROUP BY c.code, c.name "
            ),
            params = (code,),
            fetch = FetchMode.ONE,
            as_dict = True
        )