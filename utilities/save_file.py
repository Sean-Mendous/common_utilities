import json
import csv
import os

def save_by_json(data, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'a') as f:
            json.dump(data, f, indent=4)
        
        return True

    except Exception as e:
        return False


def save_by_csv(data, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerows(zip(*data.values()))
        
        return True

    except Exception as e:
        return False


def save_by_txt(data, output_path): 
    try:
        if not os.path.exists(output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            for key, value in data.items():
                f.write(f'{key}: {value}\n')
        
        return True

    except Exception as e:
        return False