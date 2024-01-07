import json
from PIL import Image
from make_light_logo import process_logo
from s3 import S3Connect
import io

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])  # 메시지 본문을 JSON 객체로 변환
        s3_key = message_body['key']
        
        s3 = S3Connect()
        original_logo = s3.get_s3_image_object(s3_key)
        original_format = original_logo.format
        
        new_logo = process_logo(original_logo, original_format)
        out_img = io.BytesIO()
        new_logo.save(out_img, format=original_format, quality=70)
        out_img.seek(0)
        s3.put_s3_image_object(out_img, s3_key)
    
    return {
        'statusCode': 200
    }