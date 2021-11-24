# import os

# from dotenv import load_dotenv

# from ftp import download_data
from data import create_catarinense_data, create_close_up
# from enrich import enrich
# from upload import toPostgre

from catarinense.pipeline import pipeline



def main():
    # load_dotenv()
    # download_data()
    
    df_catarinense_data = create_catarinense_data()
    df_close_up = create_close_up()

    # data = {
    #     os.getenv('SHEET_CLIENTS'): df_catarinense_data,
    #     os.getenv('SHEET_POTENTIALS'): df_close_up,
    # }
    
    # data = enrich(data)

    # df = data[os.getenv('SHEET_CLIENTS')]
    # toPostgre(df, 'catarinense_data')

    # df = data[os.getenv('SHEET_POTENTIALS')]
    # toPostgre(df, 'close_up')

    print('Finished!!!')


def main2():
    pipeline()
    

if __name__ == '__main__':
    # main()
    main2()
