from django.contrib import admin
from django.urls import path

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .models import ChatHistory

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'timestamp')
    search_fields = ('question', 'answer')
    list_filter = ('timestamp',)

admin.site.register(ChatHistory, ChatHistoryAdmin)

