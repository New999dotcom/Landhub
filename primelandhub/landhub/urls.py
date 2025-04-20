from django.urls import path
from .import views
from django.urls import path
from .views import forum_home, question_detail, add_question, add_answer, upvote_answer

urlpatterns = [
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('user_management/',views.listusers,name='user_management'),
    path('deleteusers/<int:id>',views.deleteusers,name='deleteusers'),
    path('deleteproperty/<int:id>',views.deleteproperty,name='deleteproperty'),
    path('propertyviewadmin/',views.propertylisting,name='propertyviewadmin'),
    path('message/',views.message,name='message'),
    path('views_messages/',views.view_messages,name='viewmessage'),
    path('reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('user_replied/',views.user_replied_messages,name='user_replied'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('login/',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('deleteprofile/',views.deleteprofile,name='deleteprofile'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('contact/',views.contact,name='contact'),
    path('viewproperty/',views.viewproperty,name='viewproperty'),
    path('edit_property/<int:property_id>/', views.edit_property, name='edit_property'),
    path('delete_property/<int:property_id>/', views.delete_property, name='delete_property'),
    path('delteproperty/<int:id>',views.delteproperty,name='delteproperty'),
    
    path('chatbot/',views.chatbot,name='chatbot'),
    path('chatbot2/',views.chatbot2,name='chatbot2'),
    path('property/',views.addproperty,name='property'),
    path('logout/',views.logout,name='logout'),
    path('review/',views.add_review, name='review'),
    path('buyer_review/', views.add_buyer_review, name='buyer_review'),
   
    
    
    path('viewproperties/', views.view_properties, name='viewproperties'),
    path('viewproperties/<int:id>/', views.view_property_detail, name='viewpropertydetail'),
    
    path('property_detail/<int:property_id>/', views.property_detail, name='property_detail'),
    path('search/', views.property_search, name='property_search'),
    path('api/hybrid-recommendations/', views.hybrid_recommendation, name='hybrid_recommendations'),
    


    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp1, name="password_verify"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("predict_price/", views.predict_property_price, name="predict_price"),
    path("predictprice buyers/", views.predict_property_pricebuyer, name="predictprice buyers"),


    path("forum/", views.forum_home, name="forum_home"),  
    path("forum/question/<int:question_id>/", views.question_detail, name="question_detail"),  
    path("forum/ask/", views.add_question, name="add_question"),
    path("forum/question/<int:question_id>/answer/", views.add_answer, name="add_answer"),
    path("forum/upvote/<int:answer_id>/", views.upvote_answer, name="upvote_answer"),
    path("forum/notifications/", views.notifications, name="notifications"),
    path("forum/notifications/read/", views.mark_notifications_read, name="mark_notifications_read"),

    path('notifications/count/', views.get_notification_count, name='notification_count'),


    path('submit/', views.submit_property, name='submit_property'),  # Property submission page
    path('verify-document/', views.verify_document, name='verify_document'),

    path('wishlist-action/', views.wishlist_action, name='wishlist_action'),


    path('Register_buyer/', views.Register_buyer, name='Register_buyer'),
    path('Verify_otpbuyer/', views.Verify_otp_buyer, name='Verify_otpbuyer'),
    path('Login_buyer/', views.Login_buyer, name='Login_buyer'),
    path('Forgot_passwordbuyer/', views.Forgot_password_buyer, name='Forgot_passwordbuyer'),
    path('Reset_password_otpbuyer/', views.Reset_password_otp_buyer, name='Reset_password_otpbuyer'),
    path('Reset_passwordbuyer/', views.Reset_password_buyer, name='Reset_passwordbuyer'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('buyerprofile/',views.buyer_profile,name='buyerprofile'),
    path('editprofilebuyer/',views.editprofilebuyer,name='editprofilebuyer'),
    path('deleteprofilebuyer/',views.deleteprofilebuyer,name='deleteprofilebuyer'),


    path('property/buyer/<int:property_id>/', views.property_detail_buyer, name='property_detailbuyer'),
    
    path('viewpropertybuyer/',views.viewpropertybuyer,name='viewpropertiesbuyer'),
    path('save/buyer/', views.save_property_buyer, name='save_property_buyer'),


    path('pay/property/<int:property_id>/', views.create_payment, name='create_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),




    path('buyer_message/', views.buyer_message, name='buyer_message'),
    path('view_buyer_messages/', views.view_buyer_messages, name='view_buyer_messages'),
    path('reply_buyer_message/<int:message_id>/', views.reply_buyer_message, name='reply_buyer_message'),
    path('buyer_replied/', views.buyer_replied_messages, name='buyer_replied'),
    path('delete_buyer_message/<int:message_id>/', views.delete_buyer_message, name='delete_buyer_message'),
    path('api/property-search/', views.property_search_api, name='property_search_api'),


    path('seller/chats/', views.chat_list, name='seller_chat_list'),
    path('buyer/chats/', views.buyer_chat_list, name='buyer_chat_list'),



    path('chat/<int:seller_id>/<int:buyer_id>/', views.chat_view, name='chat'),
    

    
    
   

 




  


     ]

   


  


  

    

   
  




