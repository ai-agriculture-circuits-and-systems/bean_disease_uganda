#!/usr/bin/env python3
"""
重组 bean_disease_uganda 数据集为标准结构

从 data/origin/ 目录读取原始数据（train/, validation/, test/），
重组为标准化的 beans/ 目录结构。

Usage:
    python scripts/reorganize_dataset.py [root_dir]
    
    root_dir: 数据集根目录（默认为当前目录）
"""
import json
import shutil
from pathlib import Path
from collections import defaultdict

def load_json(json_path):
    """加载JSON文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def json_to_csv(json_data, csv_path):
    """将JSON标注转换为CSV格式"""
    annotations = json_data.get('annotations', [])
    if not annotations:
        return
    
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("#item,x,y,width,height,label\n")
        for idx, ann in enumerate(annotations):
            bbox = ann['bbox']  # [x, y, width, height]
            category_id = ann['category_id']
            f.write(f"{idx},{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},{category_id}\n")

def reorganize_dataset(root_dir):
    """重组数据集"""
    root = Path(root_dir)
    
    # 原始数据目录
    origin_dir = root / 'data' / 'origin'
    
    # 子类别映射
    subcategories = {
        'healthy': 'healthy',
        'bean_rust': 'bean_rust',
        'angular_leaf_spot': 'angular_leaf_spot'
    }
    
    # 统计信息
    stats = defaultdict(lambda: defaultdict(int))
    image_lists = defaultdict(lambda: defaultdict(list))
    
    # 处理每个划分
    for split in ['train', 'validation', 'test']:
        split_dir = origin_dir / split
        if not split_dir.exists():
            continue
            
        for subcat_name, subcat_dir_name in subcategories.items():
            subcat_dir = split_dir / subcat_dir_name
            if not subcat_dir.exists():
                continue
            
            # 目标目录
            target_images_dir = root / 'beans' / subcat_dir_name / 'images'
            target_json_dir = root / 'beans' / subcat_dir_name / 'json'
            target_csv_dir = root / 'beans' / subcat_dir_name / 'csv'
            
            # 处理每个图像文件
            for img_path in subcat_dir.glob('*.jpg'):
                img_name = img_path.stem  # 不含扩展名
                json_path = subcat_dir / f"{img_name}.json"
                
                if not json_path.exists():
                    print(f"Warning: JSON file not found for {img_path}")
                    continue
                
                # 加载JSON数据
                json_data = load_json(json_path)
                
                # 更新图像文件名（移除split前缀）
                # 例如: bean_rust_train.237 -> bean_rust_train_237
                new_img_name = img_name.replace('.', '_')
                
                # 复制图像文件
                target_img_path = target_images_dir / f"{new_img_name}.jpg"
                shutil.copy2(img_path, target_img_path)
                
                # 更新JSON中的文件名
                if json_data.get('images'):
                    json_data['images'][0]['file_name'] = f"{new_img_name}.jpg"
                
                # 保存JSON文件
                target_json_path = target_json_dir / f"{new_img_name}.json"
                with open(target_json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                
                # 生成CSV文件
                target_csv_path = target_csv_dir / f"{new_img_name}.csv"
                json_to_csv(json_data, target_csv_path)
                
                # 统计和记录
                stats[subcat_dir_name][split] += 1
                image_lists[subcat_dir_name][split].append(new_img_name)
    
    # 生成sets文件
    for subcat_name in subcategories.values():
        sets_dir = root / 'beans' / subcat_name / 'sets'
        
        # 合并所有划分的图像列表
        all_images = []
        train_images = image_lists[subcat_name].get('train', [])
        val_images = image_lists[subcat_name].get('validation', [])
        test_images = image_lists[subcat_name].get('test', [])
        
        all_images = train_images + val_images + test_images
        
        # 写入划分文件
        if train_images:
            with open(sets_dir / 'train.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(train_images)) + '\n')
        
        if val_images:
            with open(sets_dir / 'val.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(val_images)) + '\n')
        
        if test_images:
            with open(sets_dir / 'test.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(test_images)) + '\n')
        
        if all_images:
            with open(sets_dir / 'all.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(all_images)) + '\n')
            
            train_val_images = train_images + val_images
            if train_val_images:
                with open(sets_dir / 'train_val.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(sorted(train_val_images)) + '\n')
    
    # 打印统计信息
    print("\n数据集重组完成！统计信息：")
    print("=" * 60)
    for subcat_name in sorted(subcategories.values()):
        print(f"\n{subcat_name}:")
        total = 0
        for split in ['train', 'validation', 'test']:
            count = stats[subcat_name].get(split, 0)
            total += count
            if count > 0:
                print(f"  {split}: {count}")
        print(f"  总计: {total}")
    print("=" * 60)

if __name__ == '__main__':
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    reorganize_dataset(root_dir)

