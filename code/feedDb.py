import os
import json
import uuid
import time
import random
import psycopg2
import argparse
from faker import Faker
from faker_vehicle import VehicleProvider
import logging as logger
from datetime import datetime, timezone, timedelta

# Faker and Logger
faker = Faker(["pt_BR"])
faker.add_provider(VehicleProvider)

logger.basicConfig(format="%(asctime)s (%(levelname)s) %(message)s",
                   datefmt="[%Y-%m-%d %H:%M:%S]", level=logger.INFO)

# Parser config
parser = argparse.ArgumentParser(
    epilog="example: python fake-data-generator.py --qtd 100 --debug true --interval 0",
    description="Gerador automático de dados fictícios para teste, enviando para um tópico específico do postgres."
)
parser.add_argument("--qtd", type=int,
                    help="Quantos registros fictícios deseja gerar?", default=100)
parser.add_argument("--interval", type=float, nargs="?",
                    help="Existe algum intervalo entre as inserções dos registros? [FLOAT]")
parser.add_argument("--debug", type=bool, nargs="?",
                    help="Mostrar em tela os registros inseridos ?")
args = parser.parse_args()

# DbConfig

POSTGRES_DATABASE_USER = os.environ.get("POSTGRES_DATABASE_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE")
POSTGRES_TABLE = os.environ.get("POSTGRES_TABLE")

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DATABASE,
    user=POSTGRES_DATABASE_USER,
    password=POSTGRES_PASSWORD
)

# Fake Data
logger.info("Iniciando a inserção de dados fakes...")
logger.debug("Argumentos: "
             + f"\n       TABLE: {POSTGRES_TABLE}"
             + "\n        Qtd: "+str(args.qtd)
             + "\n        Intervalo: "+str(args.interval)
             )

contador = 0
while contador < args.qtd:
    data = {}
    # data["id"] = random.getrandbits(32)
    data["uuid"] = str(uuid.uuid4())
    data["radar_id"] = random.randint(1, 50000)
    data["license_plate"] = faker.license_plate()
    data["vehicle_make"] = faker.vehicle_make().upper()
    data["vehicle_model"] = faker.vehicle_model().upper()
    data["vehicle_color"] = faker.safe_color_name().upper()
    data["velocity"] = random.randint(20, 160)
    data["velocity_limit"] = random.choice(random.choices(
        [40, 50, 60, 70, 80, 90, 100, 120], weights=(40, 10, 10, 10, 10, 15, 2.5, 2.5), k=1))
    data["country_code"] = "BR"
    data["state_name"] = faker.estado_nome().upper()
    # data["created_at"] = str(faker.date_time_between(start_date="now", tzinfo=timezone(-timedelta(hours=3, minutes=0))))
    # data["updated_at"] = str(faker.date_time_between(start_date="now", tzinfo=timezone(-timedelta(hours=3, minutes=0))))
    # data["sourceTime"] = round(time.time() * 1000)

    contador += 1

    if args.debug:
        logger.info("\n"+("---" * 20))
        print("[Registro: "+str(contador)+"]\n")
        for key, value in data.items():
            print((" " * 5) + str(key) + " -> " + str(value))

        print("\n"+("---" * 20))

    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO source.tb_radar (
                        uuid,
                        radar_id,
                        license_plate,
                        vehicle_make,
                        vehicle_model,
                        vehicle_color,
                        velocity,
                        velocity_limit,
                        country_code,
                        state_name
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        data["uuid"], data["radar_id"], data["license_plate"], data["vehicle_make"],
                        data["vehicle_model"], data["vehicle_color"], data["velocity"], data["velocity_limit"],
                        data["country_code"], data["state_name"])
                    )
        logger.info("Registro ["+str(contador)+"] inserido com sucesso na table: "+str(
            POSTGRES_TABLE)+". Restam ["+(str(args.qtd - contador))+"]")
        conn.commit()
    except (Exception) as error:
        logger.error(f"{error}")
        conn.close()
        exit()

    time.sleep(args.interval if args.interval is not None else 0)
