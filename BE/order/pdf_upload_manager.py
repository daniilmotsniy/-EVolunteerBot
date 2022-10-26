import datetime
import tempfile
from typing import Iterable

import boto3
import requests
from reportlab.lib.utils import ImageReader

from config import settings
from order.pdf_painter import ReportPainter


def get_pdf_url_for_orders(orders: Iterable) -> str:
    filename = get_pdf_file(orders)
    pseudonym = get_file_pseudonym()
    url = upload_file_to_aws(filename, pseudonym)

    return url


def get_pdf_file(orders: Iterable) -> str:
    img_logo = ImageReader('assets/pdf_logo.jpg')
    img_help = ImageReader('assets/pdf_help.jpg')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as file:
        with ReportPainter(file, img_logo, img_help) as painter:
            for order in orders:
                painter.draw_report(order['order_id'], order.get('district', ''), order['name'], order['phone'], order['address'], order['people'], order['comment'] or '')

    return file.name


def get_file_pseudonym() -> str:
    timestamp = datetime.datetime.now().strftime('%Y-&m-%d--%H:%M:%S')
    return f'Orders_{timestamp}.pdf'


def upload_file_to_aws(filename: str, pseudonym: str) -> str:
    s3_client = get_s3_client()
    folder = 'orders/'
    key = f"{folder}{pseudonym}"
    bucket = 'pdfkeeper'
    expires_in = 60

    try:
        response = s3_client.generate_presigned_post(
            Bucket=bucket,
            Key=key,
            ExpiresIn=expires_in
        )
        files = {'file': open(filename, 'rb')}
        url = response['url']
        r = requests.post(url, data=response['fields'], files=files)

        if r.status_code != 204:
            raise AWSUploadError(f'Upload to AWS failed. Status {r.status_code}')

        url_for_download = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires_in
        )
        return url_for_download

    except Exception as err:
        raise AWSUploadError(err.__str__())


def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )


class AWSUploadError(Exception):
    pass
