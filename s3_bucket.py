import boto3

s3_client = boto3.resource('s3')

# to shows list of buckets
# for bucket in s3_client.buckets.all():
#     print(bucket.name)

# upload file/s to s3 bucket
# data = open('gst_notice/G5/DRC 1 Abhijeet Krishi Seva Kendra 20-21.pdf',  'rb')
# response = s3_client.Bucket('demo-patronaid').put_object( Key='GST/Intimation/Annexure Drop Proceeding.pdf', Body=data)

# print('response - ',response)

# s3_client.Bucket('demo-patronaid').upload_file(Filename='gst_notice/G1/Annexure Drop Proceeding.pdf', Key='Annexure Drop Proceeding.pdf')

# result = s3_client.Bucket('demo-patronaid').download_file('GST APL-02.pdf','GST/APPEAL/Orders/GST APL-02.pdf')
result = s3_client.meta.client.download_file('demo-patronaid', 'GST/APPEAL/Orders/GST APL-02.pdf', 'GST APL-02.pdf')  # this worked
# client = boto3.client('s3')
# client.download_file(
#     Filename='GST APL-02.pdf',
#     Bucket='demo-patronaid',
#     Key='GST/APPEAL/Orders/GST APL-02.pdf'
# )
# client.head_object(Bucket='demo-patronaid',Key='GST/APPEAL/Orders/GST APL-02.pdf')

print(result)