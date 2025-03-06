from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.filters import SearchFilter


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # السماح فقط للمستخدمين المسجلين


    authentication_classes = [TokenAuthentication]  # المصادقة عبر التوكن

    filter_backends = [SearchFilter]  # تمكين البحث
    search_fields = ['username', 'email']  # البحث في username و email

    throttle_classes = [UserRateThrottle]  # تطبيق الحد الأقصى للطلبات لكل مستخدم
# -------
#     تحديد معدل الطلبات في الإعدادات (settings.py):
# REST_FRAMEWORK = {
#     'DEFAULT_THROTTLE_RATES': {
#         'user': '5/minute'  # السماح بـ 5 طلبات فقط لكل مستخدم في الدقيقة
#     }
# }
# -----

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)  # يعرض فقط بيانات المستخدم الحالي
    
    def get_serializer_class(self):
        """استخدام Serializer مختلف إذا كان المستخدم مشرفًا"""
        if self.request.user.is_superuser:
            return AdminUserSerializer  # Serializer للمشرفين
        return UserSerializer  # Serializer للمستخدمين العاديين