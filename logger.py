import logging
import os
import zipfile
from datetime import datetime


# Create necessary directories if they don't exist
def create_directories():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    archived_dir = 'logs/archived'
    if not os.path.exists(archived_dir):
        os.makedirs(archived_dir)


# Get today's log filename
def get_log_filename():
    today = datetime.now().strftime('%d_%m_%y')
    return f'logs/kannada_nudi_{today}.log'


# Archive log files older than 5 days, excluding today's log
def archive_old_logs():
    archived_dir = 'logs/archived'
    today = datetime.now()
    archive_name = f'kannada_nudi_logs_archived_{today.strftime("%d_%m_%Y")}.zip'
    archive_path = os.path.join(archived_dir, archive_name)

    # Find log files older than 5 days
    logs_to_archive = []
    for log_file in os.listdir('logs'):
        if log_file.endswith('.log'):
            # Extract date part correctly
            log_date_str = '_'.join(log_file.replace('.log', '').split('_')[-3:])
            try:
                log_date = datetime.strptime(log_date_str, '%d_%m_%y')
                if (today - log_date).days > 5:  # Log files older than 5 days
                    logs_to_archive.append(log_file)
            except ValueError:
                print(f"Skipping file with unexpected format: {log_file}")

    # Archive and remove old logs
    if logs_to_archive:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for log_file in logs_to_archive:
                log_path = os.path.join('logs', log_file)
                zipf.write(log_path, arcname=log_file)
                os.remove(log_path)  # Remove log after archiving


# Set up and return a logger with file and console handlers
def setup_logger(logger_name=None):
    create_directories()
    archive_old_logs()
    log_filename = get_log_filename()

    if logger_name:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger(__name__)

    logger.handlers = []  # Clear previous handlers
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
