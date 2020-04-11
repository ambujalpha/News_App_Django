from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
from django.contrib.auth.models import User, Group, Permission
import random
from random import randint
from django.contrib.contenttypes.models import ContentType

