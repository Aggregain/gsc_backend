from django.core.management import BaseCommand
from django.conf import settings
from minio import Minio
from minio.error import S3Error
import json


class Command(BaseCommand):
    help = 'Create Minio bucket and set public policy'

    def handle(self, *args, **kwargs):
        endpoint = settings.AWS_S3_ENDPOINT_URL.replace('http://', '').replace('https://', '')

        client = Minio(
            endpoint,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            secure=False
        )

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        try:
            # Улучшенная проверка существования бакета
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                self.stdout.write(self.style.SUCCESS(f'Bucket {bucket_name} created'))
            else:
                self.stdout.write(self.style.WARNING(f'Bucket {bucket_name} already exists. Skipping creation.'))

            # Всегда устанавливаем политику, даже если бакет уже существует
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [
                            f"arn:aws:s3:::{bucket_name}/static/*",
                            f"arn:aws:s3:::{bucket_name}/media/*"
                        ]
                    }
                ]
            }

            client.set_bucket_policy(bucket_name, json.dumps(policy))
            self.stdout.write(self.style.SUCCESS('Bucket policy updated'))

        except S3Error as exc:
            if exc.code == 'BucketAlreadyOwnedByYou':
                self.stdout.write(self.style.WARNING('Bucket already exists. Policy was updated.'))
            else:
                self.stdout.write(self.style.ERROR(f'Minio error: {exc}'))