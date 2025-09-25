# ER 図 / Entity Relationship Diagram

## 日本企业数据库 ER 图 / Japanese Enterprise Database ER Diagram

基于 `JpComp_ctbl.sql` 生成的实体关系图，展示了企业数据库的表结构和关系。

```mermaid
erDiagram
    %% 主数据表 (Master Tables) - 使用 _M 后缀
    HIHYOJI_M {
        CHAR(1) code PK "検索対象除外コード"
        VARCHAR(30) name "名前"
    }
    
    LATEST_M {
        CHAR(1) code PK "最新履歴コード" 
        VARCHAR(30) name "名前"
    }
    
    CLOSECAUSE_M {
        CHAR(2) code PK "登記記録閉鎖事由コード"
        VARCHAR(30) name "名前"
    }
    
    KIND_M {
        CHAR(3) code PK "法人種別コード"
        VARCHAR(30) name "名前"
    }
    
    CORRECT_M {
        CHAR(1) code PK "訂正区分コード"
        VARCHAR(30) name "名前"
    }
    
    PROCESS_M {
        CHAR(2) code PK "処理区分コード"
        VARCHAR(30) name "名前"
    }
    
    %% 数据表 (Data Table) - 使用 _T 后缀
    ENTERPRISES_T {
        INT sequenceNumber "一連番号"
        CHAR(13) corporateNumber PK "法人番号"
        CHAR(2) process FK "処理区分"
        CHAR(1) correct FK "訂正区分"
        DATE updateDate "更新年月日"
        DATE changeDate "変更年月日"
        VARCHAR(150) name "商号"
        CHAR(8) nameImageId "商号イメージID"
        CHAR(3) kind FK "法人種別"
        VARCHAR(10) prefectureName "都道府県名"
        VARCHAR(20) cityName "市区町村名"
        VARCHAR(300) streetNumber "丁目番地等"
        CHAR(8) addressImageId "所在地イメージID"
        CHAR(2) prefectureCode "都道府県コード"
        CHAR(3) cityCode "市区町村コード"
        CHAR(7) postCode "郵便番号"
        VARCHAR(300) addressOutside "国外所在地"
        CHAR(8) addressOutsideImageId "国外所在地イメージID"
        DATE closeDate "登記記録閉鎖年月日"
        CHAR(2) closeCause FK "登記記録閉鎖事由"
        CHAR(13) successorCorporateNumber "承継先法人番号"
        VARCHAR(500) changeCause "変更事由詳細"
        DATE assignmentDate "法人番号指定年月日"
        CHAR(1) latest FK "最新履歴"
        VARCHAR(300) enName "商号(英語表記)"
        VARCHAR(9) enPrefectureName "都道府県名(英語表記)"
        VARCHAR(600) enCityName "市区町村名(英語表記)"
        VARCHAR(600) enAddressOutside "国外所在地(英語表記)"
        VARCHAR(500) furigana "フリガナ"
        CHAR(1) hihyoji FK "検索対象除外"
    }
    
    %% 关系定义 / Relationship Definitions
    ENTERPRISES_T ||--o{ PROCESS_M : "process"
    ENTERPRISES_T ||--o{ CORRECT_M : "correct"
    ENTERPRISES_T ||--o{ KIND_M : "kind"
    ENTERPRISES_T ||--o{ CLOSECAUSE_M : "closeCause"
    ENTERPRISES_T ||--o{ LATEST_M : "latest"
    ENTERPRISES_T ||--o{ HIHYOJI_M : "hihyoji"
```

## 表说明 / Table Descriptions

### 主数据表 (Master Tables) - `_M` 后缀

1. **PROCESS_M** (処理区分マスタ)
   - 企业处理状态的主数据表
   - 包含新规、变更、合并等处理类型

2. **CORRECT_M** (訂正区分マスタ)
   - 记录是否为订正记录的主数据表
   - 区分正常记录和订正记录

3. **KIND_M** (法人種別マスタ)
   - 法人类型的主数据表
   - 包含股份公司、有限公司等企业类型

4. **CLOSECAUSE_M** (登記記録閉鎖事由マスタ)
   - 登记记录关闭原因的主数据表
   - 包含清算结束、合并等关闭原因

5. **LATEST_M** (最新履歴マスタ)
   - 记录是否为最新信息的主数据表
   - 区分历史记录和最新记录

6. **HIHYOJI_M** (検索対象除外マスタ)
   - 搜索对象排除的主数据表
   - 控制记录是否在搜索中显示

