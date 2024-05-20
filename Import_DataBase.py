from crud_OCI import oci_list_objects, oci_delete_file
from Error_Log import write_erro_log
from ExecOraSQL import execute_sql, execute_sql_multi
from queries import get_query
from config import var_oci_bucket_prefix, var_oci_job_semaphore, ora_db_table, ora_db_cmd_user, ora_db_cmd_url

def get_db_cmd():
    db_cmd = f"""
    BEGIN
        DBMS_CLOUD.COPY_DATA(
            table_name => '{ora_db_table}',
            credential_name => '{ora_db_cmd_user}',
            file_uri_list => '{ora_db_cmd_url}VAR_BUCKET_KEY',
            format => json_object('type' value 'csv', 'delimiter' value ';', 'header' value true)
        );
        END;
    """
    return db_cmd

def import_to_database():
    try:
        # Verifica se há arquivos para baixa
        semaphore_is_true = oci_list_objects(oci_prefix=var_oci_job_semaphore)
        # Se há retorno, baixar arquivos do Bucket para o banco de dados
        if len(semaphore_is_true) > 0:
            # print(semaphore_is_true)
            list_oci_files = oci_list_objects(oci_prefix=var_oci_bucket_prefix)
            execute_sql(f"TRUNCATE TABLE {ora_db_table}")
            for oci_file in list_oci_files:
                oci_file = oci_file.name
                exec_db_cmd = get_db_cmd()
                exec_db_cmd = exec_db_cmd.replace("VAR_BUCKET_KEY", oci_file)
                # print(exec_db_cmd)
                print("----------------------------------------------------")
                print(f"Importando arquivo: {oci_file}")
                print("----------------------------------------------------")
                execute_sql(str_sql=exec_db_cmd)

            # Limpa tabelas de log desnecessarias geradas durante a importacao
            limpa_sql_tb_log = get_query("deletar_tabelas_relatorio_importacao")
            execute_sql_multi(limpa_sql_tb_log)

            # Deleta arquivo bucket semaphore
            oci_delete_file(bucket_key=var_oci_job_semaphore)

            return 0
        else:
            print("------------------------------------------------------")
            print(f"Não há arquivos para importar em {var_oci_bucket_prefix}")
            print("------------------------------------------------------")

            return -1

    except Exception as e:
        write_erro_log(str(e))
        return None
