"""Este módulo contém funções para realizar a extração dos dados das fontes da
catarinense."""

import os
import ftplib


def extract() -> None:
    """Realiza a etapa de extração dos dados.
    
    Returns
        None
    """
    path_prefix = 'data/catarinense'

    if not os.path.exists(path_prefix):
        os.mkdir(path_prefix)

    print('Iniciando download dos dados')
    download_data(path_prefix)
    print('Download dos dados terminado')

    # Os dados da catarinense, apesar de vir com extensão .TXT, são dados
    # separados por vírgula, então vamos apenas renomear os arquivos.
    rename_data(path_prefix)


def download_data(dest_dir: str) -> None:
    """Realiza o download dos dados do FTP da catarinense.
    
    Args
        dest_dir (str) -- O diretório de destino dos dados baixados.

    Returns
        None.
    """
    ftp = ftplib.FTP((os.getenv('FTP_HOST')), (os.getenv('FTP_USER')), (os.getenv('FTP_PASSWORD')))
    ftp.cwd("/")
    filematch = '*.TXT'

    for filename in ftp.nlst(filematch):
        target_file_name = os.path.join(dest_dir, os.path.basename(filename))
        with open(target_file_name, 'wb') as fhandle:
            ftp.retrbinary('RETR %s' % filename, fhandle.write)


def rename_data(path_prefix) -> None:
    """Renomeia os arquivos baixados e padroniza o texto.
    
    Args
        path_prefix (str) -- O diretório onde os dados se encontram.

    Returns
        None.
    """
    for filename in os.listdir(path_prefix):
        formatted_filename = filename \
            .lower() \
            .replace('txt', 'csv')

        src = f'{path_prefix}/{filename}'
        dst = f'{path_prefix}/{formatted_filename}'
        os.rename(src, dst)
