from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, Template
from .serializers import OrderSerializer, TemplateSerializer
from django.core.files.storage import default_storage
from PIL import Image
import uuid

class OrderLoginAPI(generics.CreateAPIView):
    # 订单号登录验证
    def post(self, request):
        order_no = request.data.get('order_no')
        try:
            order = Order.objects.get(order_no=order_no)
            return Response({'user_id': order.user_id, 'message': '登录成功'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': '无效订单号'}, status=status.HTTP_400_BAD_REQUEST)

class ImageUploadAPI(generics.CreateAPIView):
    # 图片上传处理
    def post(self, request):
        user_id = request.data.get('user_id')
        image_file = request.FILES.get('image')
        
        # 生成唯一文件名
        file_ext = image_file.name.split('.')[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        
        # 保存并压缩图片（示例）
        with default_storage.open(f'uploads/{file_name}', 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        
        # 生成缩略图
        img = Image.open(image_file)
        img.thumbnail((800, 600))
        img.save(f'media/thumbnails/{file_name}')
        
        return Response({'file_path': f'uploads/{file_name}'}, status=status.HTTP_201_CREATED)

class TemplateListAPI(generics.ListAPIView):
    # 获取模板列表
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    def get_queryset(self):
        return Template.objects.filter(is_active=True).order_by('-update_time')
    