import redis
import json
from log_file import setup_logging
logger = setup_logging('check_redis')

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("\n================ REDIS MODEL RESULTS ================\n")

# Get all keys
keys = r.keys("*")

if not keys:
    print("No keys found in Redis.")
else:
    for key in keys:
        value = r.get(key)

        if value:
            try:
                data = json.loads(value)

                # Only process model result keys
                if "model_name" in data:
                    logger.info("====================================================")
                    logger.info(f"KEY: {key}")
                    logger.info("MODEL:", data["model_name"])
                    logger.info("----------------------------------------------------")

                    # Accuracies
                    logger.info(f"Train Accuracy : {data['train_accuracy']}")
                    logger.info(f"Val Accuracy   : {data['val_accuracy']}")
                    logger.info(f"Test Accuracy  : {data['test_accuracy']}")


                    # Losses (if available)
                    logger.info(f"Train Loss : {data.get('train_loss')}")
                    logger.info(f"Val Loss   : {data.get('val_loss')}")
                    logger.info(f"Test Loss  : {data.get('test_loss')}")


                    # Confusion Matrix
                    logger.info("Confusion Matrix:")
                    cm = data.get("confusion_matrix", [])
                    for row in cm:
                        logger.info(f"{row}")


                    # Classification Report
                    logger.info("Classification Report:")
                    report = data.get("classification_report", {})
                    logger.info(json.dumps(report, indent=2))

                    logger.info("====================================================\n")

            except Exception as e:
                logger.info(f"Error reading key {key}: {e}")

logger.info("\n================ END =================\n")