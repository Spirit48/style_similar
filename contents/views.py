from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Category, Mall, Review, Celeb, Insta, Similarity

def insta_image_list(request):
    # 인스타이미지id 리스트
    insta_image_ids = Insta.objects.filter(
        insta_product_category__in=['니트/스웨터', '블라우스/셔츠', '원피스', '구두', '스니커즈', ] # insta_product_category 행의 값이 일치하는 것들만 필터링
    ).values_list('insta_image_id', flat=True) # 해당 row의 insta_image_id의 값을 list 형태로 가져와 insta_image_ids에 저장
    
    context = {"insta_image_ids": insta_image_ids}
    return render(request, 'main.html', context)


def insta_detail(request, insta_image_id):
    # 인스타데이터
    insta_data = Insta.objects.filter(insta_image_id=insta_image_id) # 단일 값이 존재하는지 확인
    if insta_data.exists():
        insta_data = Insta.objects.get(insta_image_id=insta_image_id) # 값이 존재하면 실행
    else:
        return redirect(reverse('insta_image_list')) # 존재하지 않으면 list 페이지로

    # 유사도데이터
    similarity_datas = Similarity.objects.filter(insta_image_id=insta_image_id) # 다중 값이 존재하는지 확인하고 있으면 저장
    
    # mall_image_id_id 값 뽑아내기
    # mall_ids = similarity_datas.values_list('mall_image_id', flat=True)
    # mall_datas = Mall.objects.filter(mall_image_id__in=mall_ids)



    context = {
        'insta_data': insta_data,
        'insta_image_id': insta_image_id,
        'similarity_datas': similarity_datas,
        # 'mall_datas': mall_datas,  # mall_image_id_id 값 추가 
    }
    return render(request, 'insta_detail.html', context)


def product_detail(request, mall_image_id):

    # 유사도데이터
    similarity_datas = Similarity.objects.filter(mall_image_id_id=mall_image_id) # 다중 값이 존재하는지 확인하고 있으면 저장
    
    # 쇼핑몰데이터    
    mall_data = Mall.objects.filter(mall_image_id=mall_image_id) # 단일 값이 존재하는지 확인
    if mall_data.exists():
        mall_data = Mall.objects.get(mall_image_id=mall_image_id) # 값이 존재하면 실행

    review_data = Review.objects.filter(mall_image_id=mall_image_id)
    review_count = review_data.count()

    context = {"mall_image_id":mall_image_id, "mall_data": mall_data, "review_count":review_count,'similarity_datas': similarity_datas,}
    return render(request, 'product_detail.html', context)