from django.contrib import admin
from apps.users.models import Profile, Kyc

# Register your models here.

class KycAdmin(admin.ModelAdmin):
    list_display= ["user", "id_type", "verified"]
    list_filter = ["verified"]
    actions = ['verify_kyc']

    def verify_kyc(self, request, queryset):
        queryset.update(verified=True)
        self.message_user(request, "Selected KYC records have been verified successfully.")
    verify_kyc.short_description = "Mark selected KYC records as verified"

admin.site.register(Kyc, KycAdmin)

    
admin.site.register(Profile)