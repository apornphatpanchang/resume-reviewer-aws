"""
ResumeAPI (Python 3.12) - behind API Gateway HTTP API
  POST /reviews        {file_name, pdf_base64, job_description?} -> {resume_id}
  GET  /reviews/{id}   -> review item (status PENDING / DONE / ERROR)
Env: TABLE_NAME, BUCKET_NAME
"""
import base64
import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3

s3 = boto3.client("s3")
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
BUCKET = os.environ["BUCKET_NAME"]
MAX_PDF = 4 * 1024 * 1024  # API Gateway/Lambda payload limit is ~6 MB (base64)


def num(o):
    if isinstance(o, Decimal):
        return int(o) if o == int(o) else float(o)
    raise TypeError


def reply(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False, default=num),
    }


def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]

    if method == "POST":
        try:
            data = json.loads(event.get("body") or "{}")
            pdf = base64.b64decode(data["pdf_base64"])
        except Exception:  # noqa: BLE001
            return reply(400, {"error": "ข้อมูลที่ส่งมาไม่ถูกต้อง"})
        if not pdf.startswith(b"%PDF") or len(pdf) > MAX_PDF:
            return reply(400, {"error": "ต้องเป็นไฟล์ PDF ขนาดไม่เกิน 4 MB"})

        rid = uuid.uuid4().hex[:12]
        # save the item first so the processor can find the job description
        table.put_item(Item={
            "resume_id": rid,
            "file_name": str(data.get("file_name", "resume.pdf"))[:100],
            "job_description": str(data.get("job_description", ""))[:6000].strip(),
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        s3.put_object(Bucket=BUCKET, Key=f"uploads/{rid}.pdf", Body=pdf,
                      ContentType="application/pdf")
        return reply(200, {"resume_id": rid})

    rid = (event.get("pathParameters") or {}).get("id")
    item = table.get_item(Key={"resume_id": rid}).get("Item") if rid else None
    if not item:
        return reply(404, {"error": "ไม่พบผลการประเมิน"})
    return reply(200, item)
