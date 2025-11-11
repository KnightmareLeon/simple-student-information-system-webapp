from .DatabaseConnection import execute_query, FetchMode
from .BaseTableModel import BaseTableModel

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