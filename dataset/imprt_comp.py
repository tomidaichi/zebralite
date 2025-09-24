#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV数据导入到ENTERPRISES_T表的Python脚本
Import CSV data to ENTERPRISES_T table
run:
pip install mysql-connector-python
python imprt_comp.py
"""

import csv
import mysql.connector
from mysql.connector import Error
import sys
import logging
from datetime import datetime
from typing import Optional

# 配置日志 / Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('import_log.txt', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 数据库连接配置 / Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'e_stat',
    'user': 'root',
    'password': '',  # 请修改为您的密码 / Please modify to your password
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def parse_date(date_str: str) -> Optional[str]:
    """
    解析日期字符串，转换为MySQL DATE格式
    Parse date string and convert to MySQL DATE format
    """
    if not date_str or date_str.strip() == '':
        return None
    
    try:
        # 假设CSV中的日期格式为YYYY-MM-DD / Assume CSV date format is YYYY-MM-DD
        parsed_date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        return parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        logger.warning(f"无法解析日期: {date_str} / Failed to parse date: {date_str}")
        return None

def clean_string(value: str, max_length: int = None) -> Optional[str]:
    """
    清理字符串数据
    Clean string data
    """
    if not value or value.strip() == '':
        return None
    
    cleaned = value.strip().replace('"', '')
    if max_length and len(cleaned) > max_length:
        logger.warning(f"字符串被截断: {cleaned[:50]}... / String truncated: {cleaned[:50]}...")
        cleaned = cleaned[:max_length]
    
    return cleaned

def create_connection():
    """
    创建数据库连接
    Create database connection
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logger.info("成功连接到MySQL数据库 / Successfully connected to MySQL database")
            return connection
    except Error as e:
        logger.error(f"数据库连接错误: {e} / Database connection error: {e}")
        return None

def import_csv_to_mysql(csv_file_path: str):
    """
    将CSV文件导入到ENTERPRISES_T表
    Import CSV file to ENTERPRISES_T table
    """
    connection = create_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    v_success_count = 0  # 成功导入计数 / Success import count
    v_error_count = 0    # 错误计数 / Error count
    
    try:
        # 准备INSERT语句 / Prepare INSERT statement
        v_insert_query = """
        INSERT INTO ENTERPRISES_T (
            sequenceNumber, corporateNumber, process, correct, updateDate, changeDate,
            name, nameImageId, kind, prefectureName, cityName, streetNumber,
            addressImageId, prefectureCode, cityCode, postCode, addressOutside,
            addressOutsideImageId, closeDate, closeCause, successorCorporateNumber,
            changeCause, assignmentDate, latest, enName, enPrefectureName,
            enCityName, enAddressOutside, furigana, hihyoji
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        # 读取CSV文件 / Read CSV file
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            for v_row_num, row in enumerate(csv_reader, 1):
                try:
                    if len(row) < 30:  # 确保有足够的列 / Ensure enough columns
                        logger.warning(f"第{v_row_num}行列数不足: {len(row)} / Row {v_row_num} insufficient columns: {len(row)}")
                        v_error_count += 1
                        continue
                    
                    # 映射CSV列到数据库字段 / Map CSV columns to database fields
                    v_data = (
                        int(row[0]) if row[0].strip() else None,  # sequenceNumber
                        clean_string(row[1], 13),                # corporateNumber
                        clean_string(row[2], 2),                 # process
                        clean_string(row[3], 1),                 # correct
                        parse_date(row[4]),                      # updateDate
                        parse_date(row[5]),                      # changeDate
                        clean_string(row[6], 150),               # name
                        clean_string(row[7], 8),                 # nameImageId
                        clean_string(row[8], 3),                 # kind
                        clean_string(row[9], 10),                # prefectureName
                        clean_string(row[10], 20),               # cityName
                        clean_string(row[11], 300),              # streetNumber
                        clean_string(row[12], 8),                # addressImageId
                        clean_string(row[13], 2),                # prefectureCode
                        clean_string(row[14], 3),                # cityCode
                        clean_string(row[15], 7),                # postCode
                        clean_string(row[16], 300),              # addressOutside
                        clean_string(row[17], 8),                # addressOutsideImageId
                        parse_date(row[18]),                     # closeDate
                        clean_string(row[19], 2),                # closeCause
                        clean_string(row[20], 13),               # successorCorporateNumber
                        clean_string(row[21], 500),              # changeCause
                        parse_date(row[22]),                     # assignmentDate
                        clean_string(row[23], 1),                # latest
                        clean_string(row[24], 300),              # enName
                        clean_string(row[25], 9),                # enPrefectureName
                        clean_string(row[26], 600),              # enCityName
                        clean_string(row[27], 600),              # enAddressOutside
                        clean_string(row[28], 500),              # furigana
                        clean_string(row[29], 1) if len(row) > 29 else '0'  # hihyoji
                    )
                    
                    # 执行插入 / Execute insert
                    cursor.execute(v_insert_query, v_data)
                    v_success_count += 1
                    
                    # 每1000条记录提交一次 / Commit every 1000 records
                    if v_success_count % 1000 == 0:
                        connection.commit()
                        logger.info(f"已导入 {v_success_count} 条记录 / Imported {v_success_count} records")
                        
                except Exception as e:
                    logger.error(f"第{v_row_num}行导入失败: {e} / Row {v_row_num} import failed: {e}")
                    v_error_count += 1
                    continue
        
        # 最终提交 / Final commit
        connection.commit()
        logger.info(f"""
        导入完成 / Import completed:
        - 成功导入: {v_success_count} 条 / Successfully imported: {v_success_count} records
        - 失败记录: {v_error_count} 条 / Failed records: {v_error_count} records
        """)
        
        return True
        
    except Exception as e:
        logger.error(f"导入过程中发生错误: {e} / Error occurred during import: {e}")
        connection.rollback()
        return False
        
    finally:
        cursor.close()
        connection.close()
        logger.info("数据库连接已关闭 / Database connection closed")

def main():
    """
    主函数 / Main function
    """
    import os

    csv_file_path = os.path.expanduser("~/dbdata/00_zenkoku_all_20250829.csv")
    
    logger.info(f"开始导入CSV文件: {csv_file_path} / Starting CSV import: {csv_file_path}")
    
    # 检查文件是否存在 / Check if file exists
    try:
        with open(csv_file_path, 'r'):
            pass
    except FileNotFoundError:
        logger.error(f"文件不存在: {csv_file_path} / File not found: {csv_file_path}")
        return
    
    # 执行导入 / Execute import
    if import_csv_to_mysql(csv_file_path):
        logger.info("CSV导入成功完成 / CSV import completed successfully")
    else:
        logger.error("CSV导入失败 / CSV import failed")

if __name__ == "__main__":
    main()
