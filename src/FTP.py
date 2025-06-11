import os
import paramiko
import logging
import posixpath
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
log_folder = "./logs"
os.makedirs(log_folder, exist_ok=True)
log_file_path = os.path.join(log_folder, "upload_log.txt")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_result(file_name, status):
    logging.info(f"File: {file_name} - Status: {status}")

# FTP Connection Details (from environment variables)
FTP_HOST = os.getenv("FTP_HOST")
FTP_USERNAME = os.getenv("FTP_USERNAME")
FTP_PASSWORD = os.getenv("FTP_PASSWORD")
FTP_PORT = int(os.getenv("FTP_PORT", 22))

# Local source & remote destination folders (from environment variables)
source_folder = os.getenv("SOURCE_FOLDER")
remote_folder = os.getenv("REMOTE_FOLDER")

def upload_files_with_sftp():
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    files = os.listdir(source_folder)
    if not files:
        print("No files to upload.")
        return

    success_count = 0
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            FTP_HOST, port=FTP_PORT, username=FTP_USERNAME, password=FTP_PASSWORD,
            look_for_keys=False, allow_agent=False,
            disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']},
            banner_timeout=300
        )

        sftp = ssh.open_sftp()

        for file_name in files:
            local_path = os.path.join(source_folder, file_name)
            remote_path = posixpath.join(remote_folder, file_name)

            try:
                print(f"Uploading {file_name} to {remote_path}...")
                sftp.put(local_path, remote_path)
                print(f"{file_name} uploaded successfully.")

                if file_name in sftp.listdir(remote_folder):
                    print(f"✅ {file_name} successfully uploaded and verified.")
                    log_result(file_name, "Success")
                    success_count += 1
                else:
                    print(f"❌ Verification failed for {file_name}.")
                    log_result(file_name, "Failure")
            except Exception as e:
                print(f"❌ Failed to upload {file_name}: {e}")
                logging.error(f"Failed to upload {file_name}: {e}")

    except Exception as e:
        print(f"🚨 SFTP Connection Failed: {e}")
        logging.error(f"SFTP Connection Error: {e}")
    finally:
        if 'sftp' in locals():
            sftp.close()
        if 'ssh' in locals():
            ssh.close()

    print(f"Total files uploaded and verified: {success_count}/{len(files)}")
    logging.info(f"Total files uploaded and verified: {success_count}/{len(files)}")

if __name__ == "__main__":
    upload_files_with_sftp()