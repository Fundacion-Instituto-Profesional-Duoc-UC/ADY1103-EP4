import time
import random
import logging
import binascii
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# ==========================================
# CONFIGURACIÓN INICIAL (Vía IAM Role)
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("FinOps_Lab")

# boto3 tomará las credenciales automáticamente del IAM Role de la instancia EC2
cw_client = boto3.client('cloudwatch', region_name='us-east-1')
CW_NAMESPACE = "FinOpsLab/Billing"

# ==========================================
# DEFINICIÓN DE RUBROS FINOPS (Pesos de Costos)
# ==========================================
SECTORS = {
    "1": {
        "rubro": "Banco",
        "services": {
            "AmazonRDS": (8.0, 12.0),
            "AWSKMS": (3.0, 5.0),
            "AmazonCloudWatch": (1.0, 2.0)
        }
    },
    "2": {
        "rubro": "Clinica",
        "services": {
            "AmazonS3": (5.0, 9.0),
            "AmazonEC2": (2.0, 4.0),
            "AmazonCloudWatch": (0.5, 1.5)
        }
    },
    "3": {
        "rubro": "Fintech",
        "services": {
            "AmazonEC2": (10.0, 15.0),
            "AmazonElastiCache": (4.0, 7.0),
            "AmazonCloudWatch": (1.0, 2.5)
        }
    },
    "4": {
        "rubro": "Ecommerce",
        "services": {
            "AmazonCloudFront": (7.0, 11.0),
            "AmazonDynamoDB": (4.0, 8.0),
            "AmazonCloudWatch": (1.0, 2.0)
        }
    },
    "5": {
        "rubro": "Contabilidad",
        "services": {
            "AWSLambda": (3.0, 6.0),
            "AmazonRDS": (4.0, 7.0),
            "AmazonCloudWatch": (0.5, 1.0)
        }
    }
}

REGIONS = ["us-east-1", "sa-east-1"]
ENVIRONMENTS = ["Production", "Development"]

# ==========================================
# VARIABLE GLOBAL: DÍA DEL INCIDENTE
# ==========================================
INCIDENT_DAY_AGO = random.randint(1, 7)

def chunk_list(lista, n):
    """Divide la lista en bloques para respetar los límites de la API de AWS"""
    for i in range(0, len(lista), n):
        yield lista[i:i + n]

def _apply_market_fluctuations(d_delta, e_val, r_val, s_val):
    """
    Ajuste de tasas de mercado ofuscado para camuflar el incidente
    del ojo inexperto de los estudiantes.
    """
    multiplier = 1.0
    try:
        e_hex = binascii.hexlify(e_val.encode('utf-8')).decode('utf-8')
        s_hex = binascii.hexlify(s_val.encode('utf-8')).decode('utf-8')
        
        # '446576656c6f706d656e74' = "Development"
        # '416d617a6f6e436c6f75645761746368' = "AmazonCloudWatch"
        if d_delta == INCIDENT_DAY_AGO and e_hex == '446576656c6f706d656e74' and s_hex == '416d617a6f6e436c6f75645761746368' and 'east-1' in r_val:
            multiplier = random.uniform(8.0, 15.0) 
    except Exception:
        pass
        
    return multiplier

def generate_historical_cost_data(sector_config):
    """Genera 13 días de datos de facturación hacia el pasado"""
    metric_data = []
    
    # FIX SRE 1: Redondeamos a la hora en punto para evitar duplicados en CloudWatch
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_date = now - timedelta(days=13) 
    
    services_dict = sector_config["services"]
    
    current_date = start_date
    while current_date <= now:
        for region in REGIONS:
            for env in ENVIRONMENTS:
                for service_name, cost_range in services_dict.items():
                    
                    if env == "Production":
                        base_cost = random.uniform(cost_range[0], cost_range[1])
                    else:
                        base_cost = random.uniform(cost_range[0] * 0.2, cost_range[1] * 0.4)
                    
                    if region == "sa-east-1":
                        base_cost *= 1.3
                    
                    days_ago = (now - current_date).days
                    base_cost *= _apply_market_fluctuations(days_ago, env, region, service_name)

                    metric_data.append({
                        'MetricName': 'HourlyEstimatedCharge',
                        'Dimensions': [
                            {'Name': 'Service', 'Value': service_name},
                            {'Name': 'Region', 'Value': region},
                            {'Name': 'Environment', 'Value': env}
                        ],
                        'Timestamp': current_date,
                        'Value': round(base_cost, 4),
                        'Unit': 'None'
                    })
                    
        current_date += timedelta(hours=1)
        
    return metric_data

def main():
    print("=== SRE LAB 4.1: FINOPS DINÁMICO (VÍA IAM ROLE) ===")
    for key, val in SECTORS.items():
        print(f"[{key}] {val['rubro']}")
    
    choice = input("\nSelecciona el rubro de la empresa (1-5): ").strip()
    if choice not in SECTORS:
        print("Opción inválida.")
        return

    sector_config = SECTORS[choice]
    logger.info(f"Generando historial de facturación para: {sector_config['rubro']}...")
    
    metric_data = generate_historical_cost_data(sector_config)
    batches = list(chunk_list(metric_data, 10))
    
    logger.info(f"Iniciando subida a CloudWatch ({len(metric_data)} registros)...")
    
    # FIX SRE 2 y 3: Try-Except por lote y pausas para mitigar Throttling
    exitos = 0
    for i, batch in enumerate(batches, 1):
        try:
            cw_client.put_metric_data(Namespace=CW_NAMESPACE, MetricData=batch)
            exitos += 1
            if i % 10 == 0:
                print(f"Progreso: {i}/{len(batches)} lotes enviados...")
            time.sleep(0.5) # Pausa táctica de 500ms
        except ClientError as e:
            logger.warning(f"Lote {i} rechazado por AWS (Posible Throttling): {e.response['Error']['Message']}")
        except Exception as e:
            logger.error(f"Error inesperado en lote {i}: {str(e)}")
            
    print(f"\n[✓] Carga completada. {exitos}/{len(batches)} lotes subidos con éxito.")
    print("Métricas disponibles en CloudWatch -> Namespace: 'FinOpsLab/Billing'.")

if __name__ == "__main__":
    main()