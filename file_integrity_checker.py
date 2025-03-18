import hashlib
import os

def calculate_hash(file_path, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def save_hash(file_path, hash_value, hash_file='file_hashes.txt'):
    with open(hash_file, 'a') as f:
        f.write(f"{file_path}|{hash_value}\n")

def load_hashes(hash_file='file_hashes.txt'):
    if not os.path.exists(hash_file):
        return {}
    
    hashes = {}
    with open(hash_file, 'r') as f:
        for line in f:
            file_path, hash_value = line.strip().split('|')
            hashes[file_path] = hash_value
    return hashes

def monitor_file(file_path, hash_file='file_hashes.txt'):
    saved_hashes = load_hashes(hash_file)
    
    if file_path not in saved_hashes:
        print(f"File '{file_path}' is being monitored for the first time.")
        current_hash = calculate_hash(file_path)
        save_hash(file_path, current_hash, hash_file)
        print(f"Initial hash saved: {current_hash}")
    else:
        saved_hash = saved_hashes[file_path]
        current_hash = calculate_hash(file_path)
        
        if current_hash == saved_hash:
            print(f"File '{file_path}' has not been modified.")
        else:
            print(f"File '{file_path}' has been modified!")
            print(f"Saved hash: {saved_hash}")
            print(f"Current hash: {current_hash}")

if __name__ == "__main__":
    file_to_monitor = 'example.txt'
    monitor_file(file_to_monitor)
