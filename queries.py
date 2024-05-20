def get_query(query_id:str):
    if query_id == "deletar_tabelas_relatorio_importacao":
        query = [
"""
BEGIN
    EXECUTE IMMEDIATE 'TRUNCATE TABLE TMP_TABELAS_LOG';
    EXECUTE IMMEDIATE 'DROP TABLE TMP_TABELAS_LOG';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN
            RAISE;
        END IF;
END;
"""
,
"""
CREATE GLOBAL TEMPORARY TABLE TMP_TABELAS_LOG
ON COMMIT PRESERVE ROWS
AS
SELECT
        SUBQ.*
,       ROW_NUMBER() OVER(ORDER BY table_name)  AS  RN
FROM    (
        SELECT  DISTINCT
                table_name
        --,       column_name
        FROM    all_tab_columns
        WHERE   table_name    like    '%COPY%'
        ) SUBQ
"""
,
"""
DECLARE     
        VAR_TRUNC_QUERY   VARCHAR2(1000);
        VAR_DROP_QUERY   VARCHAR2(1000);
        VAR_I       INT := 1;
        VAR_SIZE    INT;

BEGIN
    SELECT
            COUNT(*)
    INTO    VAR_SIZE
    FROM    TMP_TABELAS_LOG
    ;
    WHILE VAR_I <= VAR_SIZE LOOP
    BEGIN
        --DBMS_OUTPUT.PUT_LINE(VAR_SIZE);
        SELECT  'TRUNCATE TABLE ' ||
                table_name
        INTO    VAR_TRUNC_QUERY
        FROM    TMP_TABELAS_LOG
        WHERE   RN  =   VAR_I
        ;
        VAR_DROP_QUERY := REPLACE(VAR_TRUNC_QUERY, 'TRUNCATE', 'DROP');

        EXECUTE IMMEDIATE VAR_DROP_QUERY;
        
        VAR_I := VAR_I + 1;
        --VAR_I := 1000;
        EXCEPTION
            WHEN OTHERS THEN
                -- Se ocorrer algum erro, exibir uma mensagem de erro
                DBMS_OUTPUT.PUT_LINE('Ocorreu um erro: ' || SQLERRM);
    END;
    END LOOP;
END;
"""
,
"""
BEGIN
    EXECUTE IMMEDIATE 'TRUNCATE TABLE TMP_TABELAS_LOG';
    EXECUTE IMMEDIATE 'DROP TABLE TMP_TABELAS_LOG';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN
            RAISE;
        END IF;
END;

"""
]
    return query
