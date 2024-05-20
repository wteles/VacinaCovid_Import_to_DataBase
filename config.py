from dotenv import dotenv_values
from pathlib import Path
import json

# Carregar as variáveis do arquivo .env
env_address = f"{Path(__file__).resolve().parent}\\.env"
env_vars = dotenv_values(env_address)

oci_user = env_vars.get("OCI_USER")
oci_fingerprint = env_vars.get("OCI_FINGERPRINT")
oci_tenancy = env_vars.get("OCI_TENANCY")
oci_region = env_vars.get("OCI_REGION")
oci_bucketname = env_vars.get("OCI_BUCKET_NAME")

ora_db_user = env_vars.get("LAKE_USER")
ora_db_pass = env_vars.get("LAKE_PW")
ora_db_sn = env_vars.get("LAKE_SN")
ora_db_cmd_user = env_vars.get("LAKE_CMD_USR")
ora_db_cmd_url = env_vars.get("LAKE_CMD_URL")
ora_db_table = env_vars.get("LAKE_TABLE")

# Carregar variáveis
variables_address = f"{Path(__file__).resolve().parent}\\variaveis.json"
with open(variables_address, 'r') as arquivo:
    variaveis = json.load(arquivo)

var_oci_bucket_prefix = variaveis["Settings"][0]["oci_bucket_prefix"]
var_oci_job_semaphore= variaveis["Settings"][0]["oci_job_semaphore"]
