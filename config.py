from dotenv import load_dotenv
load_dotenv()
import os

# Configuração para conexão com o banco de dados MySQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'server1.contaja.com.br'),
    'user': os.getenv('DB_USER', 'ctjread'),
    'password': os.getenv('DB_PASSWORD', 'ctj$23*jalhar'),
    'database': os.getenv('DB_NAME', 'contagen_api_v2')
}
