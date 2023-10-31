from django.db import models

# Create your models here.

class Category(models.Model):
    mall_category = models.CharField(max_length=20, primary_key=True)
    mall_category_url = models.CharField(max_length=50, null=True)
    mall_category_name = models.CharField(max_length=20, null=True)

    @classmethod
    def update_or_create_mall(cls, mall_category, mall_category_url=None, mall_category_name=None):
        # 주어진 mall_category로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        mall, created = cls.objects.update_or_create(
            mall_category=mall_category,
            defaults={
                'mall_category_url': mall_category_url,
                'mall_category_name': mall_category_name,
            }
        )


class Mall(models.Model):
    mall_image_id = models.IntegerField(primary_key=True)
    mall_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mall_name = models.CharField(max_length=50, null=True)
    mall_brand = models.CharField(max_length=20, null=True)
    mall_price = models.CharField(max_length=10, null=True)
    mall_url = models.CharField(max_length=50, null=True)
    review_keyword = models.CharField(max_length=50, null=True)
    review_sentiment = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.mall_name
    def __str__(self):
        return self.mall_category

    @classmethod
    def update_or_create_mall(cls, mall_image_id, mall_name=None, mall_brand=None, mall_price=None, mall_category=None, mall_url=None, review_keyword=None, review_sentiment=None):
        # 주어진 mall_image_id로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        mall, created = cls.objects.update_or_create(
            mall_image_id=mall_image_id,
            defaults={
                'mall_name': mall_name,
                'mall_brand': mall_brand,
                'mall_price': mall_price,
                'mall_category': mall_category,
                'mall_url': mall_url,
                'review_keyword': review_keyword,
                'review_sentiment': review_sentiment,  # 필드 이름 수정
            }
        )


class Review(models.Model):
    mall_image_id = models.ForeignKey(Mall, on_delete=models.CASCADE)
    review = models.TextField(null=True)
    review_sentiment = models.BooleanField(default=False)

    @classmethod
    def update_or_create_review(cls, mall_image_id, review=None, review_sentiment=False):
        # 주어진 mall_image_id로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        review, created = cls.objects.update_or_create(
            mall_image_id=mall_image_id,
            defaults={
                'review': review,
                'review_sentiment': review_sentiment,
            }
        )


class Celeb(models.Model):
    celeb_insta_id = models.CharField(max_length=30, primary_key=True)
    celeb_insta_url = models.CharField(max_length=50, null=True)
    celeb_follower = models.CharField(max_length=10, null=True)

    @classmethod
    def update_or_create_celeb(cls, celeb_insta_id, celeb_insta_url=None, celeb_follower=None):
        # 주어진 celeb_insta_id로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        celeb, created = cls.objects.update_or_create(
            celeb_insta_id=celeb_insta_id,
            defaults={
                'celeb_insta_url': celeb_insta_url,
                'celeb_follower': celeb_follower,
            }
        )


class Insta(models.Model):
    celeb_insta_id = models.ForeignKey(Celeb, on_delete=models.SET_NULL, null=True)
    insta_image_id = models.CharField(max_length=30, primary_key=True)
    insta_celeb = models.CharField(max_length=30, null=True)
    insta_product_name = models.CharField(max_length=30, null=True)
    insta_product_brand = models.CharField(max_length=15, null=True)
    insta_product_category = models.CharField(max_length=10, null=True)
    insta_url = models.CharField(max_length=50, null=True)

    @classmethod
    def update_or_create_insta(cls, insta_image_id, celeb_insta_id=None, insta_celeb=None, insta_product_name=None, insta_product_brand=None, insta_product_category=None, insta_url=None):
        # 주어진 insta_image_id로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        insta, created = cls.objects.update_or_create(
            insta_image_id=insta_image_id,
            defaults={
                'celeb_insta_id': celeb_insta_id,
                'insta_celeb': insta_celeb,
                'insta_product_name': insta_product_name,
                'insta_product_brand': insta_product_brand,
                'insta_product_category': insta_product_category,
                'insta_url': insta_url,
            }
        )

        
class Similarity(models.Model):
    insta_image_id = models.ForeignKey(Insta, on_delete=models.CASCADE)
    mall_image_id = models.ForeignKey(Mall, on_delete=models.CASCADE)
    similar_distance = models.CharField(max_length=10, null=True)

    @classmethod
    def update_or_create_insta(cls, insta_image_id):
        # 주어진 insta_image_id로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        insta, created = cls.objects.update_or_create(
            insta_image_id=insta_image_id,
        )
    def update_or_create_mall(cls, mall_image_id, similar_distance=None):
        # 주어진 mall_image_id로 데이터베이스에서 해당 레코드를 업데이트하거나 생성합니다.
        mall, created = cls.objects.update_or_create(
            mall_image_id=mall_image_id,
            defaults={
                'similar_distance': similar_distance,
            }
        )