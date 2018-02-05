from config import server_src_csv_vc06,server_src_csv_vc02,server_src_csv_ppvc06,server_src_csv,vm_src_csv,vm_src_csv_vc06,vm_src_csv_vc02,vm_src_csv_ppvc06
import pandas as pd


def merge_csv(csvs, merge_csvfile):
    dfs = [pd.DataFrame(pd.read_csv(csv)) for csv in csvs]        
    return pd.concat(dfs).to_csv(merge_csvfile)


if __name__ == '__main__':
    merge_csv(csvs=[server_src_csv_vc06,server_src_csv_vc02,server_src_csv_ppvc06], merge_csvfile=server_src_csv)
    merge_csv(csvs=[vm_src_csv_vc06,vm_src_csv_vc02,vm_src_csv_ppvc06], merge_csvfile=vm_src_csv)



