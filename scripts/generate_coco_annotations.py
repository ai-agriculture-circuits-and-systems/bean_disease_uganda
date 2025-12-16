#!/usr/bin/env python3
"""
Generate COCO format JSON annotation files for Bean Disease Uganda dataset.

This script processes images from data/origin/ directory structure and generates
individual COCO format JSON files for each image.

Usage:
    python scripts/generate_coco_annotations.py [root_dir]
    
    root_dir: Dataset root directory (default: parent directory of script)
    
Note: This script processes the original data structure in data/origin/.
For standardized structure, use scripts/reorganize_dataset.py and scripts/convert_to_coco.py.
"""
import os
import json
import random
import time
from pathlib import Path

def generate_unique_id():
    """Generate a unique 10-digit ID: 7 random digits + 3 timestamp digits"""
    random_part = random.randint(1000000, 9999999)
    timestamp_part = int(time.time() * 1000) % 1000
    return random_part * 1000 + timestamp_part

def get_image_info(image_path, category_id, category_name, supercategory):
    """Generate image information for COCO format"""
    file_size = os.path.getsize(image_path)
    file_name = os.path.basename(image_path)
    
    return {
        "id": generate_unique_id(),
        "width": 512,
        "height": 512,
        "file_name": file_name,
        "size": file_size,
        "format": "JPEG",
        "url": "",
        "hash": "",
        "status": "success"
    }

def get_annotation_info(image_id, category_id):
    """Generate annotation information for COCO format"""
    return {
        "id": generate_unique_id(),
        "image_id": image_id,
        "category_id": category_id,
        "segmentation": [],
        "area": 262144,
        "bbox": [0, 0, 512, 512]
    }

def get_category_info(category_id, category_name, supercategory):
    """Generate category information for COCO format"""
    return {
        "id": category_id,
        "name": category_name,
        "supercategory": supercategory
    }

def create_coco_json(image_path, category_id, category_name, supercategory):
    """Create individual COCO JSON file for a single image"""
    
    # Generate unique IDs
    image_id = generate_unique_id()
    annotation_id = generate_unique_id()
    
    # Create COCO format structure
    coco_data = {
        "info": {
            "description": "data",
            "version": "1.0",
            "year": 2025,
            "contributor": "search engine",
            "source": "augmented",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [
            {
                "id": image_id,
                "width": 512,
                "height": 512,
                "file_name": os.path.basename(image_path),
                "size": os.path.getsize(image_path),
                "format": "JPEG",
                "url": "",
                "hash": "",
                "status": "success"
            }
        ],
        "annotations": [
            {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": [],
                "area": 262144,
                "bbox": [0, 0, 512, 512]
            }
        ],
        "categories": [
            {
                "id": category_id,
                "name": category_name,
                "supercategory": supercategory
            }
        ]
    }
    
    return coco_data

def process_directory(root_dir=None):
    """Process all images in the dataset and generate individual JSON files
    
    Args:
        root_dir: Dataset root directory (default: parent directory of script)
    """
    if root_dir is None:
        # Default to parent directory of script (dataset root)
        root_dir = Path(__file__).resolve().parent.parent
    
    root = Path(root_dir)
    origin_dir = root / "data" / "origin"
    
    # Define category mappings
    categories = {
        "bean_rust": {"id": 1, "name": "bean_rust", "supercategory": "train"},
        "angular_leaf_spot": {"id": 2, "name": "angular_leaf_spot", "supercategory": "train"},
        "healthy": {"id": 3, "name": "healthy", "supercategory": "train"}
    }
    
    # Process each dataset split
    for split in ["train", "test", "validation"]:
        split_dir = origin_dir / split
        if not split_dir.exists():
            continue
            
        # Update supercategory based on split
        for category_name in categories:
            categories[category_name]["supercategory"] = split
            
        # Process each category
        for category_name, category_info in categories.items():
            category_dir = split_dir / category_name
            if not category_dir.exists():
                continue
                
            print(f"Processing {split}/{category_name}...")
            
            # Process each image in the category
            for image_file in category_dir.glob("*.jpg"):
                if image_file.is_file():
                    # Create COCO JSON data
                    coco_data = create_coco_json(
                        str(image_file),
                        category_info["id"],
                        category_info["name"],
                        category_info["supercategory"]
                    )
                    
                    # Generate JSON filename (same name as image but .json extension)
                    json_filename = image_file.stem + ".json"
                    json_path = image_file.parent / json_filename
                    
                    # Write JSON file
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(coco_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Generated: {json_path}")

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else None
    process_directory(root_dir)
    print("All COCO JSON files generated successfully!") 