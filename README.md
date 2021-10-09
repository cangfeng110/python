# 案例截取 

## 已有服务器上的跑车日志 

### log下载及解压存储 

魔方： 

```
python3 mofang_data_download.py --output-path /path/to/save/logs/ --sdate log_start_date --edate log_end_date --vehicle-name vehicle_name --parent-id parent_id
```

洛书： 

```
python3 loshu_data_download.py --output-path /path/to/save/logs/ --sdate log_start_date --edate log_end_date --vehicle-name vehicle_name
```

### log回放及案例截取 

单个log文件夹： 

```
bash extract_scenario_cases_replay_one_log.sh log_path run_path case_path scenario
```

含有多个log的文件夹： 

```
bash extract_scenario_cases_replay_multi_logs.sh log_path run_path case_path scenario
```

## 新跑车日志（output_pred_scenario_case_log实时打开） 

### log下载及解压存储 

同上。 

### 案例截取 

单个log文件夹： 

```
bash extract_scenario_cases_real_one_log.sh log_path run_path case_path scenario
```

含有多个log的文件夹： 

```
bash extract_scenario_cases_real_multi_logs.sh log_path run_path case_path scenario
```

# 案例序列化 

单个case： 

```
bash serialization_one_case.sh case_path
```

含多个case的文件夹： 

```
bash serialization_multi_cases.sh case_path
```

# 案例数据库管理 

## 案例上传 

```
python uploadData.py -submit 1 -case case_path -label label
```

## 案例下载 

```
python uploadData.py -download 1 -label label -caseId id -mylocal output_path -ucdf 1
```

## 案例删除 

```
python uploadData.py -delete 1 -case case_path
python uploadData.py -delete 1 -label label -caseId id
```

## 案例更新 

```
python uploadData.py -update 1 -case case_path -label label
```

# 案例自动标注 

 

# 案例特征提取